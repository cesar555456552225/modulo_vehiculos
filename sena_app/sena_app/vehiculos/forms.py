from django import forms
from django.core.exceptions import ValidationError
import re

from .models import Vehiculo, Instructor, RegistroAcceso

class VehiculoForm(forms.Form):
    tipo_vehiculo = forms.ChoiceField( label="Tipo de vehículo", choices=Vehiculo.TIPO_VEHICULO_CHOICES, required=True)
    placa =  forms.CharField(max_length=7)
    color =  forms.ChoiceField(label="Color del vehículo", choices=Vehiculo.COLOR_VEHICULO_CHOICES, required=True)
    marca =  forms.CharField(max_length=10, label="Marca del vehículo", required=False)
    propietario =  forms.ModelChoiceField(queryset=Instructor.objects.all(), label="Propietario del vehículo (Instructor)")
    activo =  forms.BooleanField(required=False, initial=True, label="Activo")
    fecha_registro =  forms.DateTimeField(widget=forms.HiddenInput(), required=False)
    observaciones =  forms.CharField(widget=forms.Textarea(attrs={'rows': 3, 'cols': 30}),label="observaciones en el vehículo", required=False)

    def clean(self):
        cleaned_data = super().clean()
        placa = cleaned_data.get('placa')
        propietario = cleaned_data.get('propietario')
        if not placa or not propietario:
            raise forms.ValidationError("Los campos placa y propietario son obligatorios.")
        return super().clean()
    
    def save(self):
        try:
            vehiculo = Vehiculo.objects.create(
                tipo_vehiculo=self.cleaned_data['tipo_vehiculo'],
                placa=self.cleaned_data['placa'],
                color=self.cleaned_data['color'],
                marca=self.cleaned_data['marca'],
                propietario=self.cleaned_data['propietario'],
                activo=self.cleaned_data['activo'],
                observaciones=self.cleaned_data['observaciones'],
            )
            return vehiculo
        except Exception as e:
            raise forms.ValidationError(f"Error al crear el vehículo: {str(e)}"
            )