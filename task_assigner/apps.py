from django.apps import AppConfig


class TaskAssignerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'task_assigner'

    def ready(self):
        pass
