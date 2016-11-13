#Story 5: As Hanno, I want to pull a XML file of the updated system 
#corresponding to the table columns of my repository
import urllib.request
import binascii
def xmlPull(name):
    formatedName = ""
    for i in name:
        #Convert all non digits and alphabet characters to their hex rep.
        if not (i.isalpha() or i.isdigit()):
            n = binascii.hexlify(str.encode(i))
            formatedName += "%" + n.decode("utf-8")
        else:
            formatedName += i            
    url = "https://raw.githubusercontent.com/OpenExoplanetCatalogue/oec_external/master/systems_open_exoplanet_catalogue/" + formatedName + ".xml"
    try:
        page = urllib.request.urlopen(url).read().decode("utf-8")
        print(page)
    except:
        print("Cannot open " + name + " system")