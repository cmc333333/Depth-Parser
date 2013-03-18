from regs.search import find_offsets, find_start
from unittest import TestCase

class SearchTest(TestCase):
    def test_find_start(self):
        text = "Here is \n Some text\nWith Some\nHeader Info Here\nthen nonsense"
        self.assertEqual(30, find_start(text, "Header", "Info"))
        self.assertEqual(0, find_start(text, "Here", "is"))
        self.assertEqual(47, find_start(text, "then", "nonsense"))
        self.assertEqual(None, find_start(text, "doesn't", "exist"))
        self.assertEqual(None, find_start(text, "Here", "text"))
    def test_find_offsets(self):
        text = "Trying to find the start of this section and the other start here"
        self.assertEqual((19,55), find_offsets(text, lambda t:t.find("start")))
        self.assertEqual((10,len(text)), find_offsets(text, lambda t:t.find("find")))
        self.assertEqual((0,len(text)), find_offsets(text, lambda t:t.find("Trying")))
        self.assertEqual(None, find_offsets(text, lambda t:t.find("xxxx")))
