# vehiculos/urls.py
from django import views
from django.urls import path
from . import views
from .views import VehiculoFormView

app_name = 'vehiculos'

urlpatterns = [
    path('', views.main, name='main'),
    path('vehiculos/', views.vehiculos, name='lista_vehiculos'), 
    #path('crear_vehiculo/', views.vehiculos, name='crear_vehiculo'), 
    path('crear_vehiculo/', views.crear_vehiculo, name='crear_vehiculo'),
    path('vehiculos/<int:pk>/', views.detalle_vehiculo, name='detalle_vehiculo'), 
    path('vehiculos/<int:pk>/editar/', views.editar_vehiculo, name='editar_vehiculo'), 
    # path('vehiculos/<int:pk>/editar/', views.VehiculoFormView.as_view(), name='editar_vehiculo'),
    
    # control de acceso
    #path('acceso/', views.registro_acceso, name='registro_acceso'),
    #path('buscar_vehiculo/', views.buscar_vehiculo_ajax, name='buscar_vehiculo_ajax'),

    # reportes
    #path('reportes/', views.reportes, name='reportes'), # Eliminé el espacio extra en el nombre
]