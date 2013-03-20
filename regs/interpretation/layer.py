from regs import utils
from regs.interpretation import chunking


def build(text, part):
    """Build a layer - the map of labels to interpretations."""
    interps = chunking.interpretations(text, part)
    layer = {}
    for start, end in interps:
        interp_text = text[start:end]
        title, body = utils.title_body(interp_text)
        section = chunking.get_section(title, part)
        chunk_pairs = chunking.split_by_header(body, section)
        add_to_layer("%d.%s" % (part, section), chunk_pairs, layer)
    return layer

def build_label(label_prefix, match):
    label = label_prefix
    for p in range(1,5):
        attr = 'paragraph' + str(p)
        if getattr(match, attr):
            label += "(" + getattr(match, attr).id + ")"
    return label

def build_element(match, interp, element):
    if match.keyterm:
        keyterms = element.get("keyterms", [])
        keyterms.append((match.keyterm.term, interp))
        element["keyterms"] = keyterms
    else:
        element["interpretation"] = interp
    return element

def add_to_layer(label_prefix, chunk_pairs, layer):
    for header_match, text in chunk_pairs:
        _, interp = utils.title_body(text)
        if not interp.strip() == '':
            label = build_label(label_prefix, header_match)
            layer[label] = build_element(header_match, interp, layer.get(label, {}))
