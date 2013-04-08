from regs import search
from regs.depth.supplement import find_supplement_start
import string

def find_appendix_start(text):
    """Find the start of the appendix (e.g. Appendix A)"""
    return search.find_start(text, u'Appendix', ur'[A-Z]')

def find_next_appendix_offsets(text):
    """Find the start/end of the next appendix. Accounts for supplements"""
    offsets = search.find_offsets(text, find_appendix_start)
    if offsets == None:
        return None

    start, end = offsets
    supplement_start = find_supplement_start(text)
    if supplement_start != None and supplement_start < start:
        return None
    if supplement_start != None and supplement_start < end:
        return (start, supplement_start)
    return (start, end)

def appendicies(text):
    """Carve out a list of all the appendix offsets."""
    def offsets_fn(remaining_text, idx, excludes):
        return find_next_appendix_offsets(remaining_text)
    return search.segments(text, offsets_fn)
