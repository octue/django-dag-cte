from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class DjangoDagCteAppConfig(AppConfig):
    name = 'django_dag_cte'
    label = 'django_dag_cte'
    verbose_name = _('Directed Acyclic Graphs (DAGs)')

    def ready(self):
        from django_dag_cte.signals import register_signal_handlers
        register_signal_handlers()
