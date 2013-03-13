import citations
import depth
import json

pt_file = open('205.14.txt')
pt = pt_file.read()
pt_file.close()

exclude = citations.internal_citations(pt)
tree = depth.build_section_tree(pt, exclude=exclude)

"""
out_file = open('205.14.json', 'w')
out_file.write(json.dumps(tree))
out_file.close()
"""

def print_node(node):
    print node['text']
    if node['children']:
        print '<ol>'
        for child in node['children']:
            print '<li>'
            print_node(child)
            print '</li>'
        print '</ol>'

print_node(tree)
