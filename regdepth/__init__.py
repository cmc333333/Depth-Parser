from regdepth.tree import *
from regdepth.section import build_section_tree, sections

def build_regulation_tree(text, part):
    """Build up the whole tree from the plain text of a single
    regulation."""
    sects = sections(text, part)
    if not sects:
        return _node(text)

    title = text[:text.find("\n")]
    lab = label(str(part), [str(part)], title)
    body_text = text[len(title):sects[0][0]]

    children = []
    for start,end in sects:
        section_text = text[start:end]
        children.append(build_section_tree(section_text, part))
    return node(body_text, children, lab)
