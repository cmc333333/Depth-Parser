def label(text="", parts=[], title=None):
    if title:
        return {'text': text, 'parts': parts, 'title': title}
    return {'text': text, 'parts': parts}
_label = label

def extend_label(existing, text, part, title=None):
    return label(existing['text'] + text, existing['parts'] + [part], title)
def node(text='', children=[], label=None):
    if not label:
        label = _label('',[])
    return {'text': text, 'children': children, 'label': label}

def walk(node, fn):
    """Perform fn for every node in the tree. Pre-order traversal. fn must be a function
    that accepts a root node."""
    results = [fn(node)]
    for child in node['children']:
        results += walk(child, fn)
    return results
