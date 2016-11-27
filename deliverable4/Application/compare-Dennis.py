import xml.etree.ElementTree as ET
import csv
import copy

def main(xml1, xml2):
    ''' (str, str) -> None
    Main function, Calls the other functions to perform
    XML Comparison
    '''
    system1 = ET.parse(xml1)
    system2 = ET.parse(xml2)
    resultSys = copy.deepcopy(system1)

    # Getting the root of the xmls
    root1 = system1.getroot()
    root2 = system2.getroot()


    compare_element(root1, root2, resultSys.getroot())
    
    #newXML = compare_element(s1, s2)
    # Write differences to CSV and return it
    resultSys.write(xml1[0:-4] + "NEW" + ".xml")

def compare_element(xml1, xml2, result):
    '''
    TO DO, check for significant digits, decimal differences
    Change last update date to current date
    
    '''
    toChange = result.getchildren()
    compareTo = xml2.getchildren()
    original = xml1.getchildren()
    x1 = len(original)
    x2 = len(compareTo)
    
    sameSystem = False #Check if names match to see if it's the same system 
    for i in xml1.findall("./name"):
        for j in xml2.findall("./name"):
            if(i.text == j.text):
                sameSystem = True
    incr = 0
    missingTags = []
    if(sameSystem):    
        for i in range(0, x2):          
            isMissingTag = True
            isMismatch = False
            index = 0
            indexOriginal = 0
            for j in range(0, x1):
                if(compareTo[i].tag == original[j].tag and compareTo[i].text != original[j].text and not compareTo[i].tag == 'name'):
                    isMismatch = True
                    indexOriginal = j
                    index = i

                if(compareTo[i].tag == original[j].tag and compareTo[i].tag != 'name' or compareTo[i].text == original[j].text and compareTo[i].tag == 'name'):
                    isMissingTag = False
                if(len(original[j].getchildren()) >= 1 and len(compareTo[i].getchildren()) >= 1):
                    compare_element(original[j], compareTo[i], result[j + incr])
#Test if you have different sys name will it still compare, but name tag is last
            if (isMismatch):
                toChange[indexOriginal].text = compareTo[index].text
                toChange[indexOriginal].attrib = compareTo[index].attrib
            elif(isMissingTag):
                incr += 1
                missingTags.append(compareTo[i])
                result.insert(1, compareTo[i])
        
        for i in range(0, x2):
            isMissingBlock = True
            children = compareTo[i].getchildren()
            if(len(children) > 0):
                for first in compareTo[i].findall('name'):
                    for j in range(0, x1):
                        children2 = original[j].getchildren()   
                        if(len(children2) > 0):
                            for second in children2:
                                if first.text == second.text:
                                    isMissingBlock = False
            else:
                isMissingBlock = False
            if(isMissingBlock and compareTo[i] not in missingTags):
                result.insert(len(result.getchildren()), compareTo[i])
                



main("Kepler-25.xml", "Kepler-26.xml")