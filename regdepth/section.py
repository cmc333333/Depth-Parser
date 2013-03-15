# vim: set fileencoding=utf-8 :
import re
from regdepth.appendix import find_appendix_start
from regdepth.tree import *
from regdepth.search import find_start
from regdepth.super_paragraph import *
from regdepth.supplement import find_supplement_start

def find_next_section_start(text, part):
    """Find the start of the next section (e.g. 205.14)"""
    return find_start(text, u"§", str(part) + r"\.\d+")

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
    def label_fn(title):
        section = re.search(r'%d\.(\d+) ' % part, title).group(1)
        return label("%d.%s" % (part, section), [str(part), section])
    return build_super_paragraph_tree(text, label_fn)

