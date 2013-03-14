# vim: set fileencoding=utf-8 :

import citations
import itertools
import re
import string
from utils import roman_nums

_p_levels = [
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
    if len(_p_levels) <= p_level or len(_p_levels[p_level]) <= paragraph:
        return None
    match_starts = [m.start() for m 
            in re.finditer("\(%s\)" % _p_levels[p_level][paragraph], text)]
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
    offsets = paragraph_offsets(text, p_level, paragraph, exclude)
    while offsets:
        paragraphs.append(offsets)
        paragraph += 1
        offsets = paragraph_offsets(text, p_level, paragraph, exclude)
    return paragraphs

def _label(text, parts, title=None):
    if title:
        return {'text': text, 'parts': parts, 'title': title}
    return {'text': text, 'parts': parts}
def _extend_label(existing, text, part):
    return _label(existing['text'] + text, existing['parts'] + [part])
def _node(text='', children=[], label=_label('',[])):
    return {'text': text, 'children': children, 'label': label}

def build_paragraph_tree(text, p_level = 0, exclude = [], 
        label = _label("", [])):
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
        new_label = _extend_label(label, 
            '(' + _p_levels[p_level][paragraph] + ')',
            _p_levels[p_level][paragraph]
            )
        children.append(build_paragraph_tree(new_text, p_level + 1,
            new_excludes, new_label))
    return _node(body_text, children, label)

def _find_start(text, heading, index):
    """Find the start of an appendix, supplement, etc."""
    match = re.search(r'^%s %s' % (heading, index), text, re.MULTILINE)
    if match:
        return match.start()

def find_next_section_start(text, part):
    """Find the start of the next section (e.g. 205.14)"""
    return _find_start(text, u"§", str(part) + r"\.\d+")

def find_appendix_start(text, appendix='A'):
    """Find the start of the appendix (e.g. Appendix A)"""
    return _find_start(text, 'Appendix', appendix)

def find_supplement_start(text, supplement='I'):
    """Find the start of the supplement (e.g. Supplement I)"""
    return _find_start(text, 'Supplement', supplement)

def next_section_offsets(text, part):
    """Find the start/end of the next section"""
    start = find_next_section_start(text, part)
    if start == None:
        return None
    post_start_text = text[start+1:]
    next_section = find_next_section_start(post_start_text, part)
    if next_section:
        next_section += start + 1

    start_appendix = find_appendix_start(text, 'A')
    start_supplement = find_supplement_start(text)

    end = next_section
    if end == None:
        end = start_appendix
    if end == None:
        end = start_supplement
    if end == None:
        end = len(text)
    return (start, end)

def sections(text, part):
    """Return a list of section offsets. Does not include appendices."""
    sections = []
    remaining_text = text
    text_offset = 0
    offsets = next_section_offsets(remaining_text, part)
    while offsets:
        begin,end = offsets
        sections.append((begin+text_offset, end+text_offset))
        text_offset += begin + 1

        remaining_text = remaining_text[begin + 1:]
        offsets = next_section_offsets(remaining_text, part)
    return sections

def build_section_tree(text, part):
    """Construct the tree for a whole section. Assumes the section starts
    with an identifier"""
    title = text[:text.find("\n")]
    text = text[len(title):]
    section = re.search(r'%d\.(\d+) ' % part, title).group(1)

    exclude = citations.internal_citations(text)
    label = _label("%d.%s" % (part, section), [str(part), section])
    tree = build_paragraph_tree(text, exclude=exclude, label=label)

    tree['label']['title'] = title
    return tree

def build_regulation_tree(text, part):
    """Build up the whole tree from the plain text of a single
    regulation."""
    sects = sections(text, part)
    if not sects:
        return _node(text)

    title = text[:text.find("\n")]
    label = _label(str(part), [str(part)], title)
    body_text = text[len(title):sects[0][0]]

    children = []
    for start,end in sects:
        section_text = text[start:end]
        children.append(build_section_tree(section_text, part))
    return _node(body_text, children, label)
