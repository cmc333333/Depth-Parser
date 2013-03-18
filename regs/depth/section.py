# vim: set fileencoding=utf-8 :
import re
from regs.depth.appendix import find_appendix_start
from regs.depth.super_paragraph import *
from regs.depth.supplement import find_supplement_start
from regs.depth.tree import *
from regs.search import find_offsets, find_start

def find_next_section_start(text, part):
    """Find the start of the next section (e.g. 205.14)"""
    return find_start(text, u"§", str(part) + r"\.\d+")

def next_section_offsets(text, part):
    """Find the start/end of the next section"""
    offsets = find_offsets(text, lambda t: find_next_section_start(t, part))
    if offsets == None:
        return None

    start, end = offsets
    appendix_start = find_appendix_start(text, 'A')
    supplement_start = find_supplement_start(text)
    if appendix_start != None and appendix_start < end:
        return (start, appendix_start)
    if supplement_start != None and supplement_start < end:
        return (start, supplement_start)
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

