import codecs
from regs.depth import build_regulation_tree
from regs.interpretation.layer import build
from xml.sax.saxutils import quoteattr

f = codecs.open('rege.txt', encoding='utf-8')
rege = unicode(f.read())
f.close()
f = codecs.open('interp.txt', encoding='utf-8')
interp = unicode(f.read())
f.close()

tree = build_regulation_tree(rege, 1005)
layer = build(interp, 1005)

f = codecs.open('rege.html', 'w', encoding='utf-8')
f.write(u'<html><meta charset="utf-8">')

def print_node(node):
    lab = node['label']['text']
    if lab in layer and 'interpretation' in layer[lab]:
        f.write("<a title=" + quoteattr(layer[lab]['interpretation'].strip()) + 
                " href='#not-done'>?</a>")
    if 'title' in node['label']:
        f.write('<h2>')
        f.write(node['label']['title'])
        f.write('</h2>')
        
    text = node['text']
    if lab in layer and 'keyterms' in layer[lab]:
        for term, interp in layer[lab]['keyterms']:
            text = text.replace(term, term + "<a title=" + quoteattr(interp.strip()) + 
                    " href='#not-done'>?</a>")
    f.write(text)
    if node['children']:
        f.write('<ol>')
        for child in node['children']:
            f.write('<li>')
            print_node(child)
            f.write('</li>')
        f.write('</ol>')

print_node(tree)

f.write('</html>')
f.close()

