# vim: set fileencoding=utf-8 :
from mock import patch
from regs.terms import *
from unittest import TestCase

class TermsTest(TestCase):
    def test_parse_from(self):
        #   Note, the first two are normal single quotes; the second are smart quotes
        text = u'Some "nonterm" and another "nterm" but this one “is a term”, but so is'
        text += u' “this”.'
        matches = parse_from(text)
        self.assertEqual(["is a term", "this"], matches)
    def test_children_with_defs(self):
        children = []
        def1 = tree.node(label=tree.label(title="This has a definition in it"))
        children.append(def1)
        children.append(tree.node(label=tree.label(title="This does not")))
        def2 = tree.node("This has a definition")
        children.append(def2)
        children.append(tree.node("no such def"))
        def_children = children_with_defs(tree.node(children=children))
        self.assertEqual([def1, def2], def_children)
    @patch('regs.terms.parse_from')
    def test_one_level_layer_empty(self, parse_from):
        parse_from.return_value = []
        root = tree.node(children=[tree.node("definition"), tree.node("definition"),
            tree.node("definition", children=[tree.node("definition")])])
        layer = one_level_layer(root)
        self.assertEqual({}, layer)
    @patch('regs.terms.parse_from')
    def test_one_level_layer_empty(self, parse_from):
        parse_from.return_value = ['key', 'test', 'word']
        root = tree.node(label=tree.label("A"), children = [
            tree.node("definition", label=tree.label("A1")),
            tree.node("definition", label=tree.label("A2")),
            tree.node("definition", label=tree.label("A3"), children = [
                tree.node(label=tree.label("A3i"))
                ])
            ])
        layer = one_level_layer(root)
        self.assertEqual(parse_from.return_value, sorted(layer.keys()))
        for key in layer:
            self.assertEqual('A3i', layer[key])
    @patch('regs.terms.one_level_layer')
    def test_build_layer(self, one_level_layer):
        one_level_layer.return_value = [True, False, True]
        root = tree.node(label=tree.label("A"), children = [
            tree.node(label=tree.label("A1")),
            tree.node(label=tree.label("A2")),
            tree.node(label=tree.label("A3"), children = [
                tree.node(label=tree.label("A3i"))
                ])
            ])
        layer = build_layer(root)
        self.assertEqual(5, len(layer))
        for label in ['A', 'A1', 'A2', 'A3', 'A3i']:
            self.assertTrue(label in layer)
            self.assertEqual(one_level_layer.return_value, layer[label])

