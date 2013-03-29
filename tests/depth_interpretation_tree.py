from regs.depth import tree
from regs.depth.interpretation.tree import *
from unittest import TestCase

class DepthInterpretationTreeTest(TestCase):
    def test_applicable_tree(self):
        title = "Paragraph 3(b)"
        depth1 = "1. Inline depth and then\n"
        depth2i = "i. some "
        depth2ii = "ii. sub "
        depth2iii = "iii. sections"
        depth2 = "2. Start of line with "
        text = title + "\n" + depth1 + depth2 + depth2i + depth2ii + depth2iii
        a_tree = applicable_tree(text, 3, tree.label())
        self.assertEqual(tree.label("(b)", ["(b)"], title), a_tree['label'])
        self.assertEqual("", a_tree['text'].strip())
        self.assertEqual(2, len(a_tree['children']))

        node = a_tree['children'][0]
        self.assertEqual(tree.label("(b)-1", ["(b)", "1"]), node['label'])
        self.assertEqual(depth1, node['text'])
        self.assertEqual(0, len(node['children']))

        node = a_tree['children'][1]
        self.assertEqual(tree.label("(b)-2", ["(b)", "2"]), node['label'])
        self.assertEqual(depth2, node['text'])
        self.assertEqual(3, len(node['children']))

        node = a_tree['children'][1]['children'][0]
        self.assertEqual(tree.label("(b)-2.i", ["(b)", "2", "i"]), node['label'])
        self.assertEqual(depth2i, node['text'])
        self.assertEqual(0, len(node['children']))

        node = a_tree['children'][1]['children'][1]
        self.assertEqual(tree.label("(b)-2.ii", ["(b)", "2", "ii"]), node['label'])
        self.assertEqual(depth2ii, node['text'])
        self.assertEqual(0, len(node['children']))

        node = a_tree['children'][1]['children'][2]
        self.assertEqual(tree.label("(b)-2.iii", ["(b)", "2", "iii"]), node['label'])
        self.assertEqual(depth2iii, node['text'])
        self.assertEqual(0, len(node['children']))
