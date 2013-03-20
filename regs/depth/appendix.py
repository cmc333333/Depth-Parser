import re
from regs.depth.super_paragraph import *
from regs.depth.tree import *
from regs.search import find_start

def find_appendix_start(text, appendix='A'):
    """Find the start of the appendix (e.g. Appendix A)"""
    return find_start(text, 'Appendix', appendix)
