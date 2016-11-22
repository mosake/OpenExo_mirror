import glob, os, xml.etree.ElementTree as ET, sys

def main():
    XML_FILE_PATH = sys.argv[1]
    # "C:/Users/Kelly/Desktop/f16/CSCC01/team25-Project/deliverable3/databasecmp/test_database3"    
    REPO_PATH = sys.argv[2] 
    # "C:/Users/Kelly/Desktop/f16/CSCC01/team25-Project/deliverable3/databasecmp/test_database1"

    # change \ to / in paths
    REPO_PATH.replace("\\", "/")
    NEW_XML_PATH.replace("\\", "/")
    
    # check if XML_FILE_PATH is a directory or file
    if (XML_FILE_PATH == "*.xml"):
        ndb = get_file(XML_FILE_PATH)
    else:
        ndb = get_dictionary(XML_FILE_PATH)
        
    cdb = get_dictionary(REPO_PATH)
    output = check_repetitions(cdb, ndb, "system");
    return output
    
    
'''
Returns a dictionary with the following format, given a path to a directory:
{file: [[system], [star], [planet], [binary planet]]}
If a field is missing, print None

path - the path of the dictionary containing 1 or more xml files
'''

def get_dictionary(path, tag="planet"):
    
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
        names = say_my_name(f, tag)
        cdb[path + "/" + filename] = temp
    return cdb
# end of get_dictionary


def say_my_name(file, tag="planet"):
    temp = []
    current_data = ET.parse(f)
    systems = current_data.getroot()
    
    if current_data.findall(".//" + tag):
        for system in systems:
            temp.append(systems.findtext("name"))
    return temp
# end of say_my_name


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

def check_repetitions(current_database, new_file, tag="planet"):
    index = None
    current_files = []
    new_files = []
    
    if tag == "system":
        index = 0
    elif tag == "star":
        index = 1
    elif tag == "planet":
        index = 2
    elif tag == "bplanet":
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


if __name__ == "__main__":
    out = main()
    print(out)