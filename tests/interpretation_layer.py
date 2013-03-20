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
        
    def test_interpretation_layer_no_title(self):
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
    def test_interpretation_layer_no_empty(self):
        chunk_pairs = [(self.header('a'), "Something\n\n")]

        layer = {}
        add_to_layer("", chunk_pairs, layer)
        self.assertEqual({}, layer)
