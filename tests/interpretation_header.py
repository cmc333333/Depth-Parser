from regs.interpretation import headers
from unittest import TestCase

class InterpretationHeader(TestCase):
    def test_parse_header_paragraphs(self):
        text = "Paragraph 3(b)(c)\n\n\nParagraph 4(z)\nParagraph Invalid\n"
        self.assertEqual([], headers.parse(text, 2))

        three = headers.parse(text, 3)
        self.assertEqual(1, len(three))
        match, start, end = three[0]
        self.assertEqual(0, start)
        self.assertEqual(14, end)
        self.assertEqual('', match.keyterm)
        self.assertNotEqual('', match.whole)
        self.assertEqual('b', match.paragraph1.id)
        self.assertEqual('', match.paragraph2)

        four = headers.parse(text, 4)
        self.assertEqual(1, len(four))
        match, start, end = four[0]
        self.assertEqual(20, start)
        self.assertEqual(35, end)
        self.assertEqual('', match.keyterm)
        self.assertNotEqual('', match.whole)
        self.assertEqual('z', match.paragraph1.id)
        self.assertEqual('', match.paragraph2)
    def test_parse_header_keywords(self):
        text = "Blah 3(b)(c)\n\n3(b)(1)(iv)(Z) Some Definition\n3(i) Another\n3 none\n"
        self.assertEqual([], headers.parse(text, 4))

        three = headers.parse(text, 3)
        self.assertEqual(2, len(three))

        match, start, end = three[0]
        self.assertEqual(14, start)
        self.assertEqual(45, end)
        self.assertEqual('', match.whole)
        self.assertNotEqual('', match.keyterm)
        self.assertEqual('Some Definition', match.keyterm.term.strip())
        self.assertEqual('b', match.paragraph1.id)
        self.assertEqual('1', match.paragraph2.id)
        self.assertEqual('iv', match.paragraph3.id)
        self.assertEqual('Z', match.paragraph4.id)

        match, start, end = three[1]
        self.assertEqual(45, start)
        self.assertEqual(58, end)
        self.assertEqual('', match.whole)
        self.assertNotEqual('', match.keyterm)
        self.assertEqual('Another', match.keyterm.term.strip())
        self.assertEqual('i', match.paragraph1.id)
        self.assertEqual('', match.paragraph2)
    def test_parse_header_mix(self):
        text = "Paragraph 3(b)(1)\n\n3(b)(1)(iv)(Z) Some Definition\n3(i) Another\n3 a\n"
        self.assertEqual([], headers.parse(text, 4))

        three = headers.parse(text, 3)
        self.assertEqual(3, len(three))

        self.assertEqual(0, three[0][1])
        self.assertEqual(19, three[0][2])
        self.assertEqual(19, three[1][1])
        self.assertEqual(50, three[1][2])
        self.assertEqual(50, three[2][1])
        self.assertEqual(63, three[2][2])
