import re
from regs.depth import tree
from regs.layers.links.reg_internal import internal_citations

def model_start(text):
    """Search through the text to determine where a model form begins.
    Return the offsets."""
    periods = [m.start() for m in re.finditer('\.', text)]
    exclude = internal_citations(text)
    periods = [p for p in periods if all(
        [p < start or p > end for start, end in exclude])]
    if periods:
        return periods[0] + 1
    else:
        return len(text)

def process_node(node, layer):
    """Look for nodes with 'Model' and internal citations in their title.
    When found, figure out where the model form begins and ends."""
    title = node['label'].get('title', '')
    if 'Model' not in title or not internal_citations(title):
        return

    if not node['children']:
        layer[node['label']['text']] = { "offsets": [(0, len(node['text']))] }
    for child in node['children']:
        start = model_start(child['text'])
        joined = tree.join_text(child)
        layer[child['label']['text']] = { "offsets": [(start, len(joined))] }

def build(root):
    """Build the model form layer. This provides start/end positions of when
    the model form begins (and hence we shouldn't format it) and when it
    ends."""
    layer = {}
    tree.walk(root, lambda n: process_node(n, layer))
    return layer
