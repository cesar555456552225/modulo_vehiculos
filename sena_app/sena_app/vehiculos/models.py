from django.db import models
from instructores.models import Instructor
# Create your models here.

class Vehiculo(models.Model):
    TIPO_VEHICULO_CHOICES = [
        ('CAR', 'Carro'),
        ('MOT', 'Moto'),
        ('OTRO', 'Otro'),
    ]

    COLOR_VEHICULO_CHOICES = [
        ('NEGRO','Negro'),
        ('AZUL','Azul'),
        ('GRIS','Gris'),
        ('BLANCO','Blanco'),
        ('ROJO','Rojo'),
        ('OTRO', 'Otro')
    ]

    tipo_vehiculo = models.CharField(max_length=4, choices=TIPO_VEHICULO_CHOICES, verbose_name="Tipo de vehículo" )
    placa = models.CharField(max_length=7, unique=True)
    color = models.CharField(max_length=10, choices=COLOR_VEHICULO_CHOICES)
    marca = models.CharField(max_length=10, verbose_name="Marca del vehículo", null=True)
    propietario = models.ForeignKey(Instructor, verbose_name="Propietario del vehículo (Instructor)", on_delete=models.CASCADE)
    activo = models.BooleanField(default=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    observaciones = models.TextField(verbose_name="observaciones en el vehículo", null=True)

    def __str__(self):
        return f"{self.placa}-{self.Instructor.nombre}"
    
    def esta_dentro(self):
        ultimo_registro = self.registros_acceso.order_by('-fecha_hora').first()
        return ultimo_registro and ultimo_registro.tipo_movimiento == 'ENTRADA'
    
    class Meta:
        verbose_name = "Vehículo"
        verbose_name_plural = "Vehículos"
        ordering = ['placa']

class RegistroAcceso(models.Model):
    TIPO_MOVIMIENTO_CHOICES = [
        ('ENTRADA', 'Entrada'),
        ('SALIDA', 'Salida'),
    ]

    vehiculo =  models.ForeignKey(Vehiculo, on_delete=models.CASCADE, related_name='registros_acceso')
    tipo_movimiento = models.CharField(max_length=7, choices=TIPO_MOVIMIENTO_CHOICES, verbose_name="Tipo de movimiento")
    fecha_hora = models.DateTimeField(auto_now_add=True, verbose_name="Fecha y hora del registro")
    observaciones = models.TextField(verbose_name="Observaciones del registro", null=True)

    def __str__(self):
        return f"{self.vehiculo.placa} - {self.tipo_movimiento} - {self.fecha_hora.strftime('%Y-%m-%d %H:%M:%S')}"
    
    class Meta:
        verbose_name = "Registro de Acceso"
        verbose_name_plural = "Registros de Acceso"
        ordering = ['-fecha_hora']
    

class ConfiguracionSistema(models.Model):
    centro_formacion = models.CharField(max_length=100, verbose_name="Centro de Formación")
    dierccion = models.CharField(max_length=200, verbose_name="Dirección del Centro de Formación")
    horario_funcionamiento = models.CharField(max_length=100, verbose_name="Horario de Funcionamiento")

    def __str__(self):
        return f"Configuración del Sistema - {self.centro_formacion}"
    
    class Meta:
        verbose_name = "Configuración del Sistema"
        verbose_name_plural = "Configuraciones del Sistema"
        ordering = ['centro_formacion']

