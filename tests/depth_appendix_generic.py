from regs.depth.appendix.generic import *
from unittest import TestCase

class DepthAppendixGenericTest(TestCase):
    def test_find_next_segment(self):
        long_text = "This Is All I Capital Case But Is Really, Really "
        long_text += "Long. So Long That It Should Not Be A Title Sentence"
        filler = "something here and something there and a little more"
        title = "Title Looking Segment"
        self.assertEqual(None, find_next_segment(long_text))
        self.assertEqual(None, find_next_segment(filler))
        self.assertEqual(None, find_next_segment(filler + "\n" + long_text))
        self.assertEqual(None, find_next_segment(long_text + "\n" + filler))
        self.assertEqual((0, len(title)), find_next_segment(title))
        self.assertEqual((len(filler), len(filler + title)), 
                find_next_segment(filler + "\n" + title))
        self.assertEqual((len(long_text), len(long_text + title)),
                find_next_segment(long_text + "\n" + title))
        self.assertEqual((0, len(title + long_text)),
                find_next_segment(title + "\n" + long_text + "\n" + title))
