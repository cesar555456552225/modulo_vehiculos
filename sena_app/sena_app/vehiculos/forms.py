# vehiculos/forms.py
# vehiculos/forms.py
from django import forms
from django.core.exceptions import ValidationError
import re

from .models import Vehiculo, Instructor, RegistroAcceso

class VehiculoForm(forms.ModelForm):
    class Meta:
        model = Vehiculo
        fields = [
            'placa', 'tipo_vehiculo', 'marca', 'modelo', 
            'color', 'año', 'propietario', 'observaciones'
        ]
        widgets = {
            'placa': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: ABC123',
                'style': 'text-transform: uppercase;',
                'required': True
            }),
            'tipo_vehiculo': forms.Select(attrs={
                'class': 'form-control form-select',
                'required': True
            }),
            'marca': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Toyota, Honda, Yamaha',
                'required': True
            }),
            'modelo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Corolla, Civic, YBR'
            }),
            'color': forms.Select(attrs={
                'class': 'form-control form-select',
                'required': True
            }),
            'año': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '2024',
                'min': '1900',
                'max': '2030'
            }),
            'propietario': forms.Select(attrs={
                'class': 'form-control form-select',
                'required': True
            }),
            'observaciones': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Observaciones adicionales (opcional)'
            })
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtrar solo propietarios activos
        self.fields['instructor'].queryset = Instructor.objects.filter(activo=True).order_by('nombre')
        
        # Configurar choices dinámicos
        self.fields['propietario'].empty_label = "Seleccione un propietario"
    
    def clean_placa(self):
        placa = self.cleaned_data['placa'].upper().strip()
        
        # Validar formato básico de placa colombiana
        if not re.match(r'^[A-Z]{3}\d{2}[A-Z0-9]$|^[A-Z]{3}\d{3}$', placa):
            # Formato flexible para diferentes tipos de vehículos
            if len(placa) < 5 or len(placa) > 7:
                raise ValidationError(
                    'Formato de placa inválido. Use formato ABC123 o ABC12D.'
                )
        
        return placa
    
    def clean_año(self):
        año = self.cleaned_data.get('año')
        if año:
            from datetime import datetime
            año_actual = datetime.now().year
            
            if año < 1900:
                raise ValidationError('El año no puede ser menor a 1900.')
            
            if año > año_actual + 1:
                raise ValidationError(f'El año no puede ser mayor a {año_actual + 1}.')
        
        return año

class RegistroAccesoForm(forms.ModelForm):
    class Meta:
        model = RegistroAcceso
        fields = ['vehiculo', 'tipo_movimiento', 'observaciones']
        widgets = {
            'vehiculo': forms.Select(attrs={
                'class': 'form-control form-select',
                'required': True
            }),
            'tipo_movimiento': forms.Select(attrs={
                'class': 'form-control form-select',
                'required': True
            }),
            'observaciones': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Observaciones del registro (opcional)'
            })
        }

class BusquedaForm(forms.Form):
    busqueda = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Buscar por placa, nombre, documento...',
            'autocomplete': 'off'
        })
    )

class FiltroReporteForm(forms.Form):
    fecha_inicio = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        }),
        label='Fecha de inicio'
    )
    
    fecha_fin = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        }),
        label='Fecha de fin'
    )
    
    tipo_movimiento = forms.ChoiceField(
        choices=RegistroAcceso.TIPO_MOVIMIENTO_CHOICES,
        widget=forms.RadioSelect(attrs={
            'class': 'form-check-input'
        }),
        label='Tipo de movimiento'
    )
    
    observaciones = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 2,
            'placeholder': 'Observaciones adicionales (opcional)'
        }),
        label='Observaciones'
    )
    
    def clean_placa(self):
        placa = self.cleaned_data['placa'].upper().strip()
        
        if not placa:
            raise ValidationError('La placa es requerida.')
            
        # Verificar que el vehículo existe y está activo
        try:
            vehiculo = Vehiculo.objects.get(placa=placa, activo=True)
        except Vehiculo.DoesNotExist:
            raise ValidationError(f'No se encontró un vehículo activo con placa {placa}.')
        
        return placachoices=[
            ('', 'Todos los movimientos'),
            ('ENTRADA', 'Solo entradas'),
            ('SALIDA', 'Solo salidas')
        ],
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-control form-select'
        }),
        label='Tipo de movimiento'
    )
    
    tipo_vehiculo = forms.ChoiceField(
        choices=[('', 'Todos los vehículos')] + Vehiculo.TIPO_VEHICULO_CHOICES,
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-control form-select'
        }),
        label='Tipo de vehículo'
    )

class RegistroRapidoForm(forms.Form):
    """Formulario simplificado para registro rápido de acceso"""
    placa = forms.CharField(
        max_length=10,
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'Ingrese placa del vehículo',
            'style': 'text-transform: uppercase;',
            'autocomplete': 'off',
            'autofocus': True
        }),
        label='Placa del vehículo'
    )
    
    tipo_movimiento = forms.ChoiceField(