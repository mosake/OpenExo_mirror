'''
Script from Hanno Rein's github
Formatted to compare names and alternate names in the exoplanet catalog and 
a given database of new files

notes:
    urllib changed to urllib.request due to update with Python3
        urllib   ->  urllib.request, urllib.parse, and urllib.error
        
url: open exoplanet catalog URL
oec: oec parsed xml trees
'''

import xml.etree.ElementTree as ET, xml.etree.ElementTree as NET, urllib.request, gzip, io, glob
url = "https://github.com/OpenExoplanetCatalogue/oec_gzip/raw/master/systems.xml.gz"
oec = ET.parse(gzip.GzipFile(fileobj=io.BytesIO(urllib.request.urlopen(url).read())))

oec_planet = []
oec_cbin = []
oec_star = []
oec_system = []


# catalog planet names 
for planet in oec.findall(".//planet"):
    oec_planet.append(planet.findtext("name"))
    
# catalog circumbinary planet names 
for cbin in oec.findall(".//binary/planet"):
    oec_cbin.append(cbin.findtext("name"))

# catalog star names 
for star in oec.findall(".//star"):
    oec_star.append(star.findtext("name"))
    
# catalog system names 
for system in oec.findall(".//system"):
    oec_system.append(system.findtext("name"))
    
# determine if name exists    
    
# compare with new files
path = 'C:/Users/Kelly/Desktop/f16/CSCC01/team25-Project/deliverable3/databasecmp/test_database1'   
files=glob.glob(path)   
for file in files: 
    tree = ET.parse(file)
    
    oec_planet = []
