from regs.depth.interpretation import carving

def build(tree, part):
    """Build a layer - the map of labels to interpretation references."""
    layer = {}
    for child in [cc for c in tree['children'] for cc in c['children']]:
        part, _, section, _ = child['label']['parts']
        if child['children'] or child['text'].strip():
            add_to_layer("%s.%s" % (part, section), child, layer)
    return layer

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

def add_to_layer(label_prefix, node, layer):
    """Adds the appropriate element to the layer."""
    parsed_match = carving.applicable_paragraph(node['label']['title'],
        node['label']['parts'][2])
    label = carving.build_label(label_prefix, parsed_match)
    layer[label] = build_element(parsed_match, node['label']['text'], 
            layer.get(label, {}))
