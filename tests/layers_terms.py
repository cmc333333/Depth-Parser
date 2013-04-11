# vim: set fileencoding=utf-8 :
from mock import patch
from regs.depth import tree
from regs.layers.terms import *
from unittest import TestCase

class LayersTermsTest(TestCase):
    def test_parse_from(self):
        text = u'“Term” and then some extra stuff'
        self.assertEqual(1, len(parse_from(text)))
        self.assertEqual(u'Term', parse_from(text)[0])
        
        text = u'Content content\n\nMore content\n then “wrapped phrase”'
        self.assertEqual(1, len(parse_from(text)))
        self.assertEqual(u'wrapped phrase', parse_from(text)[0])

        text = u'Sometimes you “have” many terms in “one section”'
        self.assertEqual(2, len(parse_from(text)))
        self.assertEqual([u'have', u'one section'], parse_from(text))

        text = u'This has no terms'
        self.assertEqual([], parse_from(text))
    def test_parse_from_quotes(self):
        #   Note, the first two are normal single quotes; the second are
        #   smart quotes
        text = u'Some "nonterm" and another "nterm" but this one “is a'
        text += u' term”, but so is “this”.'
        matches = parse_from(text)
        self.assertEqual(["is a term", "this"], matches)
    def test_children_with_defs(self):
        def1 = tree.node("Something about a definition")
        def2 = tree.node("Another definitions here")
        def3 = tree.node(label=tree.label(title="Yet more definitions"))
        def4 = tree.node(label=tree.label(title="Definition"))
        non1 = tree.node("This has no def")
        non2 = tree.node(label=tree.label(title="No def here"))
        root = tree.node(children=[def1, non1, def2, non1, def3, non2, def4, 
            non2])
        self.assertEqual([def1, def2, def3, def4], children_with_defs(root))
    def test_children_with_defs_2(self):
        children = []
        def1 = tree.node(label=tree.label(title="This has a definition in it"))
        children.append(def1)
        children.append(tree.node(label=tree.label(title="This does not")))
        def2 = tree.node("This has a definition")
        children.append(def2)
        children.append(tree.node("no such def"))
        def_children = children_with_defs(tree.node(children=children))
        self.assertEqual([def1, def2], def_children)
