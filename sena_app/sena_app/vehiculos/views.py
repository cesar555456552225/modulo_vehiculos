from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponse
from django.template import loader
from django.urls import reverse_lazy 
from django.views.generic import FormView
from django.shortcuts import get_object_or_404, render
from .models import Vehiculo
from .forms import VehiculoForm

def detalle_vehiculo(request, pk):
    """
    Muestra los detalles de un solo vehículo.
    """
    vehiculo = get_object_or_404(Vehiculo, pk=pk)
    context = {
        'vehiculo': vehiculo,
    }
    return render(request, 'detalle_vehiculo.html', context)


def crear_vehiculo(request):
    """
    Maneja la creación de un vehículo con un formulario.
    """
    if request.method == 'POST':
        form = VehiculoForm(request.POST)
        if form.is_valid():
            vehiculo = form.save()
            messages.success(request, f"El vehículo con placa {vehiculo.placa} se ha creado.")
            return redirect('vehiculos:lista_vehiculos')
    else:
        form = VehiculoForm()

    context = {
        'form': form
    }
    return render(request, 'crear_vehiculo.html', context)


def editar_vehiculo(request, pk):
    """
    Maneja la edición de un vehículo existente.
    """
    vehiculo = get_object_or_404(Vehiculo, pk=pk)
    if request.method == 'POST':
        form = VehiculoForm(request.POST, instance=vehiculo)
        if form.is_valid():
            vehiculo = form.save()
            messages.success(request, f"El vehículo con placa {vehiculo.placa} se ha actualizado.")
            return redirect('vehiculos:lista_vehiculos')
    else:
        form = VehiculoForm(instance=vehiculo)

    context = {
        'form': form
    }
    return render(request, 'editar_vehiculo.html', context)

def vehiculos(request):
    lista_vehiculos = Vehiculo.objects.all()
    template = loader.get_template('vehiculos.html')
    context = {
        'vehiculos': lista_vehiculos,
    }
    return HttpResponse(template.render(context, request))


def main(request):
    template = loader.get_template('main.html')
    return HttpResponse(template.render({}, request)) 


class VehiculoFormView(FormView): 
    template_name = 'crear_vehiculo.html'
    form_class = VehiculoForm
    success_url = reverse_lazy('vehiculos') 

    def form_valid(self, form):
        vehiculo = form.save()
        messages.success(
            self.request,
            f"El vehículo con placa {vehiculo.placa} se ha creado."
        )
        return super().form_valid(form)
    
    class VehiculoCreateView(FormView):
        """
        Vista para crear un vehículo usando un formulario.
        """
        template_name = 'crear_vehiculo.html'
        form_class = VehiculoForm
        success_url = reverse_lazy('vehiculos:lista_vehiculos')
        def form_valid(self, form):
            vehiculo = form.save()
            messages.success(self.request, f"El vehículo con placa {vehiculo.placa} se ha creado.")
            return super().form_valid(form)
        def form_invalid(self, form):
            messages.error(self.request, "Error al crear el vehículo. Por favor, corrige los errores.")
            return super().form_invalid(form)
        