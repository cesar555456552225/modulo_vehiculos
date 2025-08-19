from django.db import models

# Create your models here.

class Programa(models.Model):
    NIVEL_FORMACION_CHOICES =[
        ('AUX', 'Auxiliar'),
        ('OPE', 'Operario'),
        ('TEC', 'Tecnico'),
        ('TGL', 'Tecnologo'),
        ('ESP', 'Especializacion tecnologica'),
        ('COM', 'Complementario'),
    ]

    MODALIDAD_CHOICES = [
        ('PRE', 'Presencial'),
        ('VIR', 'Virtual'),
        ('MIX', 'Mixta'),
    ]

    ESTADO_CHOICES =[
        ('ACT', 'Activo'),
        ('INA', 'Inactivo'),
        ('SUS', 'Suspendido'),
        ('CAN', 'Cancelado'),
    ]

    codigo = models.CharField(max_length=20, unique=True)
    nombre = models.CharField(max_length=100,)
    nivel_formacion = models.CharField(max_length=3, choices=NIVEL_FORMACION_CHOICES)
    modalidad = models.CharField(max_length=3, choices=MODALIDAD_CHOICES)
    duracion_meses = models.PositiveIntegerField(verbose_name="duracion en meses")
    duracion_horas = models.PositiveIntegerField(verbose_name="Duarcion  en horas")
    descripcion = models.TextField(verbose_name="Descripcion del programa")
    competencias = models.TextField(verbose_name="Competencias del programa")
    perfil_egreso = models.TextField(verbose_name="Perfil de egreso")
    requisitos_ingreso = models.TextField(verbose_name="requisistos para entrar al programa")
    centro_formacion = models.CharField(max_length=200)
    regional = models.CharField(max_length=100)
    estado = models.CharField(max_length=3, choices=ESTADO_CHOICES, default='ACT')
    fecha_creacion = models.DateField(verbose_name="fecha de creacion del programa")
    fecha_registro = models.DateField(verbose_name="fecha de registro")

    def __str__(self):
        return f"{self.codigo} {self.nombre}"
    
    def get_duracion_completa(self):
        return f"{self.duracion_meses} meses, {self.duracion_horas} horas"
    
    def is_activo(self):
        return self.estado == 'ACT'