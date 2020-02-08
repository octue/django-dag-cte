from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class DjangoDagCteTestAppConfig(AppConfig):
    name = 'tests'
    label = 'tests'
    verbose_name = _('Directed Acyclic Graph Test App')
