# vim: set fileencoding=utf-8 :

import string
from pyparsing import Word, Optional, oneOf, OneOrMore, Regex


lower_alpha_sub = "(" + Word(string.ascii_lowercase) + ")"
upper_alpha_sub = "(" + Word(string.ascii_uppercase) + ")"
roman_sub = "(" + Word("ivxlcdm") + ")"
digit_sub = "(" + Word(string.digits) + ")"

sub_sub_paragraph = lower_alpha_sub + Optional(digit_sub +
        Optional(roman_sub + Optional(upper_alpha_sub)))

single_section = (Word(string.digits) + "." + Word(string.digits) +
        Optional(sub_sub_paragraph) + Optional(Regex(",|and") + OneOrMore(
            lower_alpha_sub | upper_alpha_sub | roman_sub | digit_sub)))

multiple_section_citation = (u"§§" + single_section + OneOrMore(
    Regex(",|and") + Optional("and") + single_section))

single_section_citation = (u"§" + single_section)

single_paragraph = "paragraph" + sub_sub_paragraph
multiple_paragraphs = "paragraphs" + sub_sub_paragraph + OneOrMore(
        Regex(",|and") + Optional("and") + sub_sub_paragraph)

any_citation = (multiple_section_citation | single_section_citation
        | single_paragraph | multiple_paragraphs)


to_check = [
    (u"§§ 205.7, 205.8, and 205.9", 13),
    (u"§ 205.9(b)", 7),
    (u"§ 205.9(a)", 7),
    (u"§ 205.9(b)(1)", 10),
    (u"§ 205.6(b) (1) and (2)", 14),
    (u"§§ 205.6(b)(3) and 205.11(b)(1)(i)", 23),
    (u"§\n205.11(c)(2)(ii)", 13),
    (u"§ 205.9(b)(1)(i)(C)", 16)
    ]


for word, length in to_check:
    assert(length == len(any_citation.parseString(word)))

def internal_citations(plain_text):
    """
    Return a list of pairs representing the start and end positions of
    internal_citations.
    """
    citations = []
    for _, start, end in any_citation.scanString(plain_text):
        citations.append((start,end))
    return citations
