from regs.depth.super_paragraph import *
from regs.depth.tree import label
from unittest import TestCase

class DepthSuperParagraphTest(TestCase):
    def test_build_super_paragraph_tree_no_citation(self):
        title = "This is my awesome title"
        body = "\nSomething (a) here (1) And then (i) Deeper (b) Message (1) Here"

        tree = build_super_paragraph_tree(title+body, lambda x:label(title=x))
        p_tree = regParser.build_paragraph_tree(body, label = label(title=title))
        for key in p_tree:
            if key != 'label':
                self.assertEqual(p_tree[key], tree[key])
        self.assertEqual(label(title=title), tree['label'])
    def test_build_super_paragraph_tree_citation(self):
        title = "This is my awesome title"
        body = "\nThis (a) has a paragraph (b) citation mixed (b) in (c) to it"

        tree = build_super_paragraph_tree(title+body, lambda x:label(title=x))
        p_tree = regParser.build_paragraph_tree(body, exclude=[(15,28)], 
                label = label(title=title))
        for key in p_tree:
            if key != 'label':
                self.assertEqual(p_tree[key], tree[key])
        self.assertEqual(label(title=title), tree['label'])
    def test_build_super_paragraph_tree_label_fn(self):
        title = "Title here"
        body = "\nthen some body"
        tree = build_super_paragraph_tree(title+body, lambda x:label(text="other"))
        self.assertEqual(tree['label'], {"text": "other", "parts": [], "title": title})
