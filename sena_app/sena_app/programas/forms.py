from django import forms
from .models import Programa

class ProgramaForm(forms.Form):
    codigo = forms.CharField(max_length=20, required=True)
    nombre = forms.CharField(max_length=100,)
    nivel_formacion = forms.ChoiceField( choices=Programa.NIVEL_FORMACION_CHOICES)
    modalidad = forms.ChoiceField( choices=Programa.MODALIDAD_CHOICES)
    duracion_meses = forms.IntegerField(label="duracion en meses")
    duracion_horas = forms.IntegerField(label="Duarcion  en horas")
    descripcion = forms.CharField(label="Descripcion del programa", widget=forms.Textarea)
    competencias = forms.CharField(label="Competencias del programa")
    perfil_egreso = forms.CharField(label="Perfil de egreso")
    requisitos_ingreso = forms.CharField(label="requisistos para entrar al programa")
    centro_formacion = forms.CharField(max_length=200)
    regional = forms.CharField(max_length=100)
    estado = forms.ChoiceField( choices=Programa.ESTADO_CHOICES, initial='ACT')
    fecha_creacion = forms.DateField(label="fecha de creacion del programa")
    fecha_registro = forms.DateField(label="fecha de registro")

    def clean(self):
        cleaned_data = super().clean()
        codigo = cleaned_data.get('codigo')
        nombre = cleaned_data.get('nombre')
        nivel_formacion = cleaned_data.get('nivel_formacion')

        if not codigo or not nombre or not nivel_formacion:
            raise forms.ValidationError("Todos los datos deben ser obligatorios.")
        return cleaned_data
    
    def clean_codigo(self):
        codigo = self.cleaned_data['codigo']
        if not codigo.isdigit():
            raise forms.ValidationError("El codigo debe tener solo numeros")
        return codigo
    
    def save(self):
        try:
            programa = Programa.objects.create(
                codigo=self.cleaned_data['codigo'],
                nombre=self.cleaned_data['nombre'],
                nivel_formacion=self.cleaned_data['nivel_formacion'],
                modalidad=self.cleaned_data['modalidad'],
                duracion_meses=self.cleaned_data['duracion_meses'],
                duracion_horas=self.cleaned_data['duracion_horas'],
                descripcion=self.cleaned_data['descripcion'],
                competencias=self.cleaned_data['competencias'],
                perfil_egreso=self.cleaned_data['perfil_egreso'],
                requisitos_ingreso=self.cleaned_data['requisitos_ingreso'],
                centro_formacion=self.cleaned_data['centro_formacion'],
                regional=self.cleaned_data['regional'],
                estado=self.cleaned_data['estado'],
                fecha_creacion=self.cleaned_data['fecha_creacion'],
                fecha_registro=self.cleaned_data['fecha_registro'],
            )
            return programa
        except Exception as e:
            raise forms.ValidationError(f"Error al crear el programa: {str(e)}")