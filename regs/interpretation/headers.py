from pyparsing import Word, Optional, LineStart, LineEnd, SkipTo, Literal
import re
import string

lower_alpha_sub = "(" + Word(string.ascii_lowercase).setResultsName("id") + ")"
upper_alpha_sub = "(" + Word(string.ascii_uppercase).setResultsName("id") + ")"
roman_sub = "(" + Word("ivxlcdm").setResultsName("id") + ")"
digit_sub = "(" + Word(string.digits).setResultsName("id") + ")"

def parse(plain_text, section):
    paragraph = (str(section) + lower_alpha_sub.setResultsName("paragraph1") + 
            Optional(digit_sub.setResultsName("paragraph2") +
                Optional(roman_sub.setResultsName("paragraph3") + 
                    Optional(upper_alpha_sub.setResultsName("paragraph4")))))

    whole_par = LineStart() + ("Paragraph" + paragraph)
    keyterm = (LineStart() + paragraph + 
            SkipTo("\n").setResultsName("term") + LineEnd())

    header = whole_par.setResultsName("whole") | keyterm.setResultsName("keyterm")

    return list(header.scanString(plain_text))

def get_section(title, part):
    return re.match(r'^Section %d.(\d+)(.*)$' % part, title).group(1)
