import re
from regdepth.search import find_start
from regdepth.super_paragraph import *
from regdepth.tree import *

def find_appendix_start(text, appendix='A'):
    """Find the start of the appendix (e.g. Appendix A)"""
    return find_start(text, 'Appendix', appendix)

def build_appendix_tree(text, part):
    def label_fn(title):
        section = re.search(r'Appendix (.) ' % part, title).group(1)
        return label("%d Appendix %s" % (part, section), [str(part), section])
    return build_super_paragraph_tree(text, label_fn)
