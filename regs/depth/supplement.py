import re
from regs.depth.tree import label
from regs.search import find_start

def find_supplement_start(text, supplement='I'):
    """Find the start of the supplement (e.g. Supplement I)"""
    return find_start(text, 'Supplement', supplement)


def build_supplemental_tree(text, part):
    return
    #@todo
    def label_fn(title):
        section = re.search(r'Supplemental (.) ' % part, title).group(1)
        return label("%d Supplemental %s" % (part, section), 
                [str(part), section])
    return build_super_paragraph_tree(text, label_fn)

