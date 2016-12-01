import glob, os, xml.etree.ElementTree as ET

def get_names(xml_tree, tag):
    temp = []
    #go through tree elements
    for elem in xml_tree.iter():
        #if tag is a "name", add to list
        if (elem.tag == 'name'):
            temp.append(elem.text)
    return temp

def matchXml(xml, repo, checkSystem = None):
    #if checkSystem is given, see if the systems are still a match
    if (checkSystem != None):
        try:
            if (os.path.isfile(os.path.join(repo,checkSystem))):
                #only do if local repo has this system as a file
                newf = open(xml, 'r', encoding='utf-8')
                #name of file should be in form [path of repo]/[system name].xml
                repof = open(os.path.join(repo,checkSystem), 'r', encoding='utf-8')
                repo_fname = ET.parse(repof)
                xml_fname = ET.parse(newf)
                tags = ["star", "system", "planet", "bplanet"]
                for tag in tags:
                    if (compare(get_names(repo_fname, tag), get_names(xml_fname, tag))):
                        return os.path.join(repo,checkSystem)            
        except:
            print ("Could not open "+os.path.join(repo,checkSystem))        
    #checkSystem was not a match or not given, so go through whole repository
    files=glob.glob(os.path.join(repo,"*.xml"))
    for file in files:
        try:
            newf = open(xml, 'r', encoding='utf-8')
            repof = open(file, 'r', encoding='utf-8')
        except InputError:
            print ("Invalid path")
            break
        filename = os.path.basename(file)
        try:
            repo_fname = ET.parse(repof)
            xml_fname = ET.parse(newf)
            tags = ["system", "star", "planet", "bplanet"]
            for tag in tags:
                if (compare(get_names(repo_fname, tag), get_names(xml_fname, tag))):
                    return file
        except:
            print ("Could not parse "+file)
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
