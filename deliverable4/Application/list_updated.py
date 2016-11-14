import urllib
import urllib.request
import urllib.error
import csv
import os
import datetime
import socket

def push_all ():
    #store data files in module path    
    #path = os.path.dirname(os.path.realpath(__file__)) 
    path="updated" #restructured to use relative path from main folder
    #TODO: What if last commit file gets deleted?
    fname = "last_commit_date.txt" #textfile containing last commit date
    last_commit_date = str(datetime.date.today())
    if (os.path.isfile(fname) == False): #create file with current date if dne
        file1 = open(fname, "w")
        file1.write(last_commit_date)
        file1.close()
    with open(fname) as f:
        content = f.readlines()
    last_commit_date = content [0].strip()
    attempts = 0
    source = "NASA_Exoplanet_Archive"
    url = "http://exoplanetarchive.ipac.caltech.edu/cgi-bin/nstedAPI/nph-nstedAPI?table=exoplanets&where=rowupdate%3E=to_date(%27"+last_commit_date+"%27,%27yyyy-mm-dd%27)&order=rowupdate&format=csv&select=*"
    #url ="http://exoplanetarchive.ipac.caltech.edu/cgi-bin/nstedAPI/nph-nstedAPI?table=exoplanets&where=pl_hostname=%27KOI-12%27&order=rowupdate&format=csv&select=*"
    while attempts < 3:
        try:
            response = urllib.request.urlopen(url, timeout = 5)
            content = response.read()
            f1 = open(path+"/"+source+"_modified_since_"+last_commit_date+".csv", 'w' )
            #create cumulative.csv for his generate_systems_kepler.py
            f2 = open( path+"/"+"cumulative.csv", 'w' ) 
            f1.write( content.decode(encoding='utf-8',errors='ignore'))
            f2.write( content.decode(encoding='utf-8',errors='ignore'))
            f1.close()
            f2.close()
            break
        except urllib.error.URLError as e:
            attempts += 1
        except socket.timeout:
            attempts += 1
            
    if (attempts >= 3): #error extracting from NASA so exit?
        print ("Could not connect to NASA archive")
    
    print ("The following are planet host name that has been modified since "+last_commit_date+":")
    print ("Host Name" + " " * 21 + "Date Modified" + " " * 17+ "Source")
    if (attempts <3):
        with open(path+"/"+source+"_modified_since_"+last_commit_date+".csv", 'r') as f:
            reader = csv.reader(f)
            row1 = next(reader)
            nameCol = row1.index("pl_hostname")
            dateCol = row1.index("rowupdate")         
            for row in reader:
                if (len(row) == 0):
                    pass
                row_hostname = row[nameCol]
                row_update = row[dateCol]
                row_source = source	
                tab= " "*(30-len(row_hostname))
                tab2= " "*(30-len(row_update))
                print (row_hostname+tab+row_update + tab2 + row_source)
            
    attempts = 0
    source = "Exoplanet"
    url = "http://exoplanet.eu/catalog/csv/?status=&f=updated+%3E%3D+%22"+last_commit_date+"%22&select=*"
    while attempts < 3:
        try:
            response = urllib.request.urlopen(url, timeout = 5)
            content = response.read()
            f = open(path+"/"+source+"_modified_since_"+last_commit_date+".csv", 'w' )
            f.write( content.decode(encoding='utf-8',errors='ignore'))
            f.close()
            break
        except urllib.error.URLError as e:
            attempts += 1
        except socket.timeout:
            attempts += 1        
    
    if (attempts >= 3): #error extracting from Exoplanet so exit?
        print ("Could not connect to Exoplanet archive")
    if (attempts < 3):
        with open(path+"/"+source+"_modified_since_"+last_commit_date+".csv", 'r') as f:
            reader = csv.reader(f)
            row1 = next(reader)
            nameCol = 0
            dateCol = row1.index("updated")
            
            for row in reader:
                if (len(row) == 0): #skip empty lines
                    continue
                takeLetterOff = -2 
                if (len(row[nameCol].split(" ")[-1]) !=1 ): #if there's no letter at end
                    takeLetterOff=len(row[nameCol]) #take whole item
                row_hostname = row[nameCol][:takeLetterOff].strip() #take off last letter
                row_update = row[dateCol]
                row_source = source	
                tab= " "*(30-len(row_hostname))
                tab2= " "*(30-len(row_update))
                print (row_hostname+tab+row_update + tab2 + row_source)