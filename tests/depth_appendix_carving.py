from regs.depth.appendix.carving import *
from unittest import TestCase

class DepthAppendixCarvingTest(TestCase):
    def test_find_appendix_start(self):
        text = "Some \nAppendix C Other\n\n Thing Appendix A\nAppendix B"
        self.assertEqual(None, find_appendix_start(text))
        self.assertEqual(None, find_appendix_start(text, 'A'))
        self.assertEqual(42, find_appendix_start(text, 'B'))
        self.assertEqual(6, find_appendix_start(text, 'C'))

