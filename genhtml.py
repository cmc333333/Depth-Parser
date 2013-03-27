import codecs
import re
from regs.depth import build_regulation_tree, tree
from regs.depth.supplement import find_supplement_start
from regs.depth.interpretation.tree import build as build_interp_tree
from regs.layers import interpretation
from regs.terms import build_layer
from xml.sax.saxutils import quoteattr

f = codecs.open('rege.txt', encoding='utf-8')
rege = unicode(f.read())
f.close()

interp = rege[find_supplement_start(rege):]

rege_tree = build_regulation_tree(rege, 1005)
interp_tree = build_interp_tree(interp, 1005)
interp_layer = interpretation.build(interp_tree, 1005)
term_layer = build_layer(rege_tree)

import json 
print json.dumps(interp_tree['children'][14]['children'][1]['children'])

indexed_reg = {}
def index_tree(tree):
    indexed_reg[tree['label']['text']] = tree
tree.walk(rege_tree, index_tree)

indexed_interp = {}
def index_tree(tree):
    indexed_interp[tree['label']['text']] = tree
tree.walk(interp_tree, index_tree)

def as_text(tree):
    text = tree['text']
    for child in tree['children']:
        text = text + as_text(child)
    return text

f = codecs.open('rege.html', 'w', encoding='utf-8')
f.write(u'<html><meta charset="utf-8">')

import StringIO

doc = StringIO.StringIO(u'')
titles = []


def print_node(node, relevant_terms = None):
    lab = node['label']['text']
    if relevant_terms == None:
        relevant_terms = {}
    relevant_terms = relevant_terms.copy()
    if lab in term_layer:
        for term in term_layer[lab]:
            relevant_terms[term.lower()] = term_layer[lab][term]
    sorted_terms = sorted(relevant_terms.keys())
    sorted_terms.reverse()

    if lab in interp_layer and 'interpretation' in interp_layer[lab]:
        doc.write("<a title=__TITLE__%d" % len(titles) + " href='#not-done'>?</a>")
        titles.append(quoteattr(as_text(indexed_interp[interp_layer[lab]['interpretation']]).strip()))
    if 'title' in node['label']:
        doc.write('<h2>')
        doc.write(node['label']['title'])
        doc.write('</h2>')
        
    text = node['text']
    #   interpretations
    if lab in interp_layer and 'keyterms' in interp_layer[lab]:
        for term, interp in interp_layer[lab]['keyterms']:
            text = re.sub(r'(?i)\b' + term + r'\b', term + "<a title=__TITLE__%d href='#not-done'>" % len(titles) + 
                    "?</a>", text)
            titles.append(quoteattr(as_text(indexed_interp[interp]).strip()))
    #   definitions
    for term in sorted_terms:
        text = re.sub(r'(?i)\b' + term + r'\b', 
                '<a title=__TITLE__%d href="#not-done">' % len(titles) + term + '</a>', 
                text)
        titles.append(quoteattr(as_text(indexed_reg[relevant_terms[term]]).strip()))
    doc.write(text)
    if node['children']:
        doc.write('<ol>')
        for child in node['children']:
            doc.write('<li>')
            print_node(child, relevant_terms)
            doc.write('</li>')
        doc.write('</ol>')

print_node(rege_tree)

txt = doc.getvalue()
for i in range(len(titles)-1, -1, -1):
    txt = txt.replace('__TITLE__%d' % i, titles[i])
f.write(txt)
f.write('</html>')
f.close()

