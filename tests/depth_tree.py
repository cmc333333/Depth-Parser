from regs.depth.tree import *
from unittest import TestCase

class DepthTreeTest(TestCase):
    def test_walk(self):
        n1 = node("1")
        n2 = node("2")
        n3 = node("3")
        n4 = node("4")

        n1['children'] = [n2, n3]
        n2['children'] = [n4]

        order = []
        def add_node(n):
            order.append(n)
            return n['text']
        ret_val = walk(n1, add_node)
        self.assertEqual([n1, n2, n4, n3], order)
        self.assertEqual(["1", "2", "4", "3"], ret_val)
    def test_join_text(self):
        n1 = node("1")
        n2 = node("2")
        n3 = node("3")
        n4 = node("4")

        n1['children'] = [n2, n3]
        n2['children'] = [n4]

        self.assertEqual("1243", join_text(n1))
        self.assertEqual("24", join_text(n2))
        self.assertEqual("3", join_text(n3))
        self.assertEqual("4", join_text(n4))
