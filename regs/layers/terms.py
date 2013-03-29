# vim: set fileencoding=utf-8 :
import string
from pyparsing import dblQuotedString, SkipTo
from regs.depth import tree

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
        if 'title' in child['label'] and 'definition' in child['label']['title'].lower():
            definition_children.append(child)
        if 'definition' in child['text'].lower():
            definition_children.append(child)
    return definition_children

def one_level_layer(node):
    """Build the definitions that apply only to this node."""
    layer = {}
    def add_to_layer(node):
        for term in parse_from(node['text']):
            layer[term] = node['label']['text']
    for child in children_with_defs(node):
        tree.walk(child, add_to_layer)
    return layer

def build_layer(reg_root):
    """Run one_level_layer for each node in the tree, linearize the results."""
    layer = {}
    def add_to_layer(node):
        sublayer = one_level_layer(node)
        if sublayer:
            layer[node['label']['text']] = sublayer
    tree.walk(reg_root, add_to_layer)
    return layer

