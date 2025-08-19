from django import forms
from .models import Aprendiz


class AprendizForm(forms.Form):
    documento_identidad = forms.CharField(max_length=255)
    nombres = forms.CharField(max_length=255)
    apellido = forms.CharField(max_length=255)
    telefono = forms.CharField(max_length=15)
    correo = forms.EmailField(max_length=225)
    fecha_nacimiento = forms.DateField( widget=forms.DateInput(attrs={'type': 'date'}))
    ciudad = forms.CharField(max_length=155)
    programa = forms.CharField(max_length=255)

    def __str__(self):
        return f"{self.nombres} {self.apellido}"
    
    def nombre_aprendiz(self):
        return f"{self.nombres} {self.apellido}"
    
    def clean(self):
        cleaned_data = super().clean()
        documento = cleaned_data.get('documento_identidad')
        nombre = cleaned_data.get('nombres')
        apellido = cleaned_data.get('apellido')

        if not documento or not nombre or not apellido:
            raise forms.ValidationError("Todos los campos son obligatorios.")
        return cleaned_data
    
    def clean_documento_identidad(self):
        documento = self.cleaned_data['documento_identidad']
        if not documento.isdigit():
            raise forms.ValidationError("El documento debe contener solo números.")
        return documento

    def clean_telefono(self):
        telefono = self.cleaned_data.get('telefono')
        if telefono and not telefono.isdigit():
            raise forms.ValidationError("El teléfono debe contener solo números.")
        return telefono
    
    def save(self):
        Aprendiz.objects.create(
            documento_identidad=self.cleaned_data['documento_identidad'],
            nombres =self.cleaned_data['nombres'],
            apellido=self.cleaned_data['apellido'],
            telefono=self.cleaned_data.get('telefono'),
            correo=self.cleaned_data.get('correo'),
            fecha_nacimiento=self.cleaned_data['fecha_nacimiento'],
            ciudad=self.cleaned_data.get('ciudad'), 
            programa=self.cleaned_data.get('programa')
        )

#-----------------------------------------
"""
class Curso(forms.Form):
    ESTADO_CHOICES = [
        ('PRO', 'Programado'),
        ('INI', 'Iniciado'),
        ('EJE', 'Ejecución'),
        ('FIN', 'Finalizado'),
        ('CAN', 'Cancelado'),
        ('SUS', 'Suspendido'),
    ]

    codigo = forms.CharField(max_length=30,unique=True,verbose_name="Codiogo",)
    nombre = forms.CharField(max_length=200,verbose_name="Nombre del curso")
    programa = forms.ForeignKey('programas.Programa', on_delete=forms.CASCADE, verbose_name='Programa de formación')
    instructor_coordinador = forms.ForeignKey('instructores.Instructor',on_delete=forms.CASCADE,related_name='cursos_coordinador',verbose_name="Instructor coordinador")
    instructores = forms.ManyToManyField('instructores.Instructor',through='InstructorCurso', related_name='cursos_impartidos', verbose_name='Instructores')
    aprendices = forms.ManyToManyField(Aprendiz,through='AprendizCurso',related_name='cursos',verbose_name='Aprendices')
    fecha_inicio= forms.DateField(verbose_name="Fecha de inicio")
    fecha_fin = forms.DateField(verbose_name="Fecha de finalización")
    horario = forms.CharField(max_length=100, verbose_name="Horario")
    aula = forms.CharField(max_length=50, verbose_name="Aula/Ambiente")
    cupos_maximos = forms.PositiveBigIntegerField(verbose_name="Cupos Maximos")
    estado = forms.CharField(max_length=3, choices=ESTADO_CHOICES, default='PRO', verbose_name="Estado del curso")
    observaciones = forms.TextField(blank=True, null=True, verbose_name="Observaciones")
    fecha_registro = forms.DateField(auto_now_add=True, verbose_name="Fecha de registro")

    class Meta:
        verbose_name = "Curso"
        verbose_name_plural = "Cursos"
        ordering = ['-fecha_inicio']

    def cupos_disponibles(self):
        return self.cupos_maximos - self.aprendices.count()

    def porcentaje_ocupacion(self):
        if self.cupos_maximos > 0:
            return (self.aprendices.count() / self.cupos_maximos) * 100
        return 0
    
    def __str__(self):
        return f"{self.nombre}"

class InstructorCurso(forms.Form):
    instructor = forms.ForeignKey('instructores.Instructor', on_delete=forms.CASCADE)
    curso = forms.ForeignKey(Curso, on_delete=forms.CASCADE)
    rol = forms.CharField(max_length=100, verbose_name="Rol en el curso")
    fecha_asignacion = forms.DateField(auto_now_add=True, verbose_name="Fecha de asignación")

    def __str__(self):
        return f"{self.instructor} - {self.curso} ({self.rol})"

    class Meta:
        verbose_name = "Instructor por curso"
        verbose_name_plural = "Instructores por curso"
        unique_together = ['instructor', 'curso']

class AprendizCurso(forms.Form):
    ESTADO_CHOICES = [
        ('INS', 'Inscrito'),
        ('ACT', 'Activo'),
        ('DES', 'Desertor'),
        ('GRA', 'Graduado'),
        ('SUS', 'Suspendido'),
    ]

    aprendiz = forms.ForeignKey(Aprendiz, on_delete=forms.CASCADE)
    curso = forms.ForeignKey(Curso, on_delete=forms.CASCADE)
    fecha_inscripcion = forms.DateField(auto_now_add=True, verbose_name="Fecha de inscripción")
    estado = forms.CharField(max_length=3, choices=ESTADO_CHOICES, default='INS', verbose_name="Estado ene el curso")
    nota_final = forms.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True, verbose_name="Nota final")
    observaciones = forms.TextField(blank=True, null=True, verbose_name="Observaciones")

    def __str__(self):
        return f"{self.aprendiz} - {self.curso} ({self.estado})"
    
    class Meta:
        verbose_name= "Aprendiz por curso"
        verbose_name_plural = "Aprendices por curso"
        unique_together = ['aprendiz','curso']
        """