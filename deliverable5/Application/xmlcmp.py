'''
ASSUMPTIONS MADE:
xml1 given to main is from Hano's OEC





INSTRUCTIONS:

1) Call main("", "")

2) The input parameters will take in source file (1st parameter),
   and outsource file (2nd Parameter).
   (I.e. main("hanno.xml", "nasa.xml")

3) xmlcmp.py will output a csv file into the same directory.

4) Open csv file and the difference will be listed in there.

5) Columns represents the information:
> | Path | Source | Outsource | Issue | Approval |

Path: The xml tag location in the XML
Source: The value of the tag in the source file
Outsource: The value of the tag in the outsource file
Issue: Display the type of difference
Approval: Status of change

'''


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

    # Getting the root of the xmls
    root1 = system1.getroot()
    root2 = system2.getroot()

    # Getting the structure of the xml file
    s1 = {}
    s2 = {}
    s1[root1.tag] = recursing_child(root1)
    s2[root2.tag] = recursing_child(root2)

        # Output the differences
    diff = compare_element(s1, s2)
    #newXML = compare_element(s1, s2)
    # Write differences to CSV and return it
    print_to_csv(xml1, diff)
    newXML = copy.deepcopy(system1)
    newXML = changeXML(diff, newXML, system2) #Don't need deep copy of sys2, only changing first one
    newXML.write(xml1[0:-4] + "NEW" + ".xml")


def check_substructure(node):
    ''' (node) -> bool
    Return true if a tag contains substructure. False, otherwise.
    '''
    substructure = False
    for child in node:
        substructure = True

    return substructure


def recursing_child(node):
    ''' (xml node) -> list
    Return the path of every child element of the node (including their substructure).
    '''
    path = {}
    #Initialize name
    path['name'] = []

    if check_substructure(node):
        for child in node:
            if check_substructure(child):
                path[child.tag + "|" +
                     child.find("name").text + "|"] = recursing_child(child)
            else:
                # If name tag, add to list for multi-name
                if child.tag == "name":
                    path[child.tag].append(child.text)
                else:
                    path[child.tag] = child.text

    return path


def get_id(l1, l2):
    ''' (list) -> str
    Return the ID for the substructure
    '''
    key = ""

    try:
        for i in l1['name']:
                for j in l2['name']:
                    if i == j:
                        key = i
    except:
        print("One of the XML is missing name tag")
        pass

    return key


def compare_element(s1, s2):
    ''' (dict, dict) -> dict
    Compare the two structures and return the difference
    in a dictionary.
    '''
    diff = {}

    for i in s2:
        for j in s1:
            if isinstance(s1[j], dict) and isinstance(s2[i], dict):
                #Initialize the block ID
                block_id = get_id(s1[j], s2[i])

                #If the block has a matching ID, then compare substructure
                if  block_id != "":
                    diff[j] = compare_element(s1[j], s2[i])
                #Otherwise, check if block missing
                else:
                    exist = False

                    for k in s1:
                        if isinstance(s1[k], dict):
                            if i in s2:
                                if get_id(s1[k], s2[i]) != "":
                                    exist = True

                    if exist == False:
                        diff[i] = ["",
                                   s2[i]['name'][0],
                                   "Missing Block"]
            else:
                #Check to see if block_id
                if i == j and i == 'name':
                    if get_id(s1, s2) == "":
                        diff[i] = [s1[i][0], s2[i][0], "Mismatch"]
                elif i == j and s1[i] != s2[j]:
                    diff[i] = [s1[i], s2[i], "Mismatch"]

        #Check if missing tag
        if i not in s1:
            if i not in diff:
                diff[i] = ["", "<" + i + ">", "Missing Tag"]

    return diff


def changeXML(diff, xml1, xml2):
    '''
    condition = 1 -> Missing block, add entire missing block in
    condition = 2 -> Different value. Nee
    condition = 3 -> Missing tag, add tag and value 
    xml2 is not a deepcopy, do not modify
    '''
    root = xml1.getroot()
    l = generate_path(diff, 'system')
    for i in l:
        m = i.replace(",", "[").split("[")     #First value = location, second = OEC value, third = external db value, fourth = type (mismatch , missing tag, missing block)
        #m[n] maybe be empty as some have || so split has space        
        location = m[0].split("|")            
        
        a = "system|star|KOI-244|['', '<star|KOI-244|>', 'Missing Tag'"
        b= "star|Kepler-25||magR['', '<magR>', 'Missing Tag'"
        c = "planet|Kepler-25 c||eccentricity['', '<eccentricity>', 'Missing Tag'"
        
        
        if(m[len(m) - 1] == " 'Mismatch'" and i == "asdf"):
            if not(m[2][1:] == "None"):
                temp = find(root, location, m[1][1:-1], True)
                    
                    
                temp.text = m[2][2:-1]  
        elif(m[len(m) - 1] == " 'Missing Tag'" and i == c):
            missingTag = find(xml2.getroot(), location, "", False)
            #addTo = find(root, location, "", False)
               
            #addTo.insert(1, missingTag)
            print(missingTag.tag)
           # print(addTo.tag)
            print(location)
        elif(m[len(m) - 1] == " 'Missing Block'"):
            print("MISSING BLOCK")
    
    return xml1

def find(xml, location, value, isMismatch):

    child = xml
    temp = xml

    print(xml)
    print(location)
#attributes need to change , err
#Significant digits

    if (len(location) >= 1):        
        if(location[0] == "" or location[0] == "system"):
            return find(xml, location[1:], value, isMismatch)
        n = location[0]
        for i in xml.findall("./" + n): #If name then will not be found
            if(i.tag == n):
                print("First for")
                print(i.tag)
                temp = find(i, location[1:], value, isMismatch)
                print("FOUND")
                print(temp.tag)
                print(location)
                if(temp.text == value or (not isMismatch and len(location) == 1)):
                    print("FOR IF")
                    return temp
        child = temp
        for i in xml.findall("./"):
            print("LOOP")
            print(i)
            print(i.text)
            print(n)
            if(i.text == n):
                print("FIRSTIF")
                print(i.text)
                print(location)
                #KOI-44 (value of name is last)
                if not isMismatch and len(location) == 2: 
                    
                    print("NOT MISMATCH")
                    print(i.text)
                    return i
                child = find(xml, location[1:], value, isMismatch)
            elif(i.tag == n):
                print("SECOND IF")
                if not isMismatch and location[len(location) - 1] == '':
                    print("SECOND NOT MISMATCH")
                    return i
                child = find(xml, location[1:], value, isMismatch)

    return child












def print_to_csv(file, struct):
    ''' (str, dict) -> None

    Take in a dictionary and file name, return the diff file with the
    given file name.
    '''
    try:
        f = open(file[0:-4] + '-diff.csv', 'w+')
        writer = csv.writer(f, delimiter=',')
        writer.writerow( ('Path','Hanno','OutSource', 'Issue', 'Approval') )
        l = generate_path(struct, 'system')
        for i in l:
            i = i.replace(",", "[")
            path = i.split("[")
            writer.writerow((path[0], path[1], path[2], path[-1]))
    finally:
        print("Result has been printed in csv.")
        f.close()


def generate_path(struct, path):
    ''' (dict, list, str) -> str

    Take in a struct and current path, return the path of each tag.
    '''
    l = []

    for i in struct:
        if isinstance(struct[i], dict):
            l.extend(generate_path(struct[i], i))
        else:
            if "[" in i:
                l.append(str(struct[i]).replace("]", ""))
            else:
                l.append(path + "|" + i + str(struct[i]).replace("]", ""))

    return l

main("kepler-25.xml", "kepler-26.xml")