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
path="extracted" #restructured to use relative path from main folder
#TODO: What if last commit file gets deleted?
fname = "last_commit_date.txt" #textfile containing last commit date
last_commit_date = str(datetime.date.today())
if (os.path.isfile(fname) == False): #create file with current date if dne
    file1 = open(fname, "w")
    file1.write(last_commit_date)
    file1.close()
with open(fname) as f:
    content = f.readlines()
last_commit_date = content[0].strip()
url_exoplanetarchive = "http://exoplanet.eu/catalog/csv/?status=&f=updated+%3E%3D+%22"+last_commit_date+"%22"
#url_exoplanetarchive = "http://exoplanet.eu/catalog/csv/?status=&f=updated+%3E%3D+%222016-01-01%22&select=*"

def get():
    try:
        #xmltools.ensure_empty_dir(path+"/"+"ExoPlanet_data")
        xmltools.ensure_empty_dir(os.path.join(os.path.curdir, 'extracted','ExoPlanet_data'))
        #urllib.request.urlretrieve (url_exoplanetarchive, path+"/"+"ExoPlanet_data/Exoplanet_archive_updated.csv")
        urllib.request.urlretrieve (url_exoplanetarchive, os.path.join(os.getcwd(), 'extracted', 'ExoPlanet_data', 'Exoplanet_archive_updated.csv'))
    except:
        pass
    
def parse():
    # delete old data
    xmltools.ensure_empty_dir(os.path.join(os.path.curdir, 'extracted', 'Extracted_XMLs'))

    # parse data into default xml format
    f = open(os.path.join(os.path.curdir, 'extracted','ExoPlanet_data','Exoplanet_archive_updated.csv'))
    
    csv_f=csv.reader(f)
    header = [x.strip() for x in f.readline().split(",")]
    for line in csv_f:
        p = dict(zip(header, [x.strip() for x in line]))
        takeLetterOff = -2 
        if (len(p["# name"].split(" ")[-1]) !=1 ): #if there's no letter at end
            takeLetterOff=len(p["# name"]) #take whole item        
        host_name = p["# name"][:takeLetterOff].strip() #remove the last letter
        pl_letter = p["# name"][takeLetterOff:].strip()
        outputfilename = os.path.join(os.path.curdir, 'extracted','Extracted_XMLs', "Exoplanet_"+host_name+".xml")        
        if os.path.exists(outputfilename):
            system = ET.parse(outputfilename).getroot()
            star = system.find(".//star")
        else:
            system = ET.Element("system")
            #TODO: Need to remove letter at the back
            ET.SubElement(system, "name").text = host_name
            ra, dec = p["ra"], p["dec"]
            if len(p["ra"]) > 0:
                ra = float(p["ra"])
            else:
                print (p["name #"])
            if len(p["dec"]) > 0:
                dec = float(p["dec"])
            else:
                print (p["name #"])
            ra_dec = converter.deg2HMS(ra, dec, True)
            
            ET.SubElement(system, "rightascension").text = ra_dec[0]
            ET.SubElement(system, "declination").text = ra_dec[1]
            
            ET.SubElement(system, "distance",errorminus=p['star_distance_error_min'], errorplus=p['star_distance_error_max']).text = p["star_distance"]            

            star = ET.SubElement(system,"star")
            ET.SubElement(star, "name").text = host_name
            #QUESTION: Will errorplus be negative?
            ET.SubElement(star, "radius", errorminus=p['star_radius_error_min'], errorplus=p['star_radius_error_max']).text = p["star_radius"]
            #ET.SubElement(star, "magV", errorminus=p['st_vjerr'], errorplus=p['st_vjerr']).text = p["st_vj"]
            #Question: no error minus plus on exoplanet
            ET.SubElement(star, "magV").text = p["mag_v"]
            ET.SubElement(star, "magI").text = p["mag_i"]
            ET.SubElement(star, "magJ").text = p["mag_j"]
            ET.SubElement(star, "magH").text = p["mag_h"]
            ET.SubElement(star, "magK").text = p["mag_k"]
            #Upperlimit?
            ET.SubElement(star, "mass", errorminus=p['mass_error_min'], errorplus=p['mass_error_max']).text = p["mass"]
            ET.SubElement(star, "temperature", errorminus=p['star_teff_error_min'], errorplus=p['star_teff_error_max']).text = p["star_teff"]
            #ET.SubElement(star, "metallicity").text = p["st_metratio"]
            ET.SubElement(star, "metallicity",errorminus=p['star_metallicity_error_min'], errorplus=(p['star_metallicity_error_max'])).text = p["star_metallicity"]
            
            #HL: Add alternate names to file to help comparison across external sources
            alternate_names = p["alternate_names"].split(",")
            for alt_name in alternate_names:
                ET.SubElement(star, "name").text = alt_name[:-2].strip() #take out letter
                
        planet = ET.SubElement(star,"planet")
        #HL: Add alternate names to file to help comparison across external sources
        alternate_names = p["alternate_names"].split(",")
        for alt_name in alternate_names:
            ET.SubElement(planet, "name").text = alt_name
        #QUESTION: This site does not separate the letters in columns??
        ET.SubElement(planet, "name").text = host_name+" "+pl_letter#+" "+p["pl_letter"]
        #why the switch between errors?
        ET.SubElement(planet, "semimajoraxis", errorminus=(p["semi_major_axis_error_min"]), errorplus=p["semi_major_axis_error_max"]).text = p["semi_major_axis"]
        ET.SubElement(planet, "eccentricity", errorminus=p['eccentricity_error_min'], errorplus=p['eccentricity_error_max']).text = p["eccentricity"]
        ET.SubElement(planet, "periastron", errorminus=p['omega_error_min'], errorplus=p['omega_error_max']).text = p["omega"]
        ET.SubElement(planet, "inclination", errorminus=p['inclination_error_min'], errorplus=p['inclination_error_max']).text = p["inclination"]
        ET.SubElement(planet, "period", errorminus=p['orbital_period_error_min'], errorplus=p['orbital_period_error_max']).text = p["orbital_period"]
        # check for both kinds of masses
        if p['mass'] == None or p['mass'] == "":
            # use msini
            ET.SubElement(planet, "mass", errorminus=p['mass_sini_error_min'], errorplus=p['mass_sini_error_max']).text = p["mass_sini"]
        else: 
            # use mass jupiter
            ET.SubElement(planet, "mass", errorminus=p['mass_error_min'], errorplus=p['mass_error_max']).text = p["mass"]
        ET.SubElement(planet, "radius", errorminus=p['radius_error_min'], errorplus=p['radius_error_max']).text = p["radius"]
        #QUESTION: No errorplus/minus???
        ET.SubElement(planet, "temperature").text = p["temp_calculated"]
        ET.SubElement(planet, "discoverymethod").text = p["detection_type"]
        ET.SubElement(planet, "discoveryyear").text = p["discovered"]
        ET.SubElement(planet, "lastupdate").text = p["updated"]

        # Need to check if BJD ?
        # QUESTION: Is BJD the same as JD?
        JD = "JD"
        if len(p["tzero_tr"]) == 0:
            JD = ""
        ET.SubElement(planet, "transittime", errorminus=p['tzero_tr_error_min'], errorplus=p['tzero_tr_error_max'], unit=JD).text = p["tzero_tr"]

        # Cleanup and write file
        xmltools.removeemptytags(system)
        xmltools.indent(system)
        ET.ElementTree(system).write(outputfilename) 



if __name__=="__main__":
    get()
    parse()