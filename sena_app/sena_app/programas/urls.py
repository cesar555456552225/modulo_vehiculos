from django.urls import path
from . import views 
from .views import ProgramaFormView

urlpatterns = [
    path('', views.main, name='main'),
    path('programas/', views.programas, name='programas'),
    path('crear_programa/', ProgramaFormView.as_view(), name='crear_programa'),
]