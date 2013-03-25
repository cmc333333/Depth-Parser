from regs import utils
from regs.interpretation import chunking


def build(text, part):
    """Build a layer - the map of labels to interpretations."""
    sects = chunking.sections(text, part)
    layer = {}
    for start, end in sects:
        sect_text = text[start:end]
        title, body = utils.title_body(sect_text)
        section = chunking.get_section_number(title, part)
        chunk_pairs = chunking.split_by_header(body, section)
        add_to_layer("%d.%s" % (part, section), chunk_pairs, layer)
    return layer

def build_label(label_prefix, match):
    """Create a string to represent this label based on the pyparsing match."""
    label = str(label_prefix)   # copy
    for p in range(1,5):
        attr = 'paragraph' + str(p)
        if getattr(match, attr):
            label += "(" + getattr(match, attr).id + ")"
    return label

def build_element(match, interp, ontop_of=None):
    """
    Build an element, a map with possible values for 'keyterms' and 'interpreation'.
    ontop_of is a parameter used if building on top an existing map. Match is a
    pyparsing match.
    """
    if not ontop_of:
        ontop_of = {}
    if match.keyterm:
        keyterms = ontop_of.get("keyterms", [])
        keyterms.append((match.keyterm.term, interp))
        ontop_of["keyterms"] = keyterms
    else:
        ontop_of["interpretation"] = interp
    return ontop_of

def add_to_layer(label_prefix, chunk_pairs, layer):
    """Adds the appropriate element to the layer."""
    for header_match, text in chunk_pairs:
        _, interp = utils.title_body(text)
        if not interp.strip() == '':
            label = build_label(label_prefix, header_match)
            layer[label] = build_element(header_match, interp, layer.get(label, {}))
