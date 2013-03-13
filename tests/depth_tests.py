from unittest import TestCase
import depth

class DepthTest(TestCase):
    def test_find_start_success(self):
        """Simple label checks."""
        text = "This (a) is (Z) the first (1) section for (2) something\n"
        text += "and then (iii) another thing goes here."
        self.assertEqual(5, depth.find_start(text, 0, 0))
        self.assertEqual(None, depth.find_start(text, 0, 1))
        self.assertEqual(26, depth.find_start(text, 1, 0))
        self.assertEqual(42, depth.find_start(text, 1, 1))
        self.assertEqual(None, depth.find_start(text, 1, 2))
        self.assertEqual(None, depth.find_start(text, 2, 0))
        self.assertEqual(None, depth.find_start(text, 2, 1))
        self.assertEqual(65, depth.find_start(text, 2, 2))
        self.assertEqual(None, depth.find_start(text, 2, 3))
        self.assertEqual(None, depth.find_start(text, 3, 0))
        self.assertEqual(12, depth.find_start(text, 3, 25))
        self.assertEqual(None, depth.find_start(text, 3, 26))
    def test_find_start_excludes(self):
        """Excluded ranges should not be included in results."""
        text = "This (a) is (a) a test (a) section for (a) testing."
        self.assertEqual(5, depth.find_start(text, 0, 0))
        self.assertEqual(5, depth.find_start(text, 0, 0, []))
        self.assertEqual(5, depth.find_start(text, 0, 0, [(10,len(text))]))
        self.assertEqual(5, depth.find_start(text, 0, 0, [(0,1)]))
        self.assertEqual(12, depth.find_start(text, 0, 0, [(0,10)]))
        self.assertEqual(12, depth.find_start(text, 0, 0, [(0,1), (4,9)]))
        self.assertEqual(12, depth.find_start(text, 0, 0, [(5,5)]))
        self.assertEqual(39, depth.find_start(text, 0, 0, [(5,7), (10,
            25)]))
        self.assertEqual(None, depth.find_start(text, 0, 0, [(0,len(text))]))
    def test_section_offsets_present(self):
        """Test that section_offsets works as expected for good input."""
        text = "This (a) is a good (b) test for (c) something like this."""
        self.assertEqual((5,19), depth.section_offsets(text, 0, 0))
        self.assertEqual((19,32), depth.section_offsets(text, 0, 1))
        self.assertEqual((32,len(text)), depth.section_offsets(text, 0, 2))
    def test_section_offsets_not_present(self):
        """Verify we get None when the searched for text isn't there."""
        text = "This (a) is a good (b) test for (c) something like this."""
        self.assertEqual(None, depth.section_offsets(text, 0, 3))
        self.assertEqual(None, depth.section_offsets(text, 1, 0))
        self.assertEqual(None, depth.section_offsets(text, 2, 0))
    def test_sections(self):
        """This method should pull out the relevant sections, as a list"""
        text = "This (a) is a good (1) test (2) of (3) some (b) body."
        sections = depth.sections(text,0)
        section_strings = [text[s[0]:s[1]] for s in sections]
        self.assertEqual(section_strings,
                ["(a) is a good (1) test (2) of (3) some ",
                    "(b) body."])

        text = "(a) is a good (1) test (2) of (3) some "
        sections = depth.sections(text,1)
        section_strings = [text[s[0]:s[1]] for s in sections]
        self.assertEqual(section_strings,
                ["(1) test ", "(2) of ", "(3) some "])

        sections = depth.sections(text,2)
        section_strings = [text[s[0]:s[1]] for s in sections]
        self.assertEqual(section_strings, [])

    def test_build_section_tree(self):
        """Verify several section trees."""
        text = "This (a) is a good (1) test (2) of (3) some (b) body."
        self.assertEqual(depth.build_section_tree(text),
                {
                    "text": "This ",
                    "children": [
                        {
                            "text": "(a) is a good ",
                            "children": [
                                {
                                    "text": "(1) test ",
                                    "children": []
                                }, {
                                    "text": "(2) of ",
                                    "children": []
                                }, {
                                    "text": "(3) some ",
                                    "children": []
                                }
                            ]
                        }, {
                            "text": "(b) body.",
                            "children": []
                        }
                    ]
                })
    def test_build_section_tree_exclude(self):
        """Section tree should not split on exclude areas."""
        ref = "Ref (b)(2)"
        text = "This (a) is a good (1) %s test (2) no?" % ref
        ref_pos = text.find(ref)
        self.assertEqual(depth.build_section_tree(text, 
            exclude=[(ref_pos,ref_pos+len(ref))]),
                {
                    "text": "This ",
                    "children": [
                        {
                            "text": "(a) is a good ",
                            "children": [
                                {
                                    "text": "(1) %s test " % ref,
                                    "children": []
                                }, {
                                    "text": "(2) no?",
                                    "children": []
                                }
                            ]
                        }
                    ]
                })
