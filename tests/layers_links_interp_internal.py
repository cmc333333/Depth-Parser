from pyparsing import ParseException
from regs.layers.links.interp_internal import *
from unittest import TestCase

class LayersLinksInterpInternalTest(TestCase):
    def test_comment_positive(self):
        citations = [
            "comment 10(b)-5",
            "comment 10(b)-7.vi",
            "comment 10(b)-7.vi.Q",
            "comment 8(b)(1)-1",
            "comment 13(x)(5)(iv)-2",
            "comment 10000(z)(9)(x)(Y)-33",
            "comment 10000(z)(9)(x)(Y)-25",
            "comment 10000(z)(9)(x)(Y)-25.xc",
            "comment 10000(z)(9)(x)(Y)-25.xc.Z"
        ]
        for citation in citations:
            self.assertEqual(1, len(list(comment.scanString(citation))))
            _, _, end = comment.scanString(citation).next()
            self.assertEqual(len(citation), end)
    def test_comment_negative(self):
        citations = [
            "comment 10(5)-5",
            "comment 10(b)"
            "comment 10"
            "comment 8-b(1)"
        ]
        for citation in citations:
            self.assertRaises(ParseException, comment.parseString, citation)
    def test_comment_citations(self):
        text = "This has (a)(1) no paragraph (b) commentary citations"
        self.assertEqual([], comment_citations(text))
        text = "This has one comment 17(b)-7"
        self.assertEqual([(13, len(text))], comment_citations(text))
        text = "Multiple: comment 17(b)-7 and comment 20(a)(3)-2 and then comment\n"
        text += "20(b)(2)-4.ii."
        #   includes the trailing space
        self.assertEqual([(10, 26), (30, 49), (58, len(text)-1)], comment_citations(text))
