
from django.db.models import CharField
from django_dag_cte.models import AbstractNode


class Node(AbstractNode):
    """
    Test node, adds just one field
    """
    name = CharField(max_length=32)

    class Meta:
        app_label = 'tests'

    def __str__(self):
        # Ensures that the abstract class __str__ method is covered in testing
        return super(Node, self).__str__() + ' ("{}")'.format(self.name)
