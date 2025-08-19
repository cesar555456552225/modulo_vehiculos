from django.urls import path
from . import views
from .forms import VehiculoFormView

app_name = 'vehiculos'

urlpatterns = [
    path('', views.main, name ='main'),
    path('vehiculos/', views.lista_vehiculos, name='lista_vehiculos'),
    path('crear_vehiculo/', views.crear_vehiculo, name='crear_vehiculo'),
    path('vehiculos/<int:pk>/', views.detalle_vehiculo, name='detalle_veviculo'),
    path('vehiculos/<int:pk>/editar/', VehiculoFormView.as_view(), name='editar_vehiculo'),

    #control de acceso
    path('acceso/', views.registro_acceso, name='registro_acceso'),
    path('buscar_vehiculo/', views.buscar_vehiculo_ajax, name='buscar_vehiculo_ajax'),

    #reportes
    path('reportes/', views.reportes, name = 'reportes '),
]