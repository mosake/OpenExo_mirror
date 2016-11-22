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
    diff = compare_element(s1, s2)

    # Write differences to CSV and return it
    print_to_csv(xml1, diff)


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
                    diff[i] = compare_element(s1[j], s2[i])
                #Otherwise, check if block missing
                else:
                    exist = False

                    for k in s1:
                        if isinstance(s1[k], dict):
                            if i in s2:
                                if get_id(s1[k], s2[i]) != "":
                                    exist = True

                    if exist == False:
                        diff[i + "|" + s2[i]['name'][0]] = ["",
                                   s2[i]['name'][0],
                                   "Missing"]
            else:
                #Check to see if block_id
                if i == j and i == 'name':
                    if get_id(s1, s2) == "":
                        diff[i] = [s1[i][0], s2[i][0], "Mismatch"]
                elif i == j and s1[i].lower() != s2[j].lower():
                    diff[i] = [s1[i], s2[i], "Mismatch"]

    return diff


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