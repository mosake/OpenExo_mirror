import xml.etree.ElementTree

def main():
    e = xml.etree.ElementTree.parse('test.xml').getroot()

    # Example of how to use
    #
    # XML:
    #
    #<foo>
    #  <bar>
    #     <type foobar="1"/>
    #     <type foobar="2"/>
    #  </bar>
    #</foo>
    #
    # Code:
    #
    #for atype in e.findall('type'):
    #   print(atype.get('foobar'))


    for planet in e.findall('planet'):
        print(planet.get('Name'))