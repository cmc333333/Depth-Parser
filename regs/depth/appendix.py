import re
from regs.depth.super_paragraph import *
from regs.depth.tree import *
from regs.search import find_start

def find_appendix_start(text, appendix='A'):
    """Find the start of the appendix (e.g. Appendix A)"""
    return find_start(text, 'Appendix', appendix)

def build_appendix_tree(text, part):
    return
    #@TODO!
    def label_fn(title):
        section = re.search(r'Appendix (.) ' % part, title).group(1)
        return label("%d Appendix %s" % (part, section), [str(part), section])
    return build_super_paragraph_tree(text, label_fn)
