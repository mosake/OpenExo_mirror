import xml.etree.ElementTree as ET
import csv

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
    big = {}
    small = {}
    source = 0
    if len(s1) > len(s2):
        big = s1
        small = s2
        source = 0
    else:
        big = s2
        small = s1
        source = 1

    diff = compare_element(big, small)

    # Write differences to CSV and return it
    print_to_csv(xml1, diff, source)


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


def get_id(struct):
    ''' (dict) -> list
    Return the ID for the substructure
    '''
    return struct['name']


def compare_id(s1, s2):
    ''' (list, list) -> bool

    Takes in a list of name and compare if name is in the list of names
    '''
    exist = False
    
    for i in s1:
        for j in s2:
            if i == j:
                exist = True
    return exist


def compare_element(s1, s2):
    ''' (dict, dict) -> dict
    Compare the two structures and return the difference
    in a dictionary.
    '''
    diff = {}

    for i in s1:
        for j in s2:
            if isinstance(s1[i], dict) and isinstance(s2[j], dict):
                if compare_id(get_id(s1[i]), get_id(s2[j])):
                    diff[i] = compare_element(s1[i], s2[j])
                else:
                    # FIX OUTPUT FILE NOT SHOWING MISSING BLOCK CORRECTLY
                    exist = False
                    for k in s2:
                        if isinstance(s2[k], dict):
                            if i in s1:
                                if compare_id(get_id(s1[i]), get_id(s2[k])):
                                    exist = True
                                    
                    if exist == False:
                        diff[i + "|" + get_id(s1[i])[0]] = [get_id(s1[i]),
                                   "",
                                   "Missing"]
                        
                    exist = False
                    for k in s1:
                        if isinstance(s1[k], dict):
                            if i in s2:
                                if compare_id(get_id(s2[i]), get_id(s1[k])):
                                    exist = True
                                    
                    if exist == False:
                        diff[j+ "|" + get_id(s2[j])[0]] = ["",
                                   get_id(s2[j]),
                                   "Missing"]                     
            else:
                if i == j and s1[i] != s2[j]:
                    diff[i] = [s1[i], s2[j], "Mismatch"]

    return diff


def print_to_csv(file, struct, source):
    ''' (str, dict) -> None

    Take in a dictionary and file name, return the diff file with the
    given file name.
    '''
    xml1 = 1
    xml2 = 2
    if source != 0:
        xml1 = 2
        xml2 = 1

    try:
        f = open(file[0:-4] + '-diff.csv', 'w+')
        writer = csv.writer(f, delimiter=',')
        writer.writerow( ('Path','Hanno','OutSource', 'Issue', 'Approval') )
        l = generate_path(struct, 'system')
        for i in l:
            i = i.replace(",", "[")
            path = i.split("[")
            writer.writerow((path[0], path[xml1], path[xml2], path[-1]))
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