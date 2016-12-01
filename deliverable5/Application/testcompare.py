import compare as c
import unittest
import filecmp
import xml.etree.ElementTree as ET

# Cannot test to see if these are correct because I get
# this error when running compare:
#     import xmltools
# builtins.ImportError: No module named 'xmltools'

class TestCompare(unittest.TestCase):

    def test_compare(self):
        c.main("Kepler-25.xml", "Kepler-26.xml")
        self.assertTrue(filecmp.cmp("test.xml", "Kepler-25New.xml"))


    def test_binaryCheck(self):
        if not (xml1 == None):
            system1 = ET.parse(xml1)
        system2 = ET.parse(xml2)
        root1 = system1.getroot()
        root2 = system2.getroot()
        assertEqual(False, c.binaryCheck(root1, root2))


    def test_checkName(self):
        if not (xml1 == None):
            system1 = ET.parse(xml1)
        system2 = ET.parse(xml2)
        root1 = system1.getroot()
        root2 = system2.getroot()
        assertEqual(True, c.checkName(root1, root2))



if __name__ == '__main__':
    unittest.main()


