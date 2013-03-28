from mock import patch
from regs.depth import tree
from regs.layers.interpretation import *
from unittest import TestCase

class EmptyClass: pass

class LayersInterpretationTest(TestCase):
    def header(self, p1):
        h = EmptyClass()
        h.keyterm = ""
        h.whole = ""
        paragraph1 = EmptyClass()
        paragraph1.id = p1
        h.paragraph1 = paragraph1
        h.paragraph2 = ""
        h.paragraph3 = ""
        h.paragraph4 = ""
        return h

    @patch('regs.layers.interpretation.carving.applicable_paragraph')
    def test_add_to_layer(self, applicable_paragraph):
        applicable_paragraph.return_value = self.header(p1='a')
        layer = {}
        node = tree.node(label=tree.label("some_section", [None]*3, "Title"))
        add_to_layer("", node, layer)

        self.assertTrue('(a)' in layer)
        self.assertTrue('interpretation' in layer['(a)'])
        self.assertFalse('keyterms' in layer['(a)'])
        self.assertEqual("some_section", layer['(a)']['interpretation'])

        applicable_paragraph.return_value = self.header(p1='p1p1p1')
        node = tree.node(label=tree.label("other", [None]*3, "Title"))
        add_to_layer("", node, layer)

        self.assertTrue('(a)' in layer)
        self.assertTrue('interpretation' in layer['(a)'])
        self.assertFalse('keyterms' in layer['(a)'])
        self.assertEqual("some_section", layer['(a)']['interpretation'])
        self.assertTrue('(p1p1p1)' in layer)
        self.assertTrue('interpretation' in layer['(p1p1p1)'])
        self.assertFalse('keyterms' in layer['(p1p1p1)'])
        self.assertEqual("other", layer['(p1p1p1)']['interpretation'])
    def test_build_element_interp(self):
        match = self.header('a')
        el = build_element(match, "Some thing here")
        self.assertTrue('interpretation' in el)
        self.assertFalse('keyterms' in el)
        self.assertEqual('Some thing here', el['interpretation'])
    def test_build_element_keyterm(self):
        match = self.header('a')
        match.keyterm = EmptyClass()
        match.keyterm.term = 'Awesome KeyTerm'
        el = build_element(match, 'Some Interp')
        self.assertFalse('interpretation' in el)
        self.assertTrue('keyterms' in el)
        self.assertEqual([(match.keyterm.term, 'Some Interp')], el['keyterms'])

        match.keyterm.term = 'keyterm_here'
        el = build_element(match, 'some_interp', el)
        self.assertFalse('interpretation' in el)
        self.assertTrue('keyterms' in el)
        self.assertEqual([
            ('Awesome KeyTerm', 'Some Interp'), (match.keyterm.term, 'some_interp')
            ], el['keyterms'])
    def test_build_element_ontop(self):
        match = self.header('a')
        el = {'keyterms': [('a', 'b')]}
        el = build_element(match, "Some thing here", el)
        self.assertTrue('interpretation' in el)
        self.assertTrue('keyterms' in el)
        self.assertEqual('Some thing here', el['interpretation'])
        self.assertEqual([('a', 'b')], el['keyterms'])
    @patch('regs.layers.interpretation.add_to_layer')
    def test_build(self, add_to_layer):
        interp1 = tree.node("Message", label=tree.label(parts=['a', 'b', 'i', '1']))
        interp2 = tree.node("Other", label=tree.label(parts=['b', 'b', 'h', '3']))
        interp3 = tree.node("\n", children=[tree.node()], 
                label=tree.label(parts=['c', 'b', 'g', '4']))
        interp4 = tree.node("Some Content", children=[tree.node()], 
                label=tree.label(parts=['d', 'b', 'f', '4']))
        root = tree.node("Start of Supplement", children = [
            tree.node("Section 1", children = [
                interp1,
                tree.node("\n\n", label=tree.label(parts=['a', 'b', 'c', '2'])),
                interp2
                ]),
            tree.node("Section 3", children = [interp3]),
            tree.node("Section 5", children = [
                tree.node("\n\n", label=tree.label(parts=['a', 'b', 'c', '2'])),
                interp4
                ])
            ])
        layer = build(root, 201)
        self.assertEqual(["a.i", "b.h", "c.g", "d.f"], 
                [args[0] for args,_ in add_to_layer.call_args_list])
        self.assertEqual([interp1, interp2, interp3, interp4],
                [args[1] for args,_ in add_to_layer.call_args_list])
