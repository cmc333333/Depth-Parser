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
