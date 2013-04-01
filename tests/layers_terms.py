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
    def test_children_with_defs(self):
        def1 = tree.node("Something about a definition")
        def2 = tree.node("Another definitions here")
        def3 = tree.node(label=tree.label(title="Yet more definitions"))
        def4 = tree.node(label=tree.label(title="Definition"))
        non1 = tree.node("This has no def")
        non2 = tree.node(label=tree.label(title="No def here"))
        root = tree.node(children=[def1, non1, def2, non1, def3, non2, def4, non2])
        self.assertEqual([def1, def2, def3, def4], children_with_defs(root))
    @patch('regs.layers.terms.children_with_defs')
    def test_one_level_layer(self, children_with_defs):
        children_with_defs.return_value = [
                tree.node(u'This has a “word” and then more', label=tree.label("aaa")),
                tree.node(u'I have “another” term and “more”', label=tree.label("bbb")),
                tree.node(u'This has no defs', children=[
                    tree.node(u'But the child “does”', label=tree.label('ccc')),
                    tree.node(children=[
                        tree.node(u'As do “sub children”', label=tree.label('ddd')),
                        tree.node(u'Has no terms')
                        ]),
                    tree.node(u'Also has no terms')
                    ])
                ]
        layer = one_level_layer(tree.node())
        self.assertTrue('word' in layer)
        self.assertEqual('aaa', layer['word'])
        self.assertTrue('another' in layer)
        self.assertEqual('bbb', layer['another'])
        self.assertTrue('more' in layer)
        self.assertEqual('bbb', layer['more'])
        self.assertTrue('does' in layer)
        self.assertEqual('ccc', layer['does'])
        self.assertTrue('sub children' in layer)
        self.assertEqual('ddd', layer['sub children'])
    def test_build_layer(self):
        root = tree.node(label=tree.label("100"), children=[
            tree.node("Definitions", children=[
                tree.node(u'This has a defined “term” and in it', 
                    label=tree.label('100.2(b)')),
                tree.node('This parent has no term', label=tree.label("100.2(c)"),
                    children=[
                    tree.node(u'But the “child” does', label=tree.label('100.2(c)(3)')),
                    tree.node('Some other node')
                    ])
                ]),
            tree.node("No defs", children=[tree.node("None here"), tree.node("either")]),
            tree.node("Parent has no defs", label=tree.label("100.4"), children=[
                tree.node(u'This child has no defs'),
                tree.node(u'But this does have definitions',
                    label=tree.label('100.4(x)'), children=[
                    tree.node(u'This “term” replaces the outer scope',
                        label=tree.label('100.4(x)(1)'))
                    ])
                ]),
            ])
        layer = build_layer(root)
        self.assertEqual(['100', '100.4'], layer.keys())    # scope
        self.assertEqual([u'term', u'child'], layer['100'].keys())
        self.assertEqual('100.2(b)', layer['100'][u'term'])
        self.assertEqual('100.2(c)(3)', layer['100'][u'child'])
        self.assertEqual([u'term'], layer['100.4'].keys())
        self.assertEqual('100.4(x)(1)', layer['100.4'][u'term'])
