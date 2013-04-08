from regs.depth.appendix.carving import *
from unittest import TestCase

class DepthAppendixCarvingTest(TestCase):
    def test_find_appendix_start(self):
        text = "Some \nAppendix C Other\n\n Thing Appendix A\nAppendix B"
        self.assertEqual(6, find_appendix_start(text))
        self.assertEqual(35, find_appendix_start(text[7:]))
        self.assertEqual(None, find_appendix_start(text[7 + 36:]))
    def test_find_next_appendix_offsets(self):
        sect1 = "Some \n"
        appa = "Appendix A Title\nContent\ncontent\n\n"
        appb = "Appendix Q More Info\n\nContent content\n"
        supp = "Supplement I The Interpretations\n\nAppendix Q\n"
        supp += "Interpretations about appendix Q"
        self.assertEqual((len(sect1), len(sect1+appa)),
                find_next_appendix_offsets(sect1+appa))
        self.assertEqual((len(sect1), len(sect1+appa)),
                find_next_appendix_offsets(sect1+appa+appb))
        self.assertEqual((0, len(appa)),
                find_next_appendix_offsets(appa+supp))
    def test_appendicies(self):
        sect1 = "Some \n"
        appa = "Appendix A Title\nContent\ncontent\n\n"
        appb = "Appendix Q More Info\n\nContent content\n"
        supp = "Supplement I The Interpretations\n\nAppendix Q\n"
        supp += "Interpretations about appendix Q"

        apps = appendicies(sect1 + appa + appb + supp)
        self.assertEqual(2, len(apps))
        self.assertEqual((len(sect1), len(sect1+appa)), apps[0])
        self.assertEqual((len(sect1+appa), len(sect1+appa+appb)), apps[1])
