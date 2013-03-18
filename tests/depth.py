# vim: set fileencoding=utf-8 :

from regdepth import *
from unittest import TestCase

class DepthTest(TestCase):
    def test_build_regulation_tree_no_sections(self):
        text = "Regulation Title\nThen some more content"
        self.assertEqual(tree.node(text, label=label("201", ["201"], "Regulation Title")), 
                build_regulation_tree(text, 201))
    def test_build_regulation_tree_sections(self):
        title = u"Regulation Title"
        sect1_title = u"§ 204.1 Best Section"
        sect1 = u"(a) I believe this is (b) the (1) best section (2) don't (c) you?"
        sect2_title = u"§ 204.2 Second Best Section"
        sect2 = u"Some sections \ndon't have must \ndepth at all."
        sect4_title = u"§ 204.4 I Skipped One"
        sect4 = u"Others \n(a) Skip sections for (1) No \n(2) Apparent \n(3) Reason"

        text = "\n".join((title, sect1_title, sect1, sect2_title, sect2, sect4_title,
            sect4))

        reg = build_regulation_tree(text, 204)
        self.assertEqual(tree.label("204", ["204"], title), reg['label'])
        self.assertEqual("", reg['text'].strip())
        self.assertEqual(3, len(reg['children']))
        (sect1_tree, sect2_tree, sect4_tree) = reg['children']

        self.assertEqual(tree.label("204.1", ["204", "1"], sect1_title),
                sect1_tree['label'])
        self.assertEqual("", sect1_tree['text'].strip())
        self.assertEqual(3, len(sect1_tree['children']))
        self.assertEqual(0, len(sect1_tree['children'][0]['children']))
        self.assertEqual(2, len(sect1_tree['children'][1]['children']))
        self.assertEqual(0, len(sect1_tree['children'][2]['children']))

        self.assertEqual(tree.label("204.2", ["204", "2"], sect2_title),
                sect2_tree['label'])
        self.assertEqual(sect2, sect2_tree['text'].strip())
        self.assertEqual(0, len(sect2_tree['children']))

        self.assertEqual(tree.label("204.4", ["204", "4"], sect4_title),
                sect4_tree['label'])
        self.assertEqual(u"Others", sect4_tree['text'].strip())
        self.assertEqual(1, len(sect4_tree['children']))
        self.assertEqual(3, len(sect4_tree['children'][0]['children']))
