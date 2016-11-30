#!/usr/bin/python 
import urllib
import urllib.request
import urllib.error
import os
import xml.etree.ElementTree as ET 
import xmltools as xmltools
import degrees_to_time_converter as converter
import csv
import datetime

#####################
# Exoplanet Archive
#####################
#store data files in module path    
#path = os.path.dirname(os.path.realpath(__file__)) 
#path="updated" #restructured to use relative path from main folder
fname = "last_commit_date.txt" #textfile containing last commit date
last_commit_date = str(datetime.date.today())
url_exoplanetarchive = ""
#print (url_exoplanetarchive)

def get():
    #xmltools.ensure_empty_dir(path+"/"+"NASA_data")
    xmltools.ensure_empty_dir(os.path.join(os.getcwd(), 'extracted','NASA_data'))
    fname = "last_commit_date.txt" #textfile containing last commit date
    last_commit_date = str(datetime.date.today())
    if (os.path.isfile(fname) == False): #create file with current date if dne
        file1 = open(fname, "w")
        file1.write(last_commit_date)
        file1.close()
    with open(fname) as f:
        content = f.readlines()
    if (len(content) == 0):
        print("Last updated date has not been set correctly. Aborting extract")
        return -1
    else:
        last_commit_date = content[0].strip()
        url_exoplanetarchive = "http://exoplanetarchive.ipac.caltech.edu/cgi-bin/nstedAPI/nph-nstedAPI?table=exoplanets&where=rowupdate>=to_date(%27"+last_commit_date+"%27,%27yyyy-mm-dd%27)&order=rowupdate&format=csv&select=*"  
        #url_exoplanetarchive = "http://exoplanet.eu/catalog/csv/?status=&f=updated+%3E%3D+%222016-01-01%22&select=*"    
    #urllib.request.urlretrieve (url_exoplanetarchive, path+"/"+"NASA_data/NASA_archive_updated.csv")
    urllib.request.urlretrieve (url_exoplanetarchive, os.path.join(os.getcwd(), 'extracted', 'NASA_data', 'NASA_archive_updated.csv'))

def parse():
    # delete old data HL: We'll take this out because the folder should have info from exoplanet
    #xmltools.ensure_empty_dir("systems_exoplanetarchive")

    # parse data into default xml format
    f = open(os.path.join(os.getcwd(), 'extracted','NASA_data','NASA_archive_updated.csv'))    
    csv_f=csv.reader(f)
    header = [x.strip() for x in f.readline().split(",")]
    for line in csv_f:
        p = dict(zip(header, [x.strip() for x in line]))
        outputfilename = os.path.join(os.getcwd(), 'extracted','Extracted_XMLs',"NASA_"+p["pl_hostname"]+".xml")
        if os.path.exists(outputfilename):
            system = ET.parse(outputfilename).getroot()
            star = system.find(".//star")
        else:
            if os.path.exists(os.path.join(os.getcwd(), 'extracted','Extracted_XMLs',"Exoplanet_"+p["pl_hostname"]+".xml")):
                #extracted from exoplanet.eu before so we will delete the file
                #print("Exoplanet_"+p["pl_hostname"]+".xml")
                os.remove(os.path.join(os.getcwd(), 'extracted','Extracted_XMLs',"Exoplanet_"+p["pl_hostname"]+".xml"))
            system = ET.Element("system")
            ET.SubElement(system, "name").text = p["pl_hostname"]
            
            tempra = ""
            tempra += p["ra_str"].split("h")[0] # hours
            tempra += " " + p["ra_str"].split("h")[1].split("m")[0] # minutes
            tempra += " %.2i" % (round(float(p["ra_str"].split("h")[1].split("m")[1].split("s")[0]))) # seconds
            ET.SubElement(system, "rightascension").text = tempra

            tempdec = ""
            tempdec += p["dec_str"].split("d")[0] # hours
            tempdec += " " + p["dec_str"].split("d")[1].split("m")[0] # minutes
            tempdec += " %.2i" % (round(float(p["dec_str"].split("d")[1].split("m")[1].split("s")[0]))) # seconds
            ET.SubElement(system, "declination").text = tempdec
            ET.SubElement(system, "distance",errorminus=p['st_disterr1'], errorplus=p['st_disterr2'][1:]).text = p["st_dist"]            

            star = ET.SubElement(system,"star")
            ET.SubElement(star, "name").text = p["pl_hostname"]
            ET.SubElement(star, "radius", errorminus=p['st_raderr1'], errorplus=p['st_raderr2'][1:]).text = p["st_rad"]
            #ET.SubElement(star, "magV", errorminus=p['st_vjerr'], errorplus=p['st_vjerr']).text = p["st_vj"]
            ET.SubElement(star, "magV", errorminus=p['st_optmagerr'], errorplus=p['st_optmaglim'][1:]).text = p["st_optmag"]
            #ET.SubElement(star, "magI", errorminus=p['st_icerr'], errorplus=p['st_icerr']).text = p["st_ic"]
            #ET.SubElement(star, "magJ", errorminus=p['st_jerr'], errorplus=p['st_jerr']).text = p["st_j"]
            #ET.SubElement(star, "magH", errorminus=p['st_herr'], errorplus=p['st_herr']).text = p["st_h"]
            #ET.SubElement(star, "magK", errorminus=p['st_kerr'], errorplus=p['st_kerr']).text = p["st_k"]
            #Upperlimit?
            ET.SubElement(star, "mass", errorminus=p['st_masserr1'], errorplus=p['st_masserr2'][1:]).text = p["st_mass"]
            ET.SubElement(star, "temperature", errorminus=p['st_tefferr1'], errorplus=p['st_tefferr2'][1:]).text = p["st_teff"]
            #ET.SubElement(star, "metallicity").text = p["st_metratio"]
            ET.SubElement(star, "metallicity",errorminus=p['st_metfeerr1'], errorplus=(p['st_metfeerr2'])[1:]).text = p["st_metfe"]

        planet = ET.SubElement(star,"planet")
        ET.SubElement(planet, "name").text = p["pl_hostname"]+" "+p["pl_letter"]
        #why the switch between errors?
        ET.SubElement(planet, "semimajoraxis", errorminus=(p["pl_orbsmaxerr2"][1:]), errorplus=p["pl_orbsmaxerr1"]).text = p["pl_orbsmax"]
        ET.SubElement(planet, "eccentricity", errorminus=p['pl_orbeccenerr2'][1:], errorplus=p['pl_orbeccenerr1']).text = p["pl_orbeccen"]
        ET.SubElement(planet, "periastron", errorminus=p['pl_orblpererr2'][1:], errorplus=p['pl_orblpererr1']).text = p["pl_orblper"]
        ET.SubElement(planet, "inclination", errorminus=p['pl_orbinclerr2'][1:], errorplus=p['pl_orbinclerr1']).text = p["pl_orbincl"]
        ET.SubElement(planet, "period", errorminus=p['pl_orbpererr2'][1:], errorplus=p['pl_orbpererr1']).text = p["pl_orbper"]
        # check for both kinds of masses
        if p['pl_massj'] == None or p['pl_massj'] == "":
            # use msini
            ET.SubElement(planet, "mass", errorminus=p['pl_msinijerr2'][1:], errorplus=p['pl_msinijerr1']).text = p["pl_msinij"]
        else: 
            # use mass jupiter
            ET.SubElement(planet, "mass", errorminus=p['pl_massjerr2'][1:], errorplus=p['pl_massjerr1']).text = p["pl_massj"]
        ET.SubElement(planet, "radius", errorminus=p['pl_radjerr2'][1:], errorplus=p['pl_radjerr1']).text = p["pl_radj"]
        ET.SubElement(planet, "temperature", errorminus=p['pl_eqterr2'][1:], errorplus=p['pl_eqterr1']).text = p["pl_eqt"]
        ET.SubElement(planet, "discoverymethod").text = p["pl_discmethod"]
        ET.SubElement(planet, "discoveryyear").text = p["pl_disc"]
        ET.SubElement(planet, "lastupdate").text = p["rowupdate"]

        # Need to check if BJD ?
        ET.SubElement(planet, "transittime", errorminus=p['pl_tranmiderr2'][2:], errorplus=p['pl_tranmiderr1'], unit=p['pl_tsystemref']).text = p["pl_tranmid"]

        # Cleanup and write file
        xmltools.removeemptytags(system)
        xmltools.indent(system)
        ET.ElementTree(system).write(outputfilename) 

