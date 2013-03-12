import itertools
import re
import string
from utils import roman_nums

levels = [
        list(string.ascii_lowercase),
        list(range(1,51)),
        list(itertools.islice(roman_nums(), 0, 50)),
        list(string.ascii_uppercase)
        ]

def find_start(text, level, idx, exclude = []):
    """Find the position for the start of the requested label. Level is one
    of 0,1,2,3; idx is the element within that label. Return None if not
    present. Does not return results in the exclude list (a list of
    start/stop indecies). """
    if len(levels) <= level or len(levels[level]) <= idx:
        return None
    match_starts = [m.start() for m 
            in re.finditer("\(%s\)" % levels[level][idx], text)]
    match_starts = [m for m in match_starts
            if all([m < e[0] or m > e[1]  for e in exclude])]
    if match_starts:
        return match_starts[0]

def section_offsets(text, level, idx, exclude = []):
    """Find the start/end of the requested label. Assumes the text does not
    just up a level -- see @TODO@ below."""
    start = find_start(text, level, idx, exclude)
    end = find_start(text, level, idx + 1, exclude)
    if start == None:
        return None
    if end == None:
        end = len(text)
    return (start, end)
