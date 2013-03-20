from pyparsing import Word, Optional, LineStart, LineEnd, SkipTo, Literal
import re
from regs import search
import string

def find_next_offsets(text, part):
    """Find the start/end of the next interpretation"""
    def find_start(text):
        return search.find_start(text, u"Section", ur"%d.\d+" % part)
    return search.find_offsets(text, find_start)

def interpretations(text, part):
    """Return a list of interpretation offsets."""
    def offsets_fn(remaining_text, idx, excludes):
        return find_next_offsets(remaining_text, part)
    return search.segments(text, offsets_fn)

def get_section(title, part):
    return re.match(r'^Section %d.(\d+)(.*)$' % part, title).group(1)

lower_alpha_sub = "(" + Word(string.ascii_lowercase).setResultsName("id") + ")"
upper_alpha_sub = "(" + Word(string.ascii_uppercase).setResultsName("id") + ")"
roman_sub = "(" + Word("ivxlcdm").setResultsName("id") + ")"
digit_sub = "(" + Word(string.digits).setResultsName("id") + ")"

def header_search(plain_text, section):
    paragraph = (str(section) + lower_alpha_sub.setResultsName("paragraph1") + 
            Optional(digit_sub.setResultsName("paragraph2") +
                Optional(roman_sub.setResultsName("paragraph3") + 
                    Optional(upper_alpha_sub.setResultsName("paragraph4")))))

    whole_par = LineStart() + ("Paragraph" + paragraph)
    keyterm = (LineStart() + paragraph + 
            SkipTo("\n").setResultsName("term") + LineEnd())

    header = whole_par.setResultsName("whole") | keyterm.setResultsName("keyterm")

    return list(header.scanString(plain_text))

