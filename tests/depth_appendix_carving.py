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

    def test_find_appendix_section_start(self):
        text = "Some \nA-4--Section here\nB-99--Section here\nContent"
        self.assertEqual(6, find_appendix_section_start(text, 'A'))
        self.assertEqual(24, find_appendix_section_start(text, 'B'))
        self.assertEqual(None, find_appendix_section_start(text, 'C'))
    def test_find_next_appendix_section_offsets(self):
        head = "More\n"
        a5 = "A-5--Some Title\nContent\ncontent\n"
        a8 = "A-8--A Title\nBody body\nbody body text\ntext text"
        self.assertEqual((len(head), len(head+a5)), 
                find_next_appendix_section_offsets(head+a5+a8, 'A'))
        self.assertEqual((0, len(a8)),
                find_next_appendix_section_offsets(a8, 'A'))
    def test_appendix_sections(self):
        head = "More\n"
        a5 = "A-5--Some Title\nContent\ncontent\n"
        a8 = "A-8--A Title\nBody body\nbody body text\ntext text\n"
        a20 = "A-20--More content\nBody body"
        text = head + a5 + a8 + a20
        offsets = appendix_sections(text, 'A')
        self.assertEqual(3, len(offsets))
        self.assertEqual(a5, text[offsets[0][0]:offsets[0][1]])
        self.assertEqual(a8, text[offsets[1][0]:offsets[1][1]])
        self.assertEqual(a20, text[offsets[2][0]:offsets[2][1]])

    def test_get_appendix_letter(self):
        self.assertEqual("A", 
                get_appendix_letter("Appendix A to Part 511", 511))
        self.assertEqual("ZQR", 
                get_appendix_letter("Appendix ZQR to Part 10101", 10101))
    def test_get_appendix_section_number(self):
        self.assertEqual("2", 
                get_appendix_section_number("A-2--Title Stuff", 'A'))
        self.assertEqual("50", 
                get_appendix_section_number("QQ-50--Title Stuff", 'QQ'))
