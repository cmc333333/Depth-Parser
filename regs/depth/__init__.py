from regs import utils
from regs.depth.tree import *
from regs.depth.section import build_section_tree, sections

def build_regulation_tree(text, part):
    """Build up the whole tree from the plain text of a single
    regulation."""
    title, body = utils.title_body(text)
    lab = label(str(part), [str(part)], title)

    sects = sections(body, part)
    if not sects:
        return node(text, label=lab)
    children_text = body[:sects[0][0]]

    children = []
    for start,end in sects:
        section_text = body[start:end]
        children.append(build_section_tree(section_text, part))
    return node(children_text, children, lab)
