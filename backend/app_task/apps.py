from django.apps import AppConfig


class AppTaskConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app_task'

    def ready(self):
        import app_task.signals
