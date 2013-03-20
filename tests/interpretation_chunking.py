from regs.interpretation.chunking import *
from unittest import TestCase

class InterpretationChunking(TestCase):
    def test_split_by_header_paragraphs(self):
        p4_text = "Paragraph 4(z)\nParagraph Invalid\n"
        text = "Paragraph 3(b)(c)\n\n\n" + p4_text
        self.assertEqual([], split_by_header(text, 2))

        three = split_by_header(text, 3)
        self.assertEqual(1, len(three))
        match, p3 = three[0]
        self.assertEqual(text, p3)
        self.assertEqual('', match.keyterm)
        self.assertNotEqual('', match.whole)
        self.assertEqual('b', match.paragraph1.id)
        self.assertEqual('', match.paragraph2)

        four = split_by_header(text, 4)
        self.assertEqual(1, len(four))
        match, p4 = four[0]
        self.assertEqual(p4_text, p4)
        self.assertEqual('', match.keyterm)
        self.assertNotEqual('', match.whole)
        self.assertEqual('z', match.paragraph1.id)
        self.assertEqual('', match.paragraph2)
    def test_split_by_header_keywords(self):
        p3_kw1_text = "3(b)(1)(iv)(Z) Some Definition\n"
        p3_kw2_text = "3(i) Another\n3 none\n"
        text = "Blah 3(b)(c)\n\n" + p3_kw1_text + p3_kw2_text
        self.assertEqual([], split_by_header(text, 4))

        three = split_by_header(text, 3)
        self.assertEqual(2, len(three))

        match, p3_kw1 = three[0]
        self.assertEqual(p3_kw1_text, p3_kw1)
        self.assertEqual('', match.whole)
        self.assertNotEqual('', match.keyterm)
        self.assertEqual('Some Definition', match.keyterm.term.strip())
        self.assertEqual('b', match.paragraph1.id)
        self.assertEqual('1', match.paragraph2.id)
        self.assertEqual('iv', match.paragraph3.id)
        self.assertEqual('Z', match.paragraph4.id)

        match, p3_kw2 = three[1]
        self.assertEqual(p3_kw2_text, p3_kw2)
        self.assertEqual('', match.whole)
        self.assertNotEqual('', match.keyterm)
        self.assertEqual('Another', match.keyterm.term.strip())
        self.assertEqual('i', match.paragraph1.id)
        self.assertEqual('', match.paragraph2)
    def test_split_by_header_mix(self):
        p1_text = "Paragraph 3(b)(1)\n\n"
        p2_text = "3(b)(1)(iv)(Z) Some Definition\n"
        p3_text = "3(i) Another\n3 a\n"
        text = p1_text + p2_text + p3_text
        self.assertEqual([], split_by_header(text, 4))

        three = split_by_header(text, 3)
        self.assertEqual(3, len(three))

        self.assertEqual([p1_text, p2_text, p3_text], [t[1] for t in three])
    def test_find_next_section_offsets(self):
        section_5 = "Section 201.5\nSection 202.3\nother body\n\n"
        section_65 = "Section 201.65\n body body\n\nSection Other"
        text = "Something Section\n" + section_5 + section_65
        self.assertEqual(None, find_next_section_offsets(text, 404))

        begin,end = find_next_section_offsets(text, 201)
        self.assertEqual(section_5, text[begin:end])
    def test_sections(self):
        section_5 = "Section 201.5\nSection 202.3\nother body\n\n"
        section_65 = "Section 201.65\n body body\n\nSection Other"
        text = "Something Section\n" + section_5 + section_65
        self.assertEqual([], sections(text,404))

        interps = sections(text, 201)
        self.assertEqual(2, len(interps))
        begin, end = interps[0]
        self.assertEqual(section_5, text[begin:end])
        begin, end = interps[1]
        self.assertEqual(section_65, text[begin:end])
    def test_get_section_number(self):
        self.assertEqual("101", get_section_number("Section 55.101 Something Here", 55))
