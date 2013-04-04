from regs import utils
from regs.depth import tree
from regs.depth.paragraph import ParagraphParser
from regs.depth.interpretation import carving
from regs.layers.links.interp_internal import comment_citations

def _mk_label(old_label, next_part):
    if old_label['text'].endswith(')'):
        return tree.extend_label(old_label, '-' + next_part, next_part)
    else:
        return tree.extend_label(old_label, '.' + next_part, next_part)
#   Can only be preceded by white space or a start of line
interpParser = ParagraphParser(r"(?<![^\s])%s\.", _mk_label)

def appendix_tree(text, label):
    """Build a tree representing an appendix interpretation (as opposed to
    an interpretation of a section)."""
    title, body = utils.title_body(text)
    label_text = 'Appendix ' + carving.get_appendix_letter(title)
    return interpParser.build_paragraph_tree(body, 1,
            comment_citations(body),
            label=tree.extend_label(label, label_text, label_text, title)
            )

def build(text, part):
    """Create a tree representing the whole interpretation."""
    title, body = utils.title_body(text)
    label = tree.label("%d-Interpretations" % part, [str(part), 
        "Interpretations"],
            title)
    appendix_offsets = carving.appendicies(body)
    appendicies = []
    if appendix_offsets:
        for start, end in appendix_offsets:
            appendicies.append(appendix_tree(body[start:end], label))
        body = body[:appendix_offsets[0][0]]

    sections = carving.sections(body, part)
    if sections:
        children = []
        for start, end in sections:
            section_text = body[start:end]
            children.append(section_tree(section_text, part, label))
        return tree.node(body[:sections[0][0]], children + appendicies, label)
    else:
        return tree.node(body, appendicies, label)

def section_tree(text, part, parent_label):
    """Tree representing a single section within the interpretation."""
    title, body = utils.title_body(text)
    section = carving.get_section_number(title, part)
    offsets = carving.applicable_offsets(body, section)
    label = tree.extend_label(parent_label, "-" + section, section, title)
    if offsets:
        children = []
        for start, end in offsets:
            applicable_text = body[start:end]
            children.append(applicable_tree(applicable_text, section, label))
        return tree.node(body[:offsets[0][0]], children, label)
    else:
        return tree.node(body, label=label)

def applicable_tree(text, section, parent_label):
    """Tree representing all of the text applicable to a single paragraph."""
    paragraph_header, body = utils.title_body(text)
    label_text = carving.build_label("", 
            carving.applicable_paragraph(paragraph_header, section))
    return interpParser.build_paragraph_tree(body, 1, comment_citations(body),
            label=tree.extend_label(parent_label, label_text, label_text,
                paragraph_header))
