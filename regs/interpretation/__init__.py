from regs import search, utils
from regs.interpretation import headers

def find_next_interpretation_offsets(text, part):
    """Find the start/end of the next interpretation"""
    def find_start(text):
        return search.find_start(text, u"Section", ur"%d.\d+" % part)
    return search.find_offsets(text, find_start)

def interpretations(text, part):
    """Return a list of interpretation offsets."""
    def offsets_fn(remaining_text, idx, excludes):
        return find_next_interpretation_offsets(remaining_text, part)
    return search.segments(text, offsets_fn)

def build_layer(text, part):
    """Build a layer - the map of labels to interpretations."""
    interps = interpretations(text, part)
    layer = {}
    for start, end in interps:
        interp_text = text[start:end]
        title, body = utils.title_body(interp_text)
        section = headers.get_section(title, part)
        header_offsets = headers.parse(body, section)
        add_to_layer("%d.%s" % (part, section), header_offsets, body, layer)
    return layer

def build_label(label_prefix, match):
    label = label_prefix
    for p in range(1,5):
        attr = 'paragraph' + str(p)
        if getattr(match, attr):
            label += "(" + getattr(match, attr).id + ")"
    return label

def build_layer_element(match, interp, element):
    if match.keyterm:
        keyterms = element.get("keyterms", [])
        keyterms.append((match.keyterm.term, interp))
        element["keyterms"] = keyterms
    else:
        element["interpretation"] = interp
    return element

def add_to_layer(label_prefix, header_offsets, text, layer):
    last_offset = (None, len(text), None)
    header_offsets = header_offsets + [last_offset]
    for i in range(1, len(header_offsets)):
        match, start, _ = header_offsets[i-1]
        _, next_start, _ = header_offsets[i]
        interp = text[start:next_start]
        _, commentary = utils.title_body(text[start:next_start])
        label = build_label(label_prefix, match)
        layer[label] = build_layer_element(match, interp, layer.get(label, {}))
