import itertools
import re
from regs.depth import tree
from regs.search import segments
from regs.utils import roman_nums
import string

p_levels = [
    list(string.ascii_lowercase),
    [str(i) for i in range(1,51)],
    list(itertools.islice(roman_nums(), 0, 50)),
    list(string.ascii_uppercase),
    #   Technically, there's italics (alpha) and (roman), but we aren't
    #   handling that yet
]
class ParagraphParser():
    def __init__(self, p_regex, inner_label_fn):
        """p_regex is the regular expression used when searching through paragraphs. It
        should contain a %s for the next paragraph 'part' (e.g. 'a', 'A', '1', 'i',
        etc.) inner_label_fn is a function which takes the current label, and the next
        paragraph 'part' and produces a new label."""
        self.p_regex = p_regex
        self.inner_label_fn = inner_label_fn

    def matching_subparagraph_ids(self, p_level, paragraph):
        """Return a list of matches if this paragraph id matches one of the subparagraph
        ids (e.g.  letter (i) and roman numeral (i)."""
        matches = []
        for depth in range(p_level+1, len(p_levels)):
            for sub_id, sub in enumerate(p_levels[depth]):
                if sub == p_levels[p_level][paragraph]:
                    matches.append((depth, sub_id))
        return matches

    def best_start(self, text, p_level, paragraph, starts, exclude = []):
        """Given a list of potential paragraph starts, pick the best based on knowledge of
        subparagraph structure. Do this by checking if the id following the subparagraph
        (e.g. ii) is between the first match and the second. If so, skip it, as that
        implies the first match was a subparagraph."""
        subparagraph_hazards = self.matching_subparagraph_ids(p_level, paragraph)
        starts = starts + [len(text)]
        for i in range(1, len(starts)):
            s_text = text[starts[i-1]:starts[i]]
            s_exclude = [(e[0] + starts[i-1], e[1] + starts[i-1]) for e in exclude]
            is_subparagraph = False
            for hazard_level, hazard_idx in subparagraph_hazards:
                if self.find_paragraph_start(s_text, hazard_level, hazard_idx + 1,
                        s_exclude):
                    is_subparagraph = True
            if not is_subparagraph:
                return starts[i-1]

    def find_paragraph_start(self, text, p_level, paragraph, exclude = []):
        """Find the position for the start of the requested label. p_Level is one
        of 0,1,2,3; paragraph is the index within that label. Return None if not
        present. Does not return results in the exclude list (a list of
        start/stop indices). """
        if len(p_levels) <= p_level or len(p_levels[p_level]) <= paragraph:
            return None
        match_starts = [m.start() for m 
                in re.finditer(self.p_regex % p_levels[p_level][paragraph], text)]
        match_starts = [m for m in match_starts
                if all([m < e[0] or m > e[1]  for e in exclude])]

        if len(match_starts) == 0:
            return None
        elif len(match_starts) == 1:
            return match_starts[0]
        else:
            return self.best_start(text, p_level, paragraph, match_starts, exclude)

    def paragraph_offsets(self, text, p_level, paragraph, exclude = []):
        """Find the start/end of the requested paragraph. Assumes the text does 
        not just up a p_level -- see build_paragraph_tree below."""
        start = self.find_paragraph_start(text, p_level, paragraph, exclude)
        end = self.find_paragraph_start(text, p_level, paragraph + 1, exclude)
        if start == None:
            return None
        if end == None:
            end = len(text)
        return (start, end)

    def paragraphs(self, text, p_level, exclude = []):
        """Return a list of paragraph offsets defined by the level param."""
        def offsets_fn(remaining_text, p_idx, exclude):
            return self.paragraph_offsets(remaining_text, p_level, p_idx, exclude)
        return segments(text, offsets_fn, exclude)


    def build_paragraph_tree(self, text, p_level = 0, exclude = [], 
            label = tree.label("", [])):
        """
        Build a dict to represent the text hierarchy.
        """
        subparagraphs = self.paragraphs(text, p_level, exclude)
        if subparagraphs:
            body_text = text[0:subparagraphs[0][0]]
        else:
            body_text = text

        children = []
        for paragraph, (start,end) in enumerate(subparagraphs):
            new_text = text[start:end]
            new_excludes = [(e[0] - start, e[1] - start) for e in exclude]
            new_label = self.inner_label_fn(label, p_levels[p_level][paragraph])
            children.append(self.build_paragraph_tree(new_text, p_level + 1,
                new_excludes, new_label))
        return tree.node(body_text, children, label)

