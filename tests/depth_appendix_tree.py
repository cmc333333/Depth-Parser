from regs.depth import tree
from regs.depth.appendix.tree import *
from unittest import TestCase

class DepthAppendixTreeTest(TestCase):
    def test_generic_tree_no_children(self):
        text = "Non title text"
        l = tree.label('Some label')
        node = generic_tree(text, l)
        self.assertEqual(tree.node(text, label=l), node)
    def test_generic_tree_with_children(self):
        start = "some text\n"
        t1 = "Title Text One"
        b1 = "\nSome body text\nsomething\nsomething\n"
        t2 = "Section Two"
        b2 = "\nSomething else\nhere"
        l = tree.label('sl', ['s', 'l'], 'Some label')
        t = generic_tree(start + t1 + b1 + t2 + b2, l)

        self.assertEqual(start, t['text'])
        self.assertEqual(l, t['label'])
        self.assertEqual(2, len(t['children']))

        node = t['children'][0]
        self.assertEqual(b1, node['text'])
        self.assertEqual(tree.label('sl-a', ['s', 'l', 'a'], t1),
            node['label'])
        self.assertEqual(0, len(node['children']))

        node = t['children'][1]
        self.assertEqual(b2, node['text'])
        self.assertEqual(tree.label('sl-b', ['s', 'l', 'b'], t2),
            node['label'])
        self.assertEqual(0, len(node['children']))
    def test_paragraph_tree_no_children(self):
        text = "Non title text"
        l = tree.label('Some label')
        node = paragraph_tree('A', [], text, l)
        self.assertEqual(tree.node(text, label=l), node)
    def test_paragraph_tree_with_children(self):
        fill = "dsfdffsfs\n"
        t1 = 'Q-3 This is the title'
        p1 = '\nSome paragraph\nContent\nmore\ncontent\n'
        t2 = 'Q-5--Spacing spacing'
        p2 = '\nMore paragraphs\nWe love them all\nParagraphs\n'
        t3 = 'Q-44 - Title here'
        p3 = '\nThird paragraph here'
        l = tree.label('L', ['l'])
        root = paragraph_tree('Q', [(len(fill), len(fill+t1+p1)), 
            (len(fill+t1+p1), len(fill+t1+p1+t2+p2)), 
            (len(fill+t1+p1+t2+p2), len(fill+t1+p1+t2+p2+t3+p3))],
            fill+t1+p1+t2+p2+t3+p3,
            l)
        self.assertEqual(fill, root['text'])
        self.assertEqual(l, root['label'])
        self.assertEqual(3, len(root['children']))

        node = root['children'][0]
        self.assertEqual(p1, node['text'])
        self.assertEqual(tree.label('L-3', ['l','3'], t1), node['label'])
        self.assertEqual(0, len(node['children']))

        node = root['children'][1]
        self.assertEqual(p2, node['text'])
        self.assertEqual(tree.label('L-5', ['l','5'], t2), node['label'])
        self.assertEqual(0, len(node['children']))

        node = root['children'][2]
        self.assertEqual(p3, node['text'])
        self.assertEqual(tree.label('L-44', ['l','44'], t3), node['label'])
        self.assertEqual(0, len(node['children']))
    def test_trees_from(self):
        reg_text = "Some reg text\nOther reg text\nSection 55. etc.\n"
        titleC = "Appendix C to Part 22 The Reckoning"
        bodyC = "\nSome content\nWith no structure\n"
        titleJ = "Appendix J to Part 22 Junior Notes"
        bodyJ = "\nTitle One\ncontent content\nTitle Two\nmore content\n"
        titleR = "Appendix R to Part 22 Reserved"
        bodyR = "\nR-1--Some Section\nmore more\nR-5--Header\nthen more"
        
        text = reg_text + titleC + bodyC + titleJ + bodyJ + titleR + bodyR

        nodes = trees_from(text, 22, tree.label('22', ['22']))
        self.assertTrue(3, len(nodes))

        self.assertEqual(generic_tree(bodyC,
            tree.label('22-C', ['22', 'C'], titleC)), nodes[0])
        self.assertEqual(generic_tree(bodyJ,
            tree.label('22-J', ['22', 'J'], titleJ)), nodes[1])
        self.assertEqual(paragraph_tree('R', [(1,29), (29, len(bodyR))], bodyR,
            tree.label('22-R', ['22', 'R'], titleR)), nodes[2])
