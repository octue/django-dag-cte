import logging
from django.db import models
from django.db.models import AutoField


logger = logging.getLogger(__name__)

# TODO implement the recursive view for closure and ancestry
# from .fields import ClosureManyToManyField
# from django_dag_cte.exceptions import CircularReference


class AbstractNode(models.Model):

    node_id = AutoField(primary_key=True)

    # Parents-Children relationship (the `children` strand) using a Directed Acyclic Graph
    parents = models.ManyToManyField('self', related_name='children', symmetrical=False, blank=True)

    # TODO implement the recursive view for closure and ancestry
    # Note this creates an unmanaged `*Closure` table which is a table view, unmanaged by Django.
    # descendants = ClosureManyToManyField('self', related_name='ancestors', symmetrical=False)

    # objects = CTEManager()

    class Meta:
        abstract = True

    def __str__(self):
        """ Allows representation in django admin
        """
        return 'Node {id}'.format(id=self.node_id)

    def add_child(self, child_node):  # pragma: no cover
        """ Adds a child to the node
        """
        return child_node.parents.add(self)

    def add_parent(self, parent_node):  # pragma: no cover
        """ Adds a child to the node
        """
        return self.parents.add(parent_node)

    def delete(self, *args, **kwargs):
        """Removes a node and all it's descendants."""
        self.__class__.objects.filter(node_id=self.node_id).delete()

    def get_ancestors(self):  # pragma: no cover
        """
        :returns:
            A queryset containing the current node object's ancestors,
            starting by the root node and descending to the parent.
            (some subclasses may return a list)
        """
        raise NotImplementedError

    def get_descendants(self):  # pragma: no cover
        """ Returns a queryset of all the node's descendants
        Doesn't include the node itself
        """
        raise NotImplementedError

    @classmethod
    def get_child_nodes(self):
        """ Returns a queryset of all nodes which are children
        TODO refactor to a chainable manager method (eg MyModel.objects.is_child....)
        """
        return self.objects.exclude(parents=None)

    @classmethod
    def get_leaf_nodes(cls):
        """ Returns queryset filtered to leaf nodes only
        TODO refactor to a chainable manager method (eg MyModel.objects.is_leaf...)
        """
        return cls.objects.filter(children=None)

    @classmethod
    def get_parent_nodes(self):
        """ Returns a queryset of parent nodes
        TODO refactor to a chainable manager method (eg MyModel.objects.is_parent...)
        """
        return self.objects.exclude(children=None)

    @classmethod
    def get_root_nodes(cls):
        """
        TODO refactor to a chainable manager method (eg MyModel.objects.is_root...)
        :returns: A queryset filtered to root nodes only
        """
        return cls.objects.filter(parents=None)

    def get_roots(self):  # pragma: no cover
        """ Returns the root nodes for the current node object
        """
        raise NotImplementedError

    def is_child_of(self, node):
        """ Verify if one node is a child of another
        :param node: The node that will be checked as a parent
        :returns: ``True`` if the node is a child of another node given as an argument, else, returns ``False``
        """
        return node.children.filter(node_id=self.node_id).exists()

    def is_descendant_of(self, node):  # pragma: no cover
        """
        :returns: ``True`` if the node is a descendant of another node given
            as an argument, else, returns ``False``
        :param node:
            The node that will be checked as an ancestor
        """
        raise NotImplementedError

    def is_leaf(self):
        """:returns: True if the node is a leaf node (else, returns False)"""
        return not self.children.exists()

    def is_parent_of(self, node):
        """
        :returns: ``True`` if the node is a child of another node given as an
            argument, else, returns ``False``
        :param node:
            The node that will be checked as a parent
        """
        return node.parents.filter(node_id=self.node_id).exists()

    def is_root(self):  # pragma: no cover
        """:returns: True if the node is a root node (else, returns False)"""
        return NotImplementedError
