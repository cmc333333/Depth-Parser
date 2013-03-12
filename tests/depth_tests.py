from unittest import TestCase
import depth

class DepthTest(TestCase):
    def test_find_start_success(self):
        """Simple label checks."""
        text = "This (a) is (Z) the first (1) section for (2) something"
        text += " and then (iii) another thing goes here."
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
