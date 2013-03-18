import re
from regdepth.search import find_start
from regdepth.tree import label

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

