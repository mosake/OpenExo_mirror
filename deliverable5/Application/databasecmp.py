import glob, os, xml.etree.ElementTree as ET

def get_names(xml_tree, tag):
    temp = []
    systems = xml_tree.getroot()
    if not xml_tree.findall(".//" + tag):
        temp.append('None')
    else:
        temp2 = []
        for system in systems:
            temp2.append(systems.findtext("name")) 
        temp.append(temp2)
    return temp


def matchXml(xml, repo):
    files=glob.glob(os.path.join(repo,"*.xml"))
    for file in files:
        try:
            newf = open(xml, 'r')
            repof = open(file, 'r')
        except InputError:
            print ("Invalid path")
            break
        filename = os.path.basename(file)
        repo_fname = ET.parse(repof)
        xml_fname = ET.parse(newf)
        tags = ["star", "system", "planet", "bplanet"]
        for tag in tags:
            if (compare(get_names(repo_fname, tag), get_names(xml_fname, tag))):
                return file  
    return None

'''
compare if one list element is in the other list
Ignore none cases
'''
def compare(list1, list2):
    for name1 in list1:
        if name1 == 'None':
            return False
        for name2 in list2:
            if name1==name2:
                return True
    return False
