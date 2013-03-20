import re
from regs.interpretation.layer import *
from unittest import TestCase

class EmptyClass: pass

class InterpretationLayer(TestCase):
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
        
    def test_add_to_layer_no_title(self):
        chunk_pairs = [
                (self.header('a'), "Something\nhere goes"), 
                (self.header('b'), "somewhere else\ndoesn't it"), 
                (self.header('c'), "now\nthen?")
            ]

        layer = {}
        add_to_layer("", chunk_pairs, layer)
        interp = lambda txt: {"interpretation": txt}
        self.assertEqual(interp("\nhere goes"), layer['(a)'])
        self.assertEqual(interp("\ndoesn't it"), layer['(b)'])
        self.assertEqual(interp("\nthen?"), layer['(c)'])
    def test_add_to_layer_no_empty(self):
        chunk_pairs = [(self.header('a'), "Something\n\n")]

        layer = {}
        add_to_layer("", chunk_pairs, layer)
        self.assertEqual({}, layer)
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
    def test_build_label_immutable(self):
        label = "Some label"
        build_label(label, self.header('a'))
        self.assertEqual("Some label", label)
    def test_build_label_p_depth(self):
        prefix = "104.22"
        self.assertEqual(prefix + "(a)", build_label(prefix, self.header('a')))

        match = self.header('b')
        match.paragraph2 = EmptyClass()
        match.paragraph2.id = '3'
        self.assertEqual(prefix + "(b)(3)", build_label(prefix, match))

        match.paragraph3 = EmptyClass()
        match.paragraph3.id = 'iv'
        match.paragraph4 = EmptyClass()
        match.paragraph4.id = 'E'
        self.assertEqual(prefix + "(b)(3)(iv)(E)", build_label(prefix, match))
    def test_build(self):
        p_5_a_5_iii = "Paragraph 5(a)(5)(iii)\nSome content here\n\n"
        p_5_d = "5(d) Keyterms go here\n\nFollowed by\nsome defintiions"
        text = "Paragraph Bad\n" + p_5_a_5_iii + p_5_d
        s201 = "Section 201.5\n" + text + "\nSection 201.8\n\n"
        layer = build(s201, 201)
        self.assertTrue('201.5(a)(5)(iii)' in layer)
        self.assertTrue('interpretation' in layer['201.5(a)(5)(iii)'])
        self.assertTrue('201.5(d)' in layer)
        self.assertTrue('keyterms' in layer['201.5(d)'])
