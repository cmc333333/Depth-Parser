from unittest import TestCase
import depth

class DepthTest(TestCase):
    def test_find_paragraph_start_success(self):
        """Simple label checks."""
        text = "This (a) is (Z) the first (1) section for (2) something\n"
        text += "and then (iii) another thing goes here."
        self.assertEqual(5, depth.find_paragraph_start(text, 0, 0))
        self.assertEqual(None, depth.find_paragraph_start(text, 0, 1))
        self.assertEqual(26, depth.find_paragraph_start(text, 1, 0))
        self.assertEqual(42, depth.find_paragraph_start(text, 1, 1))
        self.assertEqual(None, depth.find_paragraph_start(text, 1, 2))
        self.assertEqual(None, depth.find_paragraph_start(text, 2, 0))
        self.assertEqual(None, depth.find_paragraph_start(text, 2, 1))
        self.assertEqual(65, depth.find_paragraph_start(text, 2, 2))
        self.assertEqual(None, depth.find_paragraph_start(text, 2, 3))
        self.assertEqual(None, depth.find_paragraph_start(text, 3, 0))
        self.assertEqual(12, depth.find_paragraph_start(text, 3, 25))
        self.assertEqual(None, depth.find_paragraph_start(text, 3, 26))
    def test_find_paragraph_start_excludes(self):
        """Excluded ranges should not be included in results."""
        text = "This (a) is (a) a test (a) section for (a) testing."
        self.assertEqual(5, depth.find_paragraph_start(text, 0, 0))
        self.assertEqual(5, depth.find_paragraph_start(text, 0, 0, []))
        self.assertEqual(5, depth.find_paragraph_start(text, 0, 0, 
            [(10,len(text))]))
        self.assertEqual(5, depth.find_paragraph_start(text, 0, 0, [(0,1)]))
        self.assertEqual(12, depth.find_paragraph_start(text, 0, 0, [(0,10)]))
        self.assertEqual(12, depth.find_paragraph_start(text, 0, 0, 
            [(0,1), (4,9)]))
        self.assertEqual(12, depth.find_paragraph_start(text, 0, 0, [(5,5)]))
        self.assertEqual(39, depth.find_paragraph_start(text, 0, 0, 
            [(5,7), (10, 25)]))
        self.assertEqual(None, depth.find_paragraph_start(text, 0, 0, 
            [(0,len(text))]))
    def test_paragraph_offsets_present(self):
        """Test that section_offsets works as expected for good input."""
        text = "This (a) is a good (b) test for (c) something like this."""
        self.assertEqual((5,19), depth.paragraph_offsets(text, 0, 0))
        self.assertEqual((19,32), depth.paragraph_offsets(text, 0, 1))
        self.assertEqual((32,len(text)), depth.paragraph_offsets(text, 0, 2))
    def test_paragraph_offsets_not_present(self):
        """Verify we get None when the searched for text isn't there."""
        text = "This (a) is a good (b) test for (c) something like this."""
        self.assertEqual(None, depth.paragraph_offsets(text, 0, 3))
        self.assertEqual(None, depth.paragraph_offsets(text, 1, 0))
        self.assertEqual(None, depth.paragraph_offsets(text, 2, 0))
    def test_paragraphs(self):
        """This method should pull out the relevant paragraphs, as a list"""
        text = "This (a) is a good (1) test (2) of (3) some (b) body."
        paragraphs = depth.paragraphs(text,0)
        paragraph_strings = [text[s[0]:s[1]] for s in paragraphs]
        self.assertEqual(paragraph_strings,
                ["(a) is a good (1) test (2) of (3) some ",
                    "(b) body."])

        text = "(a) is a good (1) test (2) of (3) some "
        paragraphs = depth.paragraphs(text,1)
        paragraph_strings = [text[s[0]:s[1]] for s in paragraphs]
        self.assertEqual(paragraph_strings,
                ["(1) test ", "(2) of ", "(3) some "])

        paragraphs = depth.paragraphs(text,2)
        paragraph_strings = [text[s[0]:s[1]] for s in paragraphs]
        self.assertEqual(paragraph_strings, [])

    def test_build_paragraph_tree(self):
        """Verify several paragraph trees."""
        text = "This (a) is a good (1) test (2) of (3) some (b) body."
        self.assertEqual(depth.build_paragraph_tree(text),
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
        self.assertEqual(depth.build_paragraph_tree(text, 
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
        tree = depth.build_paragraph_tree(text, 
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
