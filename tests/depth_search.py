from regdepth.search import *
from unittest import TestCase

class DepthSearchTest(TestCase):
    def test_find_start(self):
        text = "Here is \n Some text\nWith Some\nHeader Info Here\nthen nonsense"
        self.assertEqual(30, find_start(text, "Header", "Info"))
        self.assertEqual(0, find_start(text, "Here", "is"))
        self.assertEqual(47, find_start(text, "then", "nonsense"))
        self.assertEqual(None, find_start(text, "doesn't", "exist"))
        self.assertEqual(None, find_start(text, "Here", "text"))

