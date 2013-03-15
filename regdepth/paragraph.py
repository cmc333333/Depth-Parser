import itertools
import re
from regdepth import tree
import string
from utils import roman_nums

p_levels = [
    list(string.ascii_lowercase),
    [str(i) for i in range(1,51)],
    list(itertools.islice(roman_nums(), 0, 50)),
    list(string.ascii_uppercase),
    #   Technically, there's italics (alpha) and (roman), but we aren't
    #   handling that yet
]

def find_paragraph_start(text, p_level, paragraph, exclude = []):
    """Find the position for the start of the requested label. p_Level is one
    of 0,1,2,3; paragraph is the index within that label. Return None if not
    present. Does not return results in the exclude list (a list of
    start/stop indices). """
    if len(p_levels) <= p_level or len(p_levels[p_level]) <= paragraph:
        return None
    match_starts = [m.start() for m 
            in re.finditer("\(%s\)" % p_levels[p_level][paragraph], text)]
    match_starts = [m for m in match_starts
            if all([m < e[0] or m > e[1]  for e in exclude])]
    if match_starts:
        return match_starts[0]

def paragraph_offsets(text, p_level, paragraph, exclude = []):
    """Find the start/end of the requested paragraph. Assumes the text does 
    not just up a p_level -- see build_paragraph_tree below."""
    start = find_paragraph_start(text, p_level, paragraph, exclude)
    end = find_paragraph_start(text, p_level, paragraph + 1, exclude)
    if start == None:
        return None
    if end == None:
        end = len(text)
    return (start, end)

def paragraphs(text, p_level, exclude = []):
    """Return a list of paragraph offsets defined by the level param."""
    paragraphs = []
    paragraph = 0
    remaining_text = text
    text_offset = 0
    offsets = paragraph_offsets(remaining_text, p_level, paragraph, exclude)
    while offsets:
        begin,end = offsets
        paragraphs.append((begin+text_offset, end+text_offset))
        paragraph += 1
        text_offset += end

        remaining_text = remaining_text[end:]
        exclude = [(e[0]-end, e[1]-end) for e in exclude]
        offsets = paragraph_offsets(remaining_text, p_level, paragraph, 
                exclude)
    return paragraphs


def build_paragraph_tree(text, p_level = 0, exclude = [], 
        label = tree.label("", [])):
    """Build a dict to represent the text hierarchy."""
    subparagraphs = paragraphs(text, p_level, exclude)
    if subparagraphs:
        body_text = text[0:subparagraphs[0][0]]
    else:
        body_text = text

    children = []
    for paragraph, (start,end) in enumerate(subparagraphs):
        new_text = text[start:end]
        new_excludes = [(e[0] - start, e[1] - start) for e in exclude]
        new_label = tree.extend_label(label, 
            '(' + p_levels[p_level][paragraph] + ')',
            p_levels[p_level][paragraph]
            )
        children.append(build_paragraph_tree(new_text, p_level + 1,
            new_excludes, new_label))
    return tree.node(body_text, children, label)

