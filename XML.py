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
    print(diff)
    # Write differences to CSV and return it
    ''' EVERYTHING IS WORKING, LEARN HOW TO CONVERT TO CSV '''
    ''' Idea: Column 1: Path, C2: Different Ele, C3: Approval(Y/N)'''
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

    if check_substructure(node):
        for child in node:
            if check_substructure(child):
                path[child.tag + "|" +
                     child.find("name").text + "|"] = recursing_child(child)
            else:
                path[child.tag] = child.text

    return path


def get_id(struct):
    ''' (dict) -> str
    Return the ID for the substructure
    '''
    return struct['name']


def compare_element(s1, s2):
    ''' (dict, dict) -> dict
    Compare the two structures and return the difference
    in a dictionary.
    '''
    diff = {}

    for i in s1:
        for j in s2:
            if isinstance(s1[i], dict) and isinstance(s2[j], dict):
                if get_id(s1[i]) == get_id(s2[j]):
                    diff[i] = compare_element(s1[i], s2[j])
                else:
                    diff[i] = [i + "[" + get_id(s1[i]) + "]",
                               j + "[" + get_id(s2[j]) + "]"]
                    diff[i] = [i + "|" + get_id(s1[i]),
                               i + "|" + get_id(s2[j])]
            else:
                if i == j and s1[i] != s2[j]:
                    diff[i] = [s1[i], s2[j]]

    return diff


def print_to_csv(file, struct):
    ''' (str, dict) -> None

    Take in a dictionary and file name, return the diff file with the
    given file name.
    '''
    f = open(file[0:-4] + '-diff.csv', 'w+')
    try:
        writer = csv.writer(f, delimiter=',')
        writer.writerow( ('Path','XML1','XML2','Approval') )
        l = generate_path(struct, [])
        for i in l:
            path = i.split("[")
            writer.writerow((path[0], path[1].split(",")))
    finally:
        f.close()


def generate_path(struct, l):
    ''' (dict, str) -> str

    Take in a struct and current path, return the path of each tag.
    '''
    for i in struct:
        if isinstance(struct[i], dict):
            l.extend(generate_path(struct[i], l))
        else:
            l.append(i + str(struct[i]))

    return l


main("system1.xml", "system2.xml")