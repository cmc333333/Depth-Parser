import re
def find_start(text, heading, index):
    """Find the start of an appendix, supplement, etc."""
    match = re.search(r'^%s %s' % (heading, index), text, re.MULTILINE)
    if match:
        return match.start()
