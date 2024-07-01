import contextlib

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class SchemasConfig(AppConfig):
    name = "backend.schemas"
    verbose_name = _("Schemas")

    def ready(self):
        with contextlib.suppress(ImportError):
            import backend.schemas.signals  # noqa: F401
