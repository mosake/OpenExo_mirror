import xml.etree.ElementTree as ET
import xmltools
import os
import copy
'''
Assumptions made, xml1 is Hano's filie, xml2 is from exsternal catalogue.
If xml1 is none then just create new file as xml2


'''
def main(xml1, xml2):
    ''' (str, str) -> None
    Main function, Calls the other functions to perform
    XML Comparison
    '''
    if not (xml1 == None):
        system1 = ET.parse(xml1)
    system2 = ET.parse(xml2)
    resultSys = copy.deepcopy(system1)

    if not (xml1 == None):
        # Getting the root of the xmls
        root1 = system1.getroot()
        root2 = system2.getroot()        
        compare_element(root1, root2, resultSys.getroot(), False)
    
    #newXML = compare_element(s1, s2)
    # Write differences to CSV and return it
    xmltools.ensure_empty_dir(os.path.join(os.path.curdir,"Changed_Systems"))
    outputfilename = os.path.join(os.path.curdir,"Changed_Systems",xml1[0:-4] + ".xml")
    resultSys.write(outputfilename)
    return outputfilename

def compare_element(xml1, xml2, result, isBinary):
    '''
    TO DO, check for significant digits, decimal differences
    Change last update date to current date
    
    '''    
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
    binary = xml1.findall("binary")
    resultBinary = result.findall("binary")
    if(len(binary) > 0):
        for i in range (0, len(binary)):
            stars = binary[i].findall("./star")
            resultStars = resultBinary[i].findall("./star")        
            for stars2 in xml2.findall("./star"):
                starExist = False
                for j in range(0, len(stars)):
                    if(binaryCheck(stars[j] , stars2)):   
                        starExist = True                       
                        compare_element(stars[j], stars2, resultStars[j], True)
                if not starExist:
                    #Add missing star block 
                    resultBinary[i].insert(len(resultBinary[i].getchildren()), stars2)
                    
       
#Flip it around? loop from second one and check if all stars are in
                        
    elif(sameSystem or isBinary): 
        toChange = result.getchildren()
        
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
                if(compareTo[i].tag == original[j].tag and compareTo[i].tag != 'name'):
                        isMissingTag = False
                if(len(original[j].getchildren()) >= 1 and len(compareTo[i].getchildren()) >= 1):           

                    compare_element(original[j], compareTo[i], result[j + incr], False)

            if (isMismatch):
                toChange[indexOriginal].text = compareTo[index].text
                toChange[indexOriginal].attrib = compareTo[index].attrib
            elif(isMissingTag):
                incr += 1
                missingTags.append(compareTo[i])
                result.insert(1, compareTo[i])
                
        if not (binary):
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
                

def binaryCheck(sys1 ,sys2):
    isSame = False
    #SYS1 currently is binary, if it is a binary find all stars
    for planet1 in sys1.findall('planet'):
        for planet2 in sys2.findall('planet'):
            if(checkName(planet1, planet2)):
                isSame = True
    return isSame

def checkName(sys1, sys2):
    sameSystem = False
    for i in sys1.findall("./name"):
        for j in sys2.findall("./name"):
            if(i.text == j.text):
                sameSystem = True
    return sameSystem


main("Kepler-68.xml", "NASA_Kepler-68.xml")
=======
import xml.etree.ElementTree as ET
import xmltools
import os
import copy
import ntpath
'''
Assumptions made, xml1 is Hano's filie, xml2 is from external catalogue.
If xml1 is none then just create new file as xml2


'''
def main(xml1, xml2, dest = "."):
    ''' (str, str, str) -> None
    Main function, Calls the other functions to perform
    XML Comparison. Dest is optional parameter to specify which
    directory the modified XMLs will be saved into
    '''
    if not (xml1 == None): 
        fileName = ntpath.basename(xml1) #get filename from abs path
        outputfilename = os.path.join(dest, fileName)
        system1 = ET.parse(xml1)
        resultSys = copy.deepcopy(system1)
        system2 = ET.parse(xml2)
        # Getting the root of the xmls
        root1 = system1.getroot()
        root2 = system2.getroot()        
        compare_element(root1, root2, resultSys.getroot(), False)
        resultSys.write(outputfilename)
    else: #does not exist in local repo
        system2 = ET.parse(xml2)
        fileName = ntpath.basename(xml2) #get filename from abs path
        fileName = fileName.split("_")[1] #remove source from file name e.g. NASA_KOI-1.xml
        outputfilename = os.path.join(dest, fileName)
        system2.write(outputfilename)
    return outputfilename

def compare_element(xml1, xml2, result, isBinary):
    '''
    TO DO, check for significant digits, decimal differences
    Change last update date to current date
    
    '''    
    compareTo = xml2.getchildren()
    original = xml1.getchildren()
    x1 = len(original)
    x2 = len(compareTo)
    
    #check if names of given xmls match
    sameSystem = checkName(xml1,xml2)
    incr = 0
    missingTags = []
    binary = xml1.findall("binary")
    resultBinary = result.findall("binary")
    #Only run if there is a binary tag
    if(len(binary) > 0):
        for i in range (0, len(binary)):
            stars = binary[i].findall("./star")
            resultStars = resultBinary[i].findall("./star")        
            for stars2 in xml2.findall("./star"):
                starExist = False
                for j in range(0, len(stars)):
                    #Check if it is the same two stars
                    if(binaryCheck(stars[j] , stars2)):   
                        starExist = True                       
                        compare_element(stars[j], stars2, resultStars[j], True)
                if not starExist:
                    #Add missing star block into binary
                    resultBinary[i].insert(len(resultBinary[i].getchildren()), stars2)
                                            
    elif(sameSystem or isBinary): 
        toChange = result.getchildren()
        #Loop through external database tags
        for i in range(0, x2):          
            isMissingTag = True
            isMismatch = False
            index = 0
            indexOriginal = 0
            #Loop through Hano's tags
            for j in range(0, x1):
                #Check if it is a mismatch
                if(compareTo[i].tag == original[j].tag and compareTo[i].text != original[j].text and not compareTo[i].tag == 'name'):
                    isMismatch = True
                    indexOriginal = j
                    index = i
                #Check if it is a missing tag
                if(compareTo[i].tag == original[j].tag):
                        isMissingTag = False
                #Only run if there are children. IE. they are stars
                if(len(original[j].getchildren()) >= 1 and len(compareTo[i].getchildren()) >= 1):           
                    #Result may have added missing tags, need to compensate by 
                    #adding number of missingTags to index value
                    compare_element(original[j], compareTo[i], result[j + incr], False)
            
            #Only change text and attributes for mismatch
            if (isMismatch):
                toChange[indexOriginal].text = compareTo[index].text
                toChange[indexOriginal].attrib = compareTo[index].attrib
            elif(isMissingTag):
                #Need to increment pointer as insertion for missing tags is done
                #at the begining. 
                incr += 1
                missingTags.append(compareTo[i])
                result.insert(1, compareTo[i])
                
        if not (binary):
            #Check for missing blocks
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
                

def binaryCheck(sys1 ,sys2):
    '''
    sys1 currently is a binary, check the planets of it's stars with sys2.
    Return true only if the names of the planets in the given stars match up
    '''
    isSame = False
    for planet1 in sys1.findall('planet'):
        for planet2 in sys2.findall('planet'):
            if(checkName(planet1, planet2)):
                isSame = True
    return isSame

def checkName(sys1, sys2):
    '''
    Returns True if Names of the two given systems match
    '''
    sameSystem = False
    for i in sys1.findall("./name"):
        for j in sys2.findall("./name"):
            if(i.text == j.text):
                sameSystem = True
    return sameSystem
