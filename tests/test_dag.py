from django.test import TestCase

from tests.models import Node


class DagTestCase(TestCase):

    def test_basic_network(self):
        """ Ensures that we can create a Directed Acyclic Graph of Twins, with no particular path or level information

                                                     (n0)                < Top level nodes (leaves) aren't always at the same level
                                                       |
                                                       |
                                                     (n1)        (n2)
                                                       |        /  |
                                                       |      /    |
                                                       |    /      |
                                                       |  /        |
          A node can have more than one parent >     (n3)        (n4)       < A node can have multiple children
                                                       |  \     /  | \
                                                       |    \ /    |  \
                      Nodes can share children >       |    /  \   |   \
                                                       |  /      \ |    \
                A node can have a single child >     (n5)        (n6)  (n7)     < Bottom level nodes (roots) aren't always at the same level
                                                       |
                                                       |
                                                     (n8)
        """  # noqa: W605

        # Create the nodes
        n0 = Node(name='n0')
        n1 = Node(name='n1')
        n2 = Node(name='n2')
        n3 = Node(name='n3')
        n4 = Node(name='n4')
        n5 = Node(name='n5')
        n6 = Node(name='n6')
        n7 = Node(name='n7')
        n8 = Node(name='n8')
        n0.save()
        n1.save()
        n2.save()
        n3.save()
        n4.save()
        n5.save()
        n6.save()
        n7.save()
        n8.save()

        # Assemble the network
        n8.parents.add(n5)
        n7.parents.add(n4)
        n6.parents.add(n3, n4)
        n5.parents.add(n3, n4)
        n4.parents.add(n2)
        n3.parents.add(n1, n2)
        n1.parents.add(n0)

        # Ensure a node name can be printed
        str(n0)

        # Check leaves are correct
        leaves = [node.node_id for node in Node.get_leaf_nodes().all()]
        self.assertEqual(len(leaves), 3)
        self.assertIn(n6.node_id, leaves)
        self.assertIn(n7.node_id, leaves)
        self.assertIn(n8.node_id, leaves)

        # Check roots are correct
        roots = [node.node_id for node in Node.get_root_nodes().all()]
        self.assertEqual(len(roots), 2)
        self.assertIn(n0.node_id, roots)
        self.assertIn(n2.node_id, roots)

        # Check children of various nodes
        n4_children = [node.name for node in n4.children.all()]
        self.assertEqual(len(n4_children), 3)
        self.assertIn('n5', n4_children)
        self.assertIn('n6', n4_children)
        self.assertIn('n7', n4_children)
        self.assertEqual(n2.children.count(), 2)
        self.assertEqual(n5.children.count(), 1)
        self.assertEqual(n8.children.count(), 0)

        # Delete a node in the middle of the network
        n3.delete()
        self.assertFalse(Node.objects.filter(name='n3').exists())

        # There should now be an extra leaf node, n1
        leaves = [node.node_id for node in Node.get_leaf_nodes().all()]
        self.assertEqual(len(leaves), 4)
        self.assertIn(n1.node_id, leaves)

        # Check the query for all children
        names = [node.name for node in Node.get_child_nodes().all()]
        for name in ['n1', 'n4', 'n5', 'n6', 'n7', 'n8']:
            self.assertIn(name, names)
        for name in ['n0', 'n2', 'n3']:
            self.assertNotIn(name, names)

        # Check the query for all parents
        names = [node.name for node in Node.get_parent_nodes().all()]
        for name in ['n0', 'n2', 'n4', 'n5']:
            self.assertIn(name, names)
        for name in ['n1', 'n3', 'n6', 'n7', 'n8']:
            self.assertNotIn(name, names)

        # Check is_child_of
        self.assertTrue(n8.is_child_of(n5))
        self.assertFalse(n8.is_child_of(n7))

        # Check is_parent_of
        self.assertTrue(n5.is_parent_of(n8))
        self.assertFalse(n7.is_parent_of(n8))

        # Check is_leaf
        self.assertTrue(n1.is_leaf())
        self.assertTrue(n8.is_leaf())
        self.assertFalse(n5.is_leaf())
