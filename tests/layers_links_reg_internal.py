# vim: set fileencoding=utf-8 :

from pyparsing import ParseException
from regs.layers.links.reg_internal import any_citation, internal_citations
from unittest import TestCase

class LayersLinksRegInternalTest(TestCase):
    def test_any_citation_positive(self):
        citations = [
            (u"§§ 205.7, 205.8, and 205.9", 13),
            (u"§ 205.9(b)", 7),
            (u"§ 205.9(a)", 7),
            (u"§ 205.9(b)(1)", 10),
            (u"§ 205.6(b) (1) and (2)", 14),
            (u"§§ 205.6(b)(3) and 205.11(b)(1)(i)", 23),
            (u"§\n205.11(c)(2)(ii)", 13),
            (u"§ 205.9(b)(1)(i)(C)", 16)
        ]
        for citation, length in citations:
            self.assertEqual(length, len(any_citation.parseString(citation)))
    def test_any_citation_negative(self):
        citations = [u"§§ abc.tt", u"§ bbb.qq", u"205.9(a)", u"§§  205.9(1)"]
        for citation in citations:
            self.assertRaises(ParseException, any_citation.parseString, citation)
    def test_internal_citations(self):
        seg1 = u"This text will be checked for "
        seg2 = u"§ 105.22(b)(1)"
        seg3 = u" sections within it. For example § this is not a section\n"
        seg4 = u"§§ 22.32(a) and 39.21(c)(4)(iv)(Q)"
        seg5 = u" § not a section."
        self.assertEqual(internal_citations(seg1 + seg2 + seg3 + seg4 + seg5),
                #   Trailing space is included
                [   (len(seg1), len(seg1 + seg2) + 1),
                    (len(seg1 + seg2 + seg3), len(seg1 + seg2 + seg3 + seg4) + 1)])
