# vim: set fileencoding=utf-8 :

from regdepth.section import *
from unittest import TestCase

class DepthSectionTest(TestCase):
    def test_find_next_section_start(self):
        text = u"\n\nSomething\n§ 205.3 thing\n\n§ 205.4 Something\n§ 203.19"
        self.assertEqual(12, find_next_section_start(text, 205))
        self.assertEqual(None, find_next_section_start(text, 204))
        self.assertEqual(45, find_next_section_start(text, 203))
    def test_next_section_offsets(self):
        """Should get the start and end of each section, even if it is
        followed by an Appendix or a supplement"""
        text = u"\n\n§ 201.3 sdsa\nsdd dsdsadsa \n asdsas\nSection\n"
        text += u"§ 201.20 dfds \n sdfds § 201.2 saddsa \n\n sdsadsa"
        self.assertEqual((2,45), next_section_offsets(text, 201))

        text = u"\n\n§ 201.3 sdsa\nsdd dsdsadsa \n asdsas\nSection\n"
        text += u"201.20 dfds \n sdfds § 201.2 saddsa \n\n sdsadsa"
        self.assertEqual((2,len(text)), next_section_offsets(text, 201))

        text = u"\n\n§ 201.3 sdsa\nsdd dsdsadsa \nAppendix A"
        self.assertEqual((2,29), next_section_offsets(text, 201))

        text = u"\n\n§ 201.3 sdsa\nsdd dsdsadsa \nSupplement I"
        self.assertEqual((2,29), next_section_offsets(text, 201))
    def test_sections(self):
        text = u"\n\n§ 201.3 sdsa\nsdd dsdsadsa \n asdsas\nSection\n"
        text += u"§ 201.20 dfds \n sdfds § 201.2 saddsa \n\n sdsadsa\n"
        text += u"Appendix A bssds \n sdsdsad \nsadad \ndsada"
        self.assertEqual([(2,45), (45,93)], sections(text, 201))
