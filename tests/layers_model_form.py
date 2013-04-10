# vim: set fileencoding=utf-8 :

from mock import patch
from regs.depth import tree
from regs.layers.model_form import *
from unittest import TestCase

class LayersModelFormTest(TestCase):
    def test_model_start(self):
        text = "Code code code. Sentence number two. Third sentence"
        self.assertEqual(15, model_start(text))
        text = "This sentence has not a single period in it"
        self.assertEqual(len(text), model_start(text))
    def test_process_node_no_model(self):
        """Node does not have 'Model' in its title"""
        layer = {}
        label = tree.label(title=u'§ 100.10')
        process_node(tree.node(label=label), layer)
        self.assertEqual({}, layer)

        process_node(tree.node("Model Not In Label", label=label), layer)
        self.assertEqual({}, layer)

        test_label = dict(label)    #   copy
        test_label['parts'] = ['Model']
        process_node(tree.node(label=test_label), layer)
        self.assertEqual({}, layer)

        test_label = dict(label)    #   copy
        test_label['text'] = ['Model']
        process_node(tree.node(label=test_label), layer)
        self.assertEqual({}, layer)

        process_node(tree.node(label=label, children=[
            tree.node(label=tree.label("Model In Child"))]), layer)
        self.assertEqual({}, layer)
    def test_process_node_no_citation(self):
        """Node does not have a citation in its title"""
        layer = {}
        process_node(tree.node(label=tree.label(title="Model")), layer)
        self.assertEqual({}, layer)
    def test_process_node_no_children(self):
        """If there's no children, assume the whole text of the node is the
        form"""
        layer = {}
        content = "Testing testing testing"
        process_node(tree.node(content, label=tree.label(
            text="X", title="Model with " + u'§ 100.10')), layer)
        self.assertTrue('X' in layer)
        self.assertEqual((0, len(content)), layer['X']['offsets'][0])
    def test_process_node_with_children(self):
        """Split on the first period within the child. Everything after that
        is a model form."""
        layer = {}
        child1 = tree.node("Does not have a period or children",
                label=tree.label("c1"))
        child2 = tree.node("No period, but children", [tree.node("a")],
                label=tree.label("c2"))
        child3 = tree.node("Has a period. Then content. No children.",
                label=tree.label("c3"))
        child4 = tree.node("Has period. And Children.", [tree.node("bb")],
                label=tree.label("c4"))
        process_node(tree.node(children=[child1, child2, child3, child4],
            label=tree.label(title="Model " + u'§ 100.10')), layer)

        self.assertTrue("c1" in layer)
        self.assertEqual((len(child1['text']), len(child1['text'])),
                layer['c1']['offsets'][0])

        self.assertTrue("c2" in layer)
        self.assertEqual((len(child2['text']), len(child2['text'] + 'a')),
                layer['c2']['offsets'][0])

        self.assertTrue("c3" in layer)
        self.assertEqual((len('Has a period.'), len(child3['text'])),
                layer['c3']['offsets'][0])

        self.assertTrue("c4" in layer)
        self.assertEqual((len('Has period.'), len(child4['text'] + 'bb')),
                layer['c4']['offsets'][0])
    @patch('regs.layers.model_form.process_node')
    def test_build(self, process_node):
        """Process Node should be called on every node in the tree."""
        build(tree.node(children=[
            tree.node(children=[tree.node(), tree.node()]),
            tree.node()
            ]))
        self.assertEqual(5, process_node.call_count)
