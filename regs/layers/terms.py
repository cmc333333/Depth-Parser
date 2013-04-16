# vim: set fileencoding=utf-8 :
from pyparsing import dblQuotedString, SkipTo
import re
from regs.depth import tree
from regs.utils import flatten
import string

smart_quotes = (u'“' + SkipTo(u'”')).setParseAction(lambda s,l,t: t[1])
term_parser = smart_quotes #   will eventually include italic text, etc.

def parse_from(text):
    """Return the terms out of any definitions found in the text."""
    matches = term_parser.scanString(text)
    return [match[0] for match,_,_ in matches]

def children_with_defs(node):
    """Find the immediate children of the node which contain definitions."""
    definition_children = []
    for child in node['children']:
        if 'title' in child['label'] and (
                'definition' in child['label']['title'].lower()):
            definition_children.append(child)
        if 'definition' in child['text'].lower():
            definition_children.append(child)
    return definition_children

def applicable_definitions(node):
    """Find the definitions which apply to this node. Return definitions in
    descreasing order by term length (containing terms come first)."""
    definitions = []
    def add_to_defs(node):
        for term in parse_from(node['text']):
            definitions.append((term.lower(), node['label']['text'],
                    tree.join_text(node)))
    for child in children_with_defs(node):
        tree.walk(child, add_to_defs)
    return sorted(definitions, key=lambda d: -1 * len(d[0]))

def term_structs(text, term_by_refs):
    """Search for the definitions in this chunk of text. If found, make sure
    the term isn't already contained in a different term, then add it to the
    list of term structures."""
    structs = []
    existing_defs = []
    for term, ref in term_by_refs:
        offsets = [(m.start(), m.end()) for m in
                re.finditer(ur'\b' + re.escape(term) + ur'\b', text.lower())]
        safe_offsets = []
        for start, end in offsets:
            if any(start >= e[0] and start <= e[1] for e in existing_defs):
                continue
            if any(end >= e[0] and end <= e[1] for e in existing_defs):
                continue
            safe_offsets.append((start, end))
        if not safe_offsets:
            continue

        existing_defs.extend(safe_offsets)
        structs.append({"ref": ref, "offsets": safe_offsets})
    return structs

def tighten_scope(structs, reference):
    """To correctly handle later definitions replacing earlier ones, remove
    any term which is later repeated."""
    final_structs = []
    terms = [reference[s['ref']]['term'] for s in structs]
    for idx, s in enumerate(structs):
        if not terms[idx] in terms[idx+1:]:
            final_structs.append(s)
    return final_structs

def referencify(existing, definitions):
    """Add all the definitions to the definition list. Return a list of
    references to those definitions"""
    term_refs = []
    for term, ref, definition in definitions:
        term_ref = term + ':' + ref
        existing[term_ref] = {
                "term": term,
                "reference": ref,
                "text": definition
        }
        term_refs.append((term, term_ref))
    return term_refs


def add_to_layer(node, layer):
    """Find all of the terms that apply to this node and its children. For
    this and all children, add their term structs to the layer."""
    definitions = tree.walk(node, applicable_definitions)
    definitions = flatten(definitions)
    if not definitions:
        return
    term_by_refs = referencify(layer['referenced'], definitions)
    def per_node(child):
        structs = term_structs(child['text'], term_by_refs)
        if structs:
            existing = layer.get(child['label']['text'], [])
            structs = existing + structs
            layer[child['label']['text']] = tighten_scope(structs,
                layer['referenced'])
    tree.walk(node, per_node)


def build(root):
    """Build the terms layer. This provides start/end positions of a keyterm
    along with its definition and a reference to that definition."""
    layer = {'referenced': {}}
    tree.walk(root, lambda n: add_to_layer(n, layer))
    return layer
