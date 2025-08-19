from django.shortcuts import render

# Create your views here.
# vehiculos/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.utils import timezone
from datetime import datetime, timedelta
from django.template.loader import render_to_string
import json

from .models import Vehiculo,  RegistroAcceso, ConfiguracionSistema
from .forms import VehiculoForm, RegistroAccesoForm, BusquedaForm
from instructores.forms import InstructorForm

# Vista principal del módulo
@login_required
def dashboard_vehiculos(request):
    """Dashboard principal con estadísticas del sistema vehicular"""
    # Estadísticas generales
    total_vehiculos = Vehiculo.objects.filter(activo=True).count()
    total_propietarios = InstructorForm.objects.filter(activo=True).count()
    vehiculos_dentro = Vehiculo.objects.filter(activo=True).filter(
        registros_acceso__tipo_movimiento='ENTRADA'
    ).exclude(
        registros_acceso__tipo_movimiento='SALIDA',
        registros_acceso__fecha_hora__gt=timezone.now() - timedelta(hours=1)
    ).count()
    
    # Registros de hoy
    hoy = timezone.now().date()
    registros_hoy = RegistroAcceso.objects.filter(fecha_hora__date=hoy).count()
    
    # Últimos registros
    ultimos_registros = RegistroAcceso.objects.select_related(
        'vehiculo', 'vehiculo__propietario'
    ).order_by('-fecha_hora')[:10]
    
    context = {
        'total_vehiculos': total_vehiculos,
        'total_propietarios': total_propietarios,
        'vehiculos_dentro': vehiculos_dentro,
        'registros_hoy': registros_hoy,
        'ultimos_registros': ultimos_registros,
    }
    
    return render(request, 'vehiculos/dashboard.html', context)


# CRUD para Vehículos
@login_required
def lista_vehiculos(request):
    """Lista de vehículos con paginación y búsqueda"""
    form_busqueda = BusquedaForm(request.GET)
    vehiculos = Vehiculo.objects.filter(activo=True).select_related('propietario')
    
    if form_busqueda.is_valid():
        busqueda = form_busqueda.cleaned_data.get('busqueda')
        if busqueda:
            vehiculos = vehiculos.filter(
                Q(placa__icontains=busqueda) |
                Q(marca__icontains=busqueda) |
                Q(modelo__icontains=busqueda) |
                Q(propietario__nombre_completo__icontains=busqueda)
            )
    
    paginator = Paginator(vehiculos.order_by('placa'), 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'form_busqueda': form_busqueda,
    }
    
    return render(request, 'vehiculos/lista_vehiculos.html', context)

@login_required
def crear_vehiculo(request):
    """Crear nuevo vehículo"""
    if request.method == 'POST':
        form = VehiculoForm(request.POST)
        if form.is_valid():
            vehiculo = form.save()
            messages.success(request, f'Vehículo {vehiculo.placa} registrado exitosamente.')
            return redirect('vehiculos:lista_vehiculos')
    else:
        form = VehiculoForm()
    
    return render(request, 'vehiculos/crear_vehiculo.html', {'form': form})

@login_required
def editar_vehiculo(request, pk):
    """Editar vehículo existente"""
    vehiculo = get_object_or_404(Vehiculo, pk=pk)
    
    if request.method == 'POST':
        form = VehiculoForm(request.POST, instance=vehiculo)
        if form.is_valid():
            form.save()
            messages.success(request, f'Vehículo {vehiculo.placa} actualizado exitosamente.')
            return redirect('vehiculos:lista_vehiculos')
    else:
        form = VehiculoForm(instance=vehiculo)
    
    return render(request, 'vehiculos/editar_vehiculo.html', {
        'form': form, 
        'vehiculo': vehiculo
    })

@login_required
def detalle_vehiculo(request, pk):
    """Ver detalles del vehículo y su historial de accesos"""
    vehiculo = get_object_or_404(Vehiculo, pk=pk)
    registros = vehiculo.registros_acceso.order_by('-fecha_hora')[:20]
    
    context = {
        'vehiculo': vehiculo,
        'registros': registros,
    }
    
    return render(request, 'vehiculos/detalle_vehiculo.html', context)

# Control de Acceso
@login_required
def registro_acceso(request):
    """Registrar entrada o salida de vehículos"""
    if request.method == 'POST':
        placa = request.POST.get('placa', '').strip().upper()
        tipo_movimiento = request.POST.get('tipo_movimiento')
        
        if not placa:
            messages.error(request, 'Debe ingresar una placa válida.')
            return redirect('vehiculos:registro_acceso')
        
        try:
            vehiculo = Vehiculo.objects.get(placa=placa, activo=True)
            
            # Crear registro de acceso
            registro = RegistroAcceso.objects.create(
                vehiculo=vehiculo,
                tipo_movimiento=tipo_movimiento,
                usuario_registro=request.user,
                observaciones=request.POST.get('observaciones', '')
            )
            
            messages.success(
                request, 
                f'{tipo_movimiento} registrada para {vehiculo.placa} - {vehiculo.propietario.nombre_completo}'
            )
            
        except Vehiculo.DoesNotExist:
            messages.error(request, f'No se encontró un vehículo activo con placa {placa}.')
    
    return render(request, 'vehiculos/registro_acceso.html')

@login_required
def buscar_vehiculo_ajax(request):
    """Búsqueda AJAX de vehículo por placa"""
    placa = request.GET.get('placa', '').strip().upper()
    
    if not placa:
        return JsonResponse({'error': 'Placa requerida'}, status=400)
    
    try:
        vehiculo = Vehiculo.objects.select_related('propietario').get(
            placa=placa, activo=True
        )
        
        data = {
            'encontrado': True,
            'placa': vehiculo.placa,
            'marca': vehiculo.marca,
            'modelo': vehiculo.modelo or '',
            'color': vehiculo.get_color_display(),
            'propietario': vehiculo.propietario.nombre_completo,
            'tipo_persona': vehiculo.propietario.get_tipo_persona_display(),
            'esta_dentro': vehiculo.esta_dentro()
        }
        
    except Vehiculo.DoesNotExist:
        data = {'encontrado': False}
    
    return JsonResponse(data)

# Reportes
@login_required
def reportes(request):
    """Página de reportes del sistema"""
    # Filtros por fecha
    fecha_inicio = request.GET.get('fecha_inicio')
    fecha_fin = request.GET.get('fecha_fin')
    
    registros = RegistroAcceso.objects.select_related(
        'vehiculo', 'vehiculo__propietario'
    )
    
    if fecha_inicio:
        registros = registros.filter(fecha_hora__date__gte=fecha_inicio)
    if fecha_fin:
        registros = registros.filter(fecha_hora__date__lte=fecha_fin)
    
    # Estadísticas del período
    total_registros = registros.count()
    entradas = registros.filter(tipo_movimiento='ENTRADA').count()
    salidas = registros.filter(tipo_movimiento='SALIDA').count()
    
    # Paginación
    paginator = Paginator(registros.order_by('-fecha_hora'), 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'total_registros': total_registros,
        'entradas': entradas,
        'salidas': salidas,
        'fecha_inicio': fecha_inicio,
        'fecha_fin': fecha_fin,
    }
    
    return render(request, 'vehiculos/reportes.html', context)