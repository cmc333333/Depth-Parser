def label(text, parts, title=None):
    if title:
        return {'text': text, 'parts': parts, 'title': title}
    return {'text': text, 'parts': parts}
def extend_label(existing, text, part):
    return label(existing['text'] + text, existing['parts'] + [part])
def node(text='', children=[], label=label('',[])):
    return {'text': text, 'children': children, 'label': label}

