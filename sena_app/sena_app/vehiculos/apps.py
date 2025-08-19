from django.apps import AppConfig

class VehiculosConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'vehiculos'
    verbose_name = 'Control Vehicular'
    
    def ready(self):
        """
        Configuración que se ejecuta cuando la aplicación está lista
        """
        # Importar señales si las tienes
        try:
            import vehiculos.signals
        except ImportError:
            pass