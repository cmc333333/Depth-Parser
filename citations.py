# vim: set fileencoding=utf-8 :

import string
from pyparsing import Word, Optional, oneOf, OneOrMore


lower_alpha_sub = "(" + Word(string.ascii_lowercase) + ")"
upper_alpha_sub = "(" + Word(string.ascii_uppercase) + ")"
roman_sub = "(" + Word("ivxlcdm") + ")"
digit_sub = "(" + Word(string.digits) + ")"

single_citation = (Word(string.digits) + "." + Word(string.digits) +
        Optional(lower_alpha_sub + Optional(digit_sub +
            Optional(roman_sub))))

multiple_sections = ("§§" + single_citation + OneOrMore(
    oneOf(",", "and") + Optional("and") + single_citation))


print multiple_sections.parseString("§§ 205.7, 205.8, and 205.9")
print single_citation.parseString("205.9")
print single_citation.parseString("205.9(b)")
print single_citation.parseString("205.9(b) (1)")
