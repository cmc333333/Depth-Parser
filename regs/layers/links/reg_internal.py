# vim: set fileencoding=utf-8 :

import string
from pyparsing import Word, Optional, oneOf, OneOrMore, Regex

lower_alpha_sub = "(" + Word(string.ascii_lowercase).setResultsName("id") + ")"
upper_alpha_sub = "(" + Word(string.ascii_uppercase).setResultsName("id") + ")"
roman_sub = "(" + Word("ivxlcdm").setResultsName("id") + ")"
digit_sub = "(" + Word(string.digits).setResultsName("id") + ")"

sub_sub_paragraph = (
        lower_alpha_sub.setResultsName("level1") + 
        Optional(digit_sub.setResultsName("level2") +
        Optional(roman_sub.setResultsName("level3") + 
        Optional(upper_alpha_sub.setResultsName("level4"))))
)

single_section = (Word(string.digits) + "." + Word(string.digits) +
        Optional(sub_sub_paragraph) + Optional(Regex(",|and") + OneOrMore(
            lower_alpha_sub | upper_alpha_sub | roman_sub | digit_sub)))

multiple_section_citation = (u"§§" + single_section + OneOrMore(
    Regex(",|and") + Optional("and") + single_section))

single_section_citation = (u"§" + single_section)

single_paragraph = "paragraph" + sub_sub_paragraph
multiple_paragraphs = (
    "paragraphs" + 
    sub_sub_paragraph.setResultsName("car") + 
    OneOrMore(
        Regex(",|and") + Optional("and") + 
        sub_sub_paragraph.setResultsName("cdr", listAllMatches=True)
    )
)

any_citation = (multiple_section_citation | single_section_citation
        | single_paragraph | multiple_paragraphs)

def internal_citations(plain_text):
    """
    Return a list of pairs representing the start and end positions of
    internal_citations.
    """
    citations = []
    for _, start, end in any_citation.scanString(plain_text):
        citations.append((start,end))
    return citations
