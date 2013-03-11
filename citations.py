# vim: set fileencoding=utf-8 :

import string
from pyparsing import Word, Optional, oneOf, OneOrMore, Regex


lower_alpha_sub = "(" + Word(string.ascii_lowercase) + ")"
upper_alpha_sub = "(" + Word(string.ascii_uppercase) + ")"
roman_sub = "(" + Word("ivxlcdm") + ")"
digit_sub = "(" + Word(string.digits) + ")"

sub_sub_section = lower_alpha_sub + Optional(digit_sub +
        Optional(roman_sub + Optional(upper_alpha_sub)))

single_citation = (Word(string.digits) + "." + Word(string.digits) +
        Optional(sub_sub_section) + Optional(Regex(",|and") + OneOrMore(
            lower_alpha_sub | upper_alpha_sub | roman_sub | digit_sub)))

multiple_sections = ("§§" + single_citation + OneOrMore(
    Regex(",|and") + Optional("and") + single_citation))

single_section = ("§" + single_citation)

any_citation = multiple_sections | single_section


to_check = [
    ("§§ 205.7, 205.8, and 205.9", 13),
    ("§ 205.9(b)", 7),
    ("§ 205.9(a)", 7),
    ("§ 205.9(b)(1)", 10),
    ("§ 205.6(b) (1) and (2)", 14),
    ("§§ 205.6(b)(3) and 205.11(b)(1)(i)", 23),
    ("§\n205.11(c)(2)(ii)", 13),
    ("§ 205.9(b)(1)(i)(C)", 16)
    ]


for word, length in to_check:
    assert(length == len(any_citation.parseString(word)))

pt_file = open('rege.txt')
pt = pt_file.read().strip()
pt_file.close()
for _, start, end in any_citation.scanString(pt):
    print pt[start:end]
