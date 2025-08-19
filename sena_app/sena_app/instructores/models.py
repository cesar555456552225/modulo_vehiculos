from django.db import models

# Create your models here.

class Instructor(models.Model):
    TIPO_DOCUMENTO_CHOICES = [
        ('CC','cedula de ciudania'),
        ('CE', 'cedula de extranjeria'),
        ('TI', 'Tarjeta de identidad'),
        ('PAS','pasaporte'),
    ]

    NIVEL_EDUCATIVO_CHOICES = [
        ('TEC','Tecnico'),
        ('TGL', 'Tecnologo'),
        ('PRE', 'Pregrado'),
        ('ESP', 'Especialización'),
        ('MAE', 'Maestria'),
        ('DOC', 'Doctorado'),
    ]

    documento_identidad = models.CharField(max_length=20, unique = True)
    tipo_documento = models.CharField(max_length=3, choices=TIPO_DOCUMENTO_CHOICES, default='CC')
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    telefono = models.CharField(max_length=15)
    correo = models.EmailField(max_length=50)
    fecha_nacimiento = models.DateField(null=True)
    ciudad = models.CharField(max_length=50)
    direccion = models.CharField(max_length=30, null=True)
    nivel_educativo = models.CharField(max_length=3, choices=NIVEL_EDUCATIVO_CHOICES, default='MAE')
    especialidad = models.CharField(max_length=50)
    años_experiencia = models.CharField(max_length=4)
    activo = models.BooleanField(default=True)
    fecha_vinculacion = models.DateField(null=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"
    
    def nombre_instructor (self):
        return f"{self.nombre} {self.apellido}"

