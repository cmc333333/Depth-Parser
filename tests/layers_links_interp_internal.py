from regs.layers.links.interp_internal import comment_citations
from unittest import TestCase

class LayersLinksInterpInternalTest(TestCase):
    def test_comment_citations(self):
        text = "This has (a)(1) no paragraph (b) commentary citations"
        self.assertEqual([], comment_citations(text))
        text = "This has one comment 17(b)-7"
        self.assertEqual([(13, len(text))], comment_citations(text))
        text = "Multiple: comment 17(b)-7 and comment 20(a)(3)-2 and then comment\n"
        text += "20(b)(2)-4.ii."
        #   includes the trailing space
        self.assertEqual([(10, 26), (30, 49), (58, len(text)-1)], comment_citations(text))
