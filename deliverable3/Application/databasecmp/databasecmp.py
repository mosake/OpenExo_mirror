import glob, os, xml.etree.ElementTree as ET

REPO_PATH = "C:/Users/Kelly/Desktop/f16/CSCC01/team25-Project/deliverable3/databasecmp/test_database1"
NEW_XML_PATH = "C:/Users/Kelly/Desktop/f16/CSCC01/team25-Project/deliverable3/databasecmp/test_database3"

'''
Returns a dictionary with the following format, given a path to a directory:
{file: [[system], [star], [planet], [binary planet]]}
If a field is missing, print None

path - the path of the dictionary containing 1 or more xml files
'''

def get_dictionary(path):
    
    # compare with new files   
    files=glob.glob(path + "/*.xml")

    cdb = {}

    for file in files:
        try:
            f = open(file, 'r')
        except InputError:
            print ("Invalid path")
            break
        filename = os.path.basename(file)
        temp = []
        current_data = ET.parse(f)
        systems = current_data.getroot()

        if not current_data.findall(".//planet"):
            temp.append('None')
        else:         
            temp2 = []
            for system in systems:
                temp2.append(systems.findtext("name")) 
            temp.append(temp2)
        
        if not current_data.findall(".//star"):
            temp.append('None')
        else:                
            temp2 = []
            for star in current_data.findall(".//star"):
                temp2.append(star.findtext("name"))   
            temp.append(temp2)
            
        if not current_data.findall(".//planet"):
            temp.append('None')
        else:
            temp2 = []
            for planet in current_data.findall(".//planet"):
                temp2.append(planet.findtext("name"))
            temp.append(temp2)
            
        if not current_data.findall(".//binary/planet"):
            temp.append('None')
        else:
            temp2 = []
            for cbin in current_data.findall(".//binary/planet"):
                temp2.append(cbin.findtext("name"))     
            temp.append(temp2)
        cdb[path + "/" + filename] = temp
        
    return cdb
# end of get_dictionary

'''
Given 2 dictionaries of the form:
{file: [[system], [star], [planet], [binary planet]]}
(If a field is missing, print None)

Check if each file has distinct values between the chosen value.

Returns a list of filenames that are already in both files.
If find is invalid do nothing.

dict1, dict2 - dictionaries
find - system, star, planet or bplanet
       default: "planet"
'''

def check_repetitions(current_database, new_database, find="planet"):
    index = None
    current_files = []
    new_files = []
    
    if find == "system":
        index = 0
    elif find == "star":
        index = 1
    elif find == "planet":
        index = 2
    elif find == "bplanet":
        index = 3
    else:
        return None
    
    for key in current_database:
        for i in key[index]:
            for key2 in new_database:
                # check if filenames repeat
                if key == key2:
                    current_files.append(key)
                    new_files.append(key2)
                else:
                    for j in key2[index]:
                        if i == j:
                            current_files.append(key)
                            new_files.append(key2)
                            break
    return (current_files, new_files)
#end of check_repetitions


# change \ to / in paths
REPO_PATH.replace("\\", "/")
NEW_XML_PATH.replace("\\", "/")

cdb = get_dictionary(REPO_PATH)
ndb = get_dictionary(NEW_XML_PATH)

print(check_repetitions(cdb, ndb, "system"))