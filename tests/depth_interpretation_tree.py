from mock import patch
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
    @patch('regs.depth.interpretation.tree.applicable_tree')
    @patch('regs.depth.interpretation.tree.carving.applicable_offsets')
    def test_section_tree_with_subs(self, applicable_offsets, applicable_tree):
        title = "Section 105.11 This is a section title"
        body = "Body of the interpretation's section"
        non_title = "\n" + body
        applicable_tree.return_value = tree.node("An interpretation")   # sub tree
        applicable_offsets.return_value = [(2,5), (5,8), (10, 12)]
        result = section_tree(title + non_title, 105, tree.label("abcd"))
        self.assertEqual(non_title[:2], result['text'])
        self.assertEqual("abcd-11", result['label']['text'])
        self.assertEqual(3, len(result['children']))
        for child in result['children']:
            self.assertEqual(applicable_tree.return_value, child)
    def test_section_tree_no_children(self):
        title = "Section 105.11 This is a section title"
        body = "Body of the interpretation's section"
        non_title = "\n" + body
        result = section_tree(title + non_title, 105, tree.label("abcd"))
        self.assertEqual(non_title, result['text'])
        self.assertEqual("abcd-11", result['label']['text'])
        self.assertEqual(0, len(result['children']))
    def test_build_with_subs(self):
        text = "Something here\nSection 100.22\nmore more\nSection 100.5\nand more"
        result = build(text, 100)
        self.assertEqual("Something here\n", result['text'])
        self.assertEqual("100-Interpretations", result['label']['text'])
        self.assertEqual(["100", "Interpretations"], result['label']['parts'])
        self.assertEqual("Supplement I to Part 100", result['label']['title'])
        self.assertEqual(2, len(result['children']))

        node = result['children'][0]
        self.assertEqual("\nmore more\n", node['text'])
        self.assertEqual('100-Interpretations-22', node['label']['text'])
        self.assertEqual(['100', 'Interpretations', '22'], node['label']['parts'])
        self.assertEqual(0, len(node['children']))

        node = result['children'][1]
        self.assertEqual("\nand more", node['text'])
        self.assertEqual('100-Interpretations-5', node['label']['text'])
        self.assertEqual(['100', 'Interpretations', '5'], node['label']['parts'])
        self.assertEqual(0, len(node['children']))
    def test_build_without_subs(self):
        text = "Something here\nAnd then more\nSome more\nAnd yet another line"
        result = build(text, 100)
        self.assertEqual(text, result['text'])
        self.assertEqual("100-Interpretations", result['label']['text'])
        self.assertEqual(["100", "Interpretations"], result['label']['parts'])
        self.assertEqual("Supplement I to Part 100", result['label']['title'])
        self.assertEqual(0, len(result['children']))
    def test_section_tree_label(self):
        """The section tree should include the section header as label"""
        title = "Section 105.11 This is a section title"
        body = "Body of the interpretation's section"
        non_title = "\n" + body
        result = section_tree(title + non_title, 105, tree.label("abcd"))
        self.assertTrue('title' in result['label'])
        self.assertEqual(title, result['label']['title'])
