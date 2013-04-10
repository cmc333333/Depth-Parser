# vim: set fileencoding=utf-8 :

import string
from pyparsing import Word, Optional, oneOf, OneOrMore, Regex


lower_alpha_sub = "(" + Word(string.ascii_lowercase) + ")"
upper_alpha_sub = "(" + Word(string.ascii_uppercase) + ")"
roman_sub = "(" + Word("ivxlcdm") + ")"
digit_sub = "(" + Word(string.digits) + ")"

reg_ref = Word(string.digits) + lower_alpha_sub + Optional(digit_sub +
        Optional(roman_sub + Optional(upper_alpha_sub)))

upper_alpha_dec = "." + Word(string.ascii_uppercase)
roman_dec = "." + Word("ivxlcdm")
digit_dec = Word(string.digits)

comment = "comment" + reg_ref + "-" + (digit_dec + Optional(roman_dec + 
        # do not account for whitespace
        Optional(upper_alpha_dec))).leaveWhitespace()   

def comment_citations(plain_text):
    """
    Return a list of pairs representing the start and end positions of
    internal_citations.
    """
    p = "comment" + reg_ref + "-" + digit_dec
    return [(start, end) for _, start, end in comment.scanString(plain_text)]

