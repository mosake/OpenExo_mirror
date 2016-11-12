import glob, os, xml.etree.ElementTree as ET

'''
Returns a dictionary with the following format, given a path to a directory:
{file: [system, star, planet, binary planet]}
If a field is missing, print None

path - the path of the dictionary containing 1 or more xml files
'''

def get_dictionary(path):
    
    # compare with new files   
    files=glob.glob(path + "/*.xml")

    cdb = {}

    for file in files:
        f = open(file, 'r')
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
        cdb[filename] = temp
        
    return cdb
# end of get_dictionary

current_database = "C:/Users/Kelly/Desktop/f16/CSCC01/team25-Project/deliverable3/databasecmp/test_database1"
new_database = "C:/Users/Kelly/Desktop/f16/CSCC01/team25-Project/deliverable3/databasecmp/test_database3"
print(get_dictionary(current_database))