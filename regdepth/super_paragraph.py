import citations
from regdepth.paragraph import build_paragraph_tree

def build_super_paragraph_tree(text, label_fn):
    """Construct the tree for a section, appendix, or supplemental piece.
    label_fn takes the title as a parameter and creates the label for this
    tree node."""
    title = text[:text.find("\n")]
    text = text[len(title):]

    exclude = citations.internal_citations(text)
    label = label_fn(title)
    tree = build_paragraph_tree(text, exclude=exclude, label=label)

    tree['label']['title'] = title
    return tree

