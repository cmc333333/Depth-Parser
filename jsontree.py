import codecs
import json
from regs.depth.appendix.tree import trees_from
from regs.depth.reg_text import build_reg_text_tree
from regs.depth.supplement import find_supplement_start
from regs.depth.interpretation.tree import build as build_interp_tree

f = codecs.open('rege.txt', encoding='utf-8')
rege = unicode(f.read())
f.close()

interp = rege[find_supplement_start(rege):]

rege_tree = build_reg_text_tree(rege, 1005)
interp_tree = build_interp_tree(interp, 1005)
appendix_trees = trees_from(rege, 1005, rege_tree['label'])

f = codecs.open('rege.json', 'w', encoding='utf-8')
f.write(json.dumps({
    "reg_text": rege_tree, 
    'appendices': appendix_trees,
    'interpretation': interp_tree
    }))
f.close()

