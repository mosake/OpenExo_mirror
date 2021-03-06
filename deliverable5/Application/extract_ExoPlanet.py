#!/usr/bin/python 
import urllib
import urllib.request
import urllib.error
import os
import xml.etree.ElementTree as ET 
import xmltools as xmltools
import csv
import datetime
#####################
# Exoplanet.eu
#####################
url_exoplaneteu = "http://exoplanet.eu/catalog/csv/"

def get():
    try:
        #xmltools.ensure_empty_dir(path+"/"+"ExoPlanet_data")
        xmltools.ensure_empty_dir(os.path.join(os.path.curdir, 'extracted','ExoPlanet_data'))
        #urllib.request.urlretrieve (url_exoplanetarchive, path+"/"+"ExoPlanet_data/Exoplanet_archive_updated.csv")
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
            url_exoplanetarchive = "http://exoplanet.eu/catalog/csv/?status=&f=updated+%3E%3D+%22"+last_commit_date+"%22"   
            #url_exoplanetarchive = "http://exoplanet.eu/catalog/csv/?status=&f=updated+%3E%3D+%222016-01-01%22&select=*"        
            urllib.request.urlretrieve (url_exoplanetarchive, os.path.join(os.getcwd(), 'extracted', 'ExoPlanet_data', 'Exoplanet_archive_updated.csv'))
    except:
        return -1


def parse():
    # delete old data
    xmltools.ensure_empty_dir(os.path.join(os.getcwd(), 'extracted', 'Extracted_XMLs'))

    # parse data into default xml format
    f = open(os.path.join(os.getcwd(), 'extracted','ExoPlanet_data','Exoplanet_archive_updated.csv'))
    header = [x.strip() for x in f.readline()[1:].replace("# ", "").split(",")]
    reader = csv.reader(f)
    for line in reader:
        p = dict(zip(header, line))
        outputfilename = os.path.join(os.path.curdir, 'extracted','Extracted_XMLs', "Exoplanet_"+p["star_name"]+".xml")
        if os.path.exists(outputfilename):
            system = ET.parse(outputfilename).getroot()
            star = system.find(".//star")
        else:
            system = ET.Element("system")
            ET.SubElement(system, "name").text = p["star_name"].strip()
          
            # convert the right ascension to hh mm ss
            tempra = ""
            ra = float(p['ra'])
            hours = ra / 360 * 24
            tempra += "%.2i" % (hours)
            minutes = hours % 1 * 60
            tempra += " %.2i" % (minutes)
            seconds = minutes % 1 * 60
            tempra += " %.2i" % (round(seconds))
            ET.SubElement(system, "rightascension").text = tempra

            # convert declination to deg mm ss
            tempdec = ""
            dec = float(p['dec'])
            tempdec += "%+.2i" %(dec) 
            minutes = dec % 1 * 60
            tempdec += " %.2i" % (minutes)
            seconds = round(minutes % 1 * 60)
            tempdec+= " %.2i" % (seconds)
            ET.SubElement(system, "declination").text = tempdec

            ET.SubElement(system, "distance").text = p["star_distance"]
            star = ET.SubElement(system, "star")
            ET.SubElement(star, "name").text = p["star_name"].strip()
            ET.SubElement(star, "age").text = p["star_age"]
            ET.SubElement(star, "radius").text = p["star_radius"]
            #HL: Added
            ET.SubElement(star, "magV").text = p["mag_v"]
            ET.SubElement(star, "magI").text = p["mag_i"]
            ET.SubElement(star, "magJ").text = p["mag_j"]
            ET.SubElement(star, "magH").text = p["mag_h"]
            ET.SubElement(star, "magK").text = p["mag_k"]
            #
            ET.SubElement(star, "mass").text = p["star_mass"]
            ET.SubElement(star, "spectraltype").text = p["star_sp_type"]
            ET.SubElement(star, "temperature").text = p["star_teff"]
            ET.SubElement(star, "metallicity").text = p["star_metallicity"]

        planet = ET.SubElement(star, "planet")
        ET.SubElement(planet, "name").text = p["name"].strip()
        alternate_names = p["alternate_names"].split(",")
        for alt_name in alternate_names:
            ET.SubElement(planet, "name").text = alt_name        
        ET.SubElement(planet, "semimajoraxis", errorminus=p["semi_major_axis_error_min"], errorplus=p["semi_major_axis_error_max"]).text = p["semi_major_axis"]
        ET.SubElement(planet, "periastron", errorminus=p['omega_error_min'], errorplus=p['omega_error_max']).text = p["omega"]
        ET.SubElement(planet, "eccentricity", errorminus=p['eccentricity_error_min'], errorplus=p['eccentricity_error_max']).text = p["eccentricity"]
        ET.SubElement(planet, "longitude", errorminus=p['lambda_angle_error_min'], errorplus=p['lambda_angle_error_max']).text = p["lambda_angle"]
        ET.SubElement(planet, "inclination", errorminus=p['inclination_error_min'], errorplus=p['inclination_error_max']).text = p["inclination"]
        ET.SubElement(planet, "period", errorminus=p['orbital_period_error_min'], errorplus=p['orbital_period_error_min']).text = p["orbital_period"]
        ET.SubElement(planet, "mass", errorminus=p['mass_error_min'], errorplus=p['mass_error_max']).text = p["mass"]
        ET.SubElement(planet, "radius", errorminus=p['radius_error_min'], errorplus=p['radius_error_max']).text = p["radius"]
        ET.SubElement(planet, "temperature").text = p["temp_measured"]
        # to match OEC 
        if p['detection_type'].find("Radial Velocity") != -1:
            ET.SubElement(planet, "discoverymethod").text = "RV"
        elif p['detection_type'].find("imaging") != -1:
            ET.SubElement(planet, "discoverymethod").text = "imaging"
        elif p['detection_type'].find("ransit") != -1: #transit and Primary Transit checked
            ET.SubElement(planet, "discoverymethod").text = "transit"
        ET.SubElement(planet, "discoveryyear").text = p["discovered"]
        ET.SubElement(planet, "lastupdate").text = p["updated"].replace("-","/")[2:]

        # ET.SubElement(planet, "spinorbitalignment").text = p[""]

        # Cleanup and write file
        xmltools.removeemptytags(system)
        xmltools.indent(system)
        ET.ElementTree(system).write(outputfilename) 