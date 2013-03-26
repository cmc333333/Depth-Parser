from pyparsing import Word, Optional, LineStart, LineEnd, SkipTo, Literal
import re
from regs import search
import string

def find_next_section_offsets(text, part):
    """Find the start/end of the next section"""
    def find_start(text):
        return search.find_start(text, u"Section", ur"%d.\d+" % part)
    return search.find_offsets(text, find_start)

def sections(text, part):
    """Return a list of interpretation offsets."""
    def offsets_fn(remaining_text, idx, excludes):
        return find_next_section_offsets(remaining_text, part)
    return search.segments(text, offsets_fn)

def get_section_number(title, part):
    """Pull out section number from header. Assumes proper format"""
    return re.match(r'^Section %d.(\d+)(.*)$' % part, title).group(1)

lower_alpha_sub = "(" + Word(string.ascii_lowercase).setResultsName("id") + ")"
upper_alpha_sub = "(" + Word(string.ascii_uppercase).setResultsName("id") + ")"
roman_sub = "(" + Word("ivxlcdm").setResultsName("id") + ")"
digit_sub = "(" + Word(string.digits).setResultsName("id") + ")"

def _header_parser(section):
    paragraph = (str(section) + lower_alpha_sub.setResultsName("paragraph1") + 
            Optional(digit_sub.setResultsName("paragraph2") +
                Optional(roman_sub.setResultsName("paragraph3") + 
                    Optional(upper_alpha_sub.setResultsName("paragraph4")))))

    whole_par = LineStart() + ("Paragraph" + paragraph)
    keyterm = (LineStart() + paragraph + 
            SkipTo("\n").setResultsName("term") + LineEnd())

    return whole_par.setResultsName("whole") | keyterm.setResultsName("keyterm")

def relevance_offsets(plain_text, section):
    starts = [start for _,start,_ in _header_parser(section).scanString(plain_text)]
    starts.append(len(plain_text))
    for i in range(1, len(starts)):
        starts[i-1] = (starts[i-1], starts[i])
    starts = starts[:-1]
    return starts

def split_by_header(plain_text, section):
    triplets = list(_header_parser(section).scanString(plain_text))
    triplets.append((None, len(plain_text), None))
    chunks = []
    for i in range(1, len(triplets)):
        match, start, _ = triplets[i-1]
        _, end, _ = triplets[i]
        chunks.append((match, plain_text[start:end]))
    return chunks
