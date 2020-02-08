from django.db import models
from django.utils.translation import gettext_lazy as _


class ClosureManyToManyField(models.ManyToManyField):
    """ Pre-configured M2M that defines a 'through' model automatically for closure table of a Directed Acyclic Graph

    The `through` model has managed=False, meaning that the "table" is actually a postgres view, rather than a real
     table... ie there is no storage but it behaves like a table (hence managed=False; we don't want django issuing
     CREATE TABLE statements).

    Adapted from https://github.com/funkybob/django-closure-tree for Directional Acyclic Graph as per
     https://schinckel.net/2019/07/08/graphs-in-django-and-postgres/
    """

    def contribute_to_class(self, cls, name, **kwargs):
        if not cls._meta.abstract:
            # Define through table
            meta = type('Meta', (), {
                'db_table': '%s_closure' % cls._meta.db_table,
                'app_label': cls._meta.app_label,
                'db_tablespace': cls._meta.db_tablespace,
                'unique_together': ('ancestor', 'descendant'),
                'verbose_name': _('Ancestor-Descendant Relationship'),
                'verbose_name_plural': _('Ancestor-Descendant Relationships'),
                'apps': cls._meta.apps,
                # 'managed': False,
            })
            # Construct and set the new class.
            name_ = '%sClosure' % cls._meta.model_name.capitalize()
            self.remote_field.through = type(name_, (models.Model,), {
                'Meta': meta,
                '__module__': cls.__module__,
                'ancestor': models.ForeignKey(
                    cls,
                    related_name='%s+' % name_,
                    db_tablespace=self.db_tablespace,
                    db_constraint=self.remote_field.db_constraint,
                    on_delete=models.CASCADE,
                ),
                'descendant': models.ForeignKey(
                    cls,
                    related_name='%s+' % name_,
                    db_tablespace=self.db_tablespace,
                    db_constraint=self.remote_field.db_constraint,
                    on_delete=models.CASCADE,
                ),
            })

        super().contribute_to_class(cls, name, **kwargs)
