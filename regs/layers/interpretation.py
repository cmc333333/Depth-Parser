import re
from regs.depth.interpretation import carving

def build(tree, part, ontop_of = None):
    """Build a layer - the map of labels to interpretation references."""
    if ontop_of == None:
        ontop_of = {}
    for child in tree['children']:
        part = child['label']['parts'][0]
        section = child['label']['parts'][2]
        if len(child['label']['parts']) == 3 and section.isdigit():
            build(child, part, ontop_of)
        elif child['children'] or child['text'].strip():
            add_to_layer("%s.%s" % (part, section), child, ontop_of)
    return ontop_of

def build_element(match, interp, ontop_of=None):
    """
    Build an element, a map with possible values for 'keyterms' and
    'interpreation'.  ontop_of is a parameter used if building on top an
    existing map. Match is a pyparsing match.
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

def add_to_layer(label_prefix, node, layer):
    """Adds the appropriate interpretation/keyterm to the layer."""
    parsed_match = carving.applicable_paragraph(node['label']['title'],
        node['label']['parts'][2])
    if parsed_match:
        label = carving.build_label(label_prefix, parsed_match)
        layer[label] = build_element(parsed_match, node['label']['text'], 
                layer.get(label, {}))
    appendix_match = re.match(ur"Appendix ([A-Z])", node['label']['title'])
    if appendix_match:
        label = label_prefix + appendix_match.group(1)
        layer[label] = {"interpretation": node['label']['text']}
