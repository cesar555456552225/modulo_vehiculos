from django import forms
from .models import Instructor


# Create your models here.

class InstructorForm(forms.Form):

    documento_identidad = forms.CharField(max_length=20)
    tipo_documento = forms.ChoiceField( choices=Instructor.TIPO_DOCUMENTO_CHOICES, initial='CC')
    nombre = forms.CharField(max_length=100)
    apellido = forms.CharField(max_length=100)
    telefono = forms.CharField(max_length=15)
    correo = forms.EmailField(max_length=50)
    fecha_nacimiento = forms.DateField(required=True)
    ciudad = forms.CharField(max_length=50)
    direccion = forms.CharField(max_length=30, required=True)
    nivel_educativo = forms.ChoiceField( choices=Instructor.NIVEL_EDUCATIVO_CHOICES, initial='MAE')
    especialidad = forms.CharField(max_length=50)
    años_experiencia = forms.CharField(max_length=4)
    activo = forms.BooleanField(required=True)
    fecha_vinculacion = forms.DateField(required=True)
    fecha_registro = forms.DateField(label='fecha de registro', help_text='Ingrese la fecha de registro')

    def clean(self):
        cleaned_data = super().clean()
        documento = cleaned_data.get('documento_identidad')
        nombre = cleaned_data.get('nombre')
        apellido = cleaned_data.get('apellido')

        if not documento or not nombre or not apellido:
            raise forms.ValidationError("Todos los campos son obligatorios.")

        return cleaned_data

    def clean_documento_identidad(self):
        documento = self.cleaned_data['documento_identidad']
        if not documento.isdigit():
            raise forms.ValidationError("El documento debe contener solo números.")
        return documento
        
        
    def save(self):
        """Método para guardar el instructor en la base de datos"""
        try:
            instructor = Instructor.objects.create(
                documento_identidad=self.cleaned_data['documento_identidad'],
                tipo_documento=self.cleaned_data['tipo_documento'],
                nombre=self.cleaned_data['nombre'],
                apellido=self.cleaned_data['apellido'],
                telefono=self.cleaned_data.get('telefono', ''),
                correo=self.cleaned_data.get('correo', ''),
                fecha_nacimiento=self.cleaned_data['fecha_nacimiento'],
                ciudad=self.cleaned_data.get('ciudad', ''),
                direccion=self.cleaned_data.get('direccion', ''),
                nivel_educativo=self.cleaned_data['nivel_educativo'],
                especialidad=self.cleaned_data['especialidad'],
                años_experiencia=self.cleaned_data['años_experiencia'],
                activo=self.cleaned_data.get('activo', True),
                fecha_vinculacion=self.cleaned_data['fecha_vinculacion'],
            )
            return instructor
        except Exception as e:
            raise forms.ValidationError(f"Error al crear el instructor: {str(e)}")