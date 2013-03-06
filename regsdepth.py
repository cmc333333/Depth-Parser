import re
import string

pt_file = open('205.14.txt')
pt = pt_file.read()
pt_file.close()

def roman_nums(max_value=False):
    """Generator for roman numerals."""
    mapping = [ 
            (   1, 'i'), (  4, 'iv'), (  5, 'v'), (  9, 'ix'),
            (  10, 'x'), ( 40, 'xl'), ( 50, 'l'), ( 90, 'xc'),
            ( 100, 'c'), (400, 'cd'), (500, 'd'), (900, 'cm'),
            (1000, 'm')
            ]
    i = 1
    while not bool(max_value) or i < max_value:
        next_str = ''
        remaining_int = i
        remaining_mapping = list(mapping)
        while remaining_mapping:
            (amount, chars) = remaining_mapping.pop()
            while remaining_int >= amount:
                next_str += chars
                remaining_int -= amount
        yield next_str
        i += 1

levels = [
        list(string.ascii_lowercase),
        list(string.digits[1:]),
        list(roman_nums(50)),
        list(string.ascii_uppercase)
        ]


def find_section_label(text, level, section):
    if len(levels) <= level or len(levels[level]) <= section:
        return None
    return re.search(r"\(%s\)" % levels[level][section], text)

def section_body_rest(text, level, section):
    match = find_section_label(text, level, section + 1)
    if match:
        return (text[:match.start()], text[match.start():])
    else:
        return (text, "")
    
def split_into_sections(text, level=0, section=0):
    match = find_section_label(text, level, section)
    if match:
        (body, rest) = section_body_rest(text[match.end():], level, section)
        return [body] + split_into_sections(rest, level, section+1)
    else:
        return []
    
x = split_into_sections(pt, 0, 0)
print len(x)
for i in range(len(x)):
    print x[i]
    print "\n\n"

"""
def parse(text, level = 0, index = 0):
    #   first, check if one up the parent layers has ended
    for l in range(level - 1):


    match = re.search(r"\(%s\)" % levels[level][index], text)
    if 
    print match.group(), match.start(), match.end()

parse(pt)
parse(pt, index = 2)
parse(pt, 2, 1)


lower_alpha = r"\(([a-z])\)"

def parse(txt):


matches = re.search(lower_alpha, pt)
print matches.group(), matches.start(), matches.end()
"""
