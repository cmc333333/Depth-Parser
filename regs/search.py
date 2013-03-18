import re
def find_start(text, heading, index):
    """Find the start of an appendix, supplement, etc."""
    match = re.search(r'^%s %s' % (heading, index), text, re.MULTILINE)
    if match:
        return match.start()

def find_offsets(text, search_fn):
    """Find the start and end of an appendix, supplement, etc."""
    start = search_fn(text)
    if start == None or start == -1:
        return None

    post_start_text = text[start+1:]
    end = search_fn(post_start_text)
    if end and end > -1:
        return (start, start + end + 1)
    else:
        return (start, len(text))
