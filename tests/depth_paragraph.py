from regs.depth import tree
from regs.depth.paragraph import ParagraphParser
from unittest import TestCase

def _mk_label(old_label, next_part):
    return tree.extend_label(old_label, '(' + next_part + ')', next_part)

regParser = ParagraphParser(r"\(%s\)", _mk_label)

class DepthParagraphTest(TestCase):
    def test_find_paragraph_start_success(self):
        """Simple label checks."""
        text = "This (a) is (Z) the first (1) section for (2) something\n"
        text += "and then (iii) another thing goes here."
        self.assertEqual(5, regParser.find_paragraph_start(text, 0, 0))
        self.assertEqual(None, regParser.find_paragraph_start(text, 0, 1))
        self.assertEqual(26, regParser.find_paragraph_start(text, 1, 0))
        self.assertEqual(42, regParser.find_paragraph_start(text, 1, 1))
        self.assertEqual(None, regParser.find_paragraph_start(text, 1, 2))
        self.assertEqual(None, regParser.find_paragraph_start(text, 2, 0))
        self.assertEqual(None, regParser.find_paragraph_start(text, 2, 1))
        self.assertEqual(65, regParser.find_paragraph_start(text, 2, 2))
        self.assertEqual(None, regParser.find_paragraph_start(text, 2, 3))
        self.assertEqual(None, regParser.find_paragraph_start(text, 3, 0))
        self.assertEqual(12, regParser.find_paragraph_start(text, 3, 25))
        self.assertEqual(None, regParser.find_paragraph_start(text, 3, 26))
    def test_find_paragraph_start_excludes(self):
        """Excluded ranges should not be included in results."""
        text = "This (a) is (a) a test (a) section for (a) testing."
        self.assertEqual(5, regParser.find_paragraph_start(text, 0, 0))
        self.assertEqual(5, regParser.find_paragraph_start(text, 0, 0, []))
        self.assertEqual(5, regParser.find_paragraph_start(text, 0, 0, 
            [(10,len(text))]))
        self.assertEqual(5, regParser.find_paragraph_start(text, 0, 0, [(0,1)]))
        self.assertEqual(12, regParser.find_paragraph_start(text, 0, 0, [(0,10)]))
        self.assertEqual(12, regParser.find_paragraph_start(text, 0, 0, 
            [(0,1), (4,9)]))
        self.assertEqual(12, regParser.find_paragraph_start(text, 0, 0, [(5,5)]))
        self.assertEqual(39, regParser.find_paragraph_start(text, 0, 0, 
            [(5,7), (10, 25)]))
        self.assertEqual(None, regParser.find_paragraph_start(text, 0, 0, 
            [(0,len(text))]))
    def test_paragraph_offsets_present(self):
        """Test that section_offsets works as expected for good input."""
        text = "This (a) is a good (b) test for (c) something like this."""
        self.assertEqual((5,19), regParser.paragraph_offsets(text, 0, 0))
        self.assertEqual((19,32), regParser.paragraph_offsets(text, 0, 1))
        self.assertEqual((32,len(text)), regParser.paragraph_offsets(text, 0, 2))
    def test_paragraph_offsets_not_present(self):
        """Verify we get None when the searched for text isn't there."""
        text = "This (a) is a good (b) test for (c) something like this."""
        self.assertEqual(None, regParser.paragraph_offsets(text, 0, 3))
        self.assertEqual(None, regParser.paragraph_offsets(text, 1, 0))
        self.assertEqual(None, regParser.paragraph_offsets(text, 2, 0))
    def test_paragraphs(self):
        """This method should pull out the relevant paragraphs, as a list"""
        text = "This (a) is a good (1) test (2) of (3) some (b) body."
        ps = regParser.paragraphs(text,0)
        paragraph_strings = [text[s[0]:s[1]] for s in ps]
        self.assertEqual(paragraph_strings,
                ["(a) is a good (1) test (2) of (3) some ",
                    "(b) body."])

        text = "(a) is a good (1) test (2) of (3) some "
        ps = regParser.paragraphs(text,1)
        paragraph_strings = [text[s[0]:s[1]] for s in ps]
        self.assertEqual(paragraph_strings,
                ["(1) test ", "(2) of ", "(3) some "])

        ps = regParser.paragraphs(text,2)
        paragraph_strings = [text[s[0]:s[1]] for s in ps]
        self.assertEqual(paragraph_strings, [])

    def test_build_paragraph_tree(self):
        """Verify several paragraph trees."""
        text = "This (a) is a good (1) test (2) of (3) some (b) body."
        self.assertEqual(regParser.build_paragraph_tree(text),
                {
                    "text": "This ",
                    "label": {"text": "", "parts": []},
                    "children": [
                        {
                            "text": "(a) is a good ",
                            "label": {"text": "(a)", "parts": ["a"]},
                            "children": [
                                {
                                    "text": "(1) test ",
                                    "label": {
                                        "text": "(a)(1)",
                                        "parts": ["a", "1"]
                                        },
                                    "children": []
                                }, {
                                    "text": "(2) of ",
                                    "label": {
                                        "text": "(a)(2)",
                                        "parts": ["a", "2"]
                                        },
                                    "children": []
                                }, {
                                    "text": "(3) some ",
                                    "label": {
                                        "text": "(a)(3)",
                                        "parts": ["a", "3"]
                                        },
                                    "children": []
                                }
                            ]
                        }, {
                            "text": "(b) body.",
                            "label": {"text": "(b)", "parts": ["b"]},
                            "children": []
                        }
                    ]
                })
    def test_build_paragraph_tree_exclude(self):
        """Paragraph tree should not split on exclude areas."""
        ref = "Ref (b)(2)"
        text = "This (a) is a good (1) %s test (2) no?" % ref
        ref_pos = text.find(ref)
        self.assertEqual(regParser.build_paragraph_tree(text, 
            exclude=[(ref_pos,ref_pos+len(ref))]),
                {
                    "text": "This ",
                    "label": {"text": "", "parts": []},
                    "children": [
                        {
                            "text": "(a) is a good ",
                            "label": {"text": "(a)", "parts": ["a"]},
                            "children": [
                                {
                                    "text": "(1) %s test " % ref,
                                    "label": {
                                        "text": "(a)(1)",
                                        "parts": ["a", "1"]
                                        },
                                    "children": []
                                }, {
                                    "text": "(2) no?",
                                    "label": {
                                        "text": "(a)(2)",
                                        "parts": ["a", "2"]
                                        },
                                    "children": []
                                }
                            ]
                        }
                    ]
                })
    def test_build_paragraph_tree_label_preamble(self):
        """Paragraph tree's labels can be prepended."""
        text = "This (a) is a good (1) test (2) of (3) some (b) body."
        tree = regParser.build_paragraph_tree(text, 
                label={"text": "205.14", "parts": ["205", "14"]})
        self.assertEqual("205.14", tree['label']['text'])
        self.assertEqual(["205", "14"], tree['label']['parts'])
        child_a, child_b = tree['children']
        self.assertEqual("205.14(a)", child_a['label']['text'])
        self.assertEqual(["205", "14", "a"], child_a['label']['parts'])
        child_a_1, child_a_2, child_a_3 = child_a['children']
        self.assertEqual("205.14(a)(1)", child_a_1['label']['text'])
        self.assertEqual(["205", "14", "a", "1"], child_a_1['label']['parts'])
        self.assertEqual("205.14(a)(2)", child_a_2['label']['text'])
        self.assertEqual(["205", "14", "a", "2"], child_a_2['label']['parts'])
        self.assertEqual("205.14(a)(3)", child_a_3['label']['text'])
        self.assertEqual(["205", "14", "a", "3"], child_a_3['label']['parts'])
        self.assertEqual("205.14(b)", child_b['label']['text'])
        self.assertEqual(["205", "14", "b"], child_b['label']['parts'])
    def test_find_paragraph_start_is(self):
        """Test the case where we are looking for paragraph (i) (the letter,) but we run
        into (i) (the roman numeral.)"""
        text1 = "(h) Paragraph (1) H has (i) some (ii) sub (iii) sections but "
        text2 = "(i) this paragraph does not."
        self.assertEqual(len(text1), regParser.find_paragraph_start(text1+text2, 0, 8))
    def test_matching_subparagraph_ids(self):
        matches = regParser.matching_subparagraph_ids(0,8)    #   'i'
        self.assertEqual(1, len(matches))
        self.assertEqual(2, matches[0][0])
        self.assertEqual(0, matches[0][1])
        matches = regParser.matching_subparagraph_ids(1,3)    #   '4'
        self.assertEqual(0, len(matches))
    def test_best_start(self):
        text = "This is my (ii) awesome text with a subparagraph in it."
        self.assertEqual(len(text), regParser.best_start(text, 0, 8, [0, len(text)]))
        self.assertEqual(0, regParser.best_start(text, 0, 9, [0, len(text)]))
