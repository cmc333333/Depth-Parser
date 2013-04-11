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
    @patch('regs.layers.terms.children_with_defs')
    def test_applicable_definitions(self, children_with_defs):
        text1 = u'This has a “worD” and then more'
        text2 = u'I have “anotheR word” term and “moree”'
        text3 = u'This has no defs'
        text3a = u'But the child “DoeS sEe?”'
        text3bi = u'As do “subchildren”'
        text3biA = u'Also has no terms'
        text3bii = u'Has no terms'
        text3c = u'Also has no terms'
        children_with_defs.return_value = [
                tree.node(text1, label=tree.label("aaa")),
                tree.node(text2, label=tree.label("bbb")),
                tree.node(text3, children=[
                    tree.node(text3a, label=tree.label('ccc')),
                    tree.node(children=[
                        tree.node(text3bi, [tree.node(text3biA)], 
                            tree.label('ddd')),
                        tree.node(text3bii)
                        ]),
                    tree.node(text3c)
                    ])
                ]
        definitions = applicable_definitions(tree.node())
        self.assertEqual(5, len(definitions))
        
        definition = definitions[0]
        self.assertEqual(u'another word', definition[0])
        self.assertEqual(u'bbb', definition[1])
        self.assertEqual(text2, definition[2])

        definition = definitions[1]
        self.assertEqual(u'subchildren', definition[0])
        self.assertEqual(u'ddd', definition[1])
        self.assertEqual(text3bi + text3biA, definition[2])

        definition = definitions[3]
        self.assertEqual(u'moree', definition[0])
        self.assertEqual(u'bbb', definition[1])
        self.assertEqual(text2, definition[2])
    def test_term_structs(self):
        term_by_refs = [('rock band', 'a'), ('band', 'b'), ('drum', 'c'),
                ('other thing', 'd')]
        text = "I am in a rock band. That's a band with a drum, a rock drum."
        structs = term_structs(text, term_by_refs)
        self.assertEqual(3, len(structs))
        self.assertEqual('a', structs[0]['ref'])
        self.assertEqual([(10,19)], structs[0]['offsets'])
        self.assertEqual('b', structs[1]['ref'])
        self.assertEqual([(30,34)], structs[1]['offsets'])
        self.assertEqual('c', structs[2]['ref'])
        self.assertEqual([(42,46), (55,59)], structs[2]['offsets'])
    def test_tighten_scope(self):
        reference = {
                'a': {'term': 'apple', 'text': 'Outer scope'},
                'b': {'term': 'banana'},
                'c': {'term': 'apple', 'text': 'Inner scope'},
                'd': {'term': 'not userd'},
                'e': {'term': 'apple', 'text': 'Most inner scope'}
                }
        structs = [{'ref': 'b'}, {'ref':'a'}, {'ref': 'c'}, {'ref': 'e'}]
        self.assertEqual([structs[0], structs[3]], tighten_scope(structs,
            reference))
    def test_referencify(self):
        definitions = [("t"+str(i), "r"+str(i), "d"+str(i)) for i in
                range(3)]
        existing = {}
        refs = referencify(existing, definitions)
        self.assertEqual(3, len(refs))
        self.assertEqual(3, len(existing))

        definitions = [("t"+str(i), "r"+str(i+3), "d"+str(i+3)) for i in
                range(3)]
        refs = referencify(existing, definitions)
        self.assertEqual(3, len(refs))
        self.assertEqual(6, len(existing))

        term, ref = refs[1]
        self.assertEqual('t1', term)
        self.assertEqual({'term': 't1', 'reference': 'r4', 'text': 'd4'},
                existing[ref])
    @patch('regs.layers.terms.add_to_layer')
    def test_build(self, add_to_layer):
        """Add to Layer should be called on every node in the tree."""
        layer = build(tree.node(children=[
            tree.node(children=[tree.node(), tree.node()]),
            tree.node()
            ]))
        self.assertEqual(5, add_to_layer.call_count)
        self.assertTrue('referenced' in layer)

    def test_add_to_layer(self):
        """Integration test. Verify that a term later at one root in the
        tree is created."""
        root = tree.node(children=[
            tree.node('Section 1: No Defs'),
            tree.node('Section 2: Definitions', children=[
                tree.node(u'The term “awesome sauce” means "excellent"',
                    label=tree.label('2a')),
                tree.node(u'To “rock” means to have excellence', 
                    label=tree.label('2b'), children=[
                    tree.node("For example, `you rock' is positive",
                        label=tree.label('2bi'))
                ])
            ]),
            tree.node('Section 3: Rock Lobster', label=tree.label('3'),
                children=[
                tree.node('Rock Lobster, however, is not cool.',
                    label=tree.label('3a')),
                tree.node('Evidence: lobsters are not cool.',
                    label=tree.label('3b')),
                tree.node('Lobsers certainly have no awesome sauce.',
                    label=tree.label('3c'))
            ])
        ])
        layer = {'referenced': {}}
        add_to_layer(root, layer)
        self.assertTrue('2bi' in layer)
        struct = layer['2bi'][0]
        self.assertEqual([(18,22)], struct['offsets'])
        self.assertEqual('rock', layer['referenced'][struct['ref']]['term'])

        self.assertTrue('3' in layer)
        struct = layer['3'][0]
        self.assertEqual([(11,15)], struct['offsets'])
        self.assertEqual('rock', layer['referenced'][struct['ref']]['term'])

        self.assertTrue('3a' in layer)
        struct = layer['3a'][0]
        self.assertEqual([(0,4)], struct['offsets'])
        self.assertEqual('rock', layer['referenced'][struct['ref']]['term'])

        self.assertTrue('3c' in layer)
        struct = layer['3c'][0]
        self.assertEqual([(26,39)], struct['offsets'])
        self.assertEqual('awesome sauce', 
                layer['referenced'][struct['ref']]['term'])

