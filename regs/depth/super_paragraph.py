from regs import citations, utils
from regs.depth import tree
from regs.depth.paragraph import ParagraphParser

def _mk_label(old_label, next_part):
    return tree.extend_label(old_label, '(' + next_part + ')', next_part)

regParser = ParagraphParser(r"\(%s\)", _mk_label)

def build_super_paragraph_tree(text, label_fn):
    """Construct the tree for a section, appendix, or supplemental piece.
    label_fn takes the title as a parameter and creates the label for this
    tree node."""
    title, text = utils.title_body(text)

    exclude = citations.internal_citations(text)
    label = label_fn(title)
    tree = regParser.build_paragraph_tree(text, exclude=exclude, label=label)

    tree['label']['title'] = title
    return tree

