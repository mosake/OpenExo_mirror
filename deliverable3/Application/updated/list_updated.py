import urllib
import urllib.request
import urllib.error
import csv
import os
import datetime

def main ():
    path = os.path.dirname(os.path.realpath(__file__))
    #TODO: What if last commit file gets deleted?
    fname = path+"/last_commit_date.txt" #textfile containing last commit date
    last_commit_date = str(datetime.date.today())
    if (os.path.isfile(fname) == False): #create file with current date if dne
    	os.system("echo "+last_commit_date+" > updated/last_commit_date.txt")
    with open(fname) as f:
        content = f.readlines()
    last_commit_date = content [0].strip()
    attempts = 0
    source = "NASA_Exoplanet_Archive"
    url = "http://exoplanetarchive.ipac.caltech.edu/cgi-bin/nstedAPI/nph-nstedAPI?table=exoplanets&where=rowupdate%3E=to_date(%27"+last_commit_date+"%27,%27yyyy-mm-dd%27)&order=rowupdate&format=csv"
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
            print (type(e))
            
    print ("The following are planet host name that has been modified since "+last_commit_date+":")
    with open(path+"/"+source+"_modified_since_"+last_commit_date+".csv", 'r') as f:
        reader = csv.reader(f, delimiter=',')
        for row in reader:
            row_hostname = row[0]
            row_update = row[len(row)-1]
            row_source = source
            if (row[0] == "pl_hostname"):
                row_hostname = "Planet Host Name" 
            if (row[len(row)-1] == "rowupdate"):
                row_update = "Date Modified" 
                row_source = "Source"
    
            tab= " "*(30-len(row_hostname))
            tab2= " "*(30-len(row_update))
            print (row_hostname+tab+row_update + tab2 + row_source)
            
    attempts = 0
    source = "Exoplanet"
    url = "http://exoplanet.eu/catalog/csv/?status=&f=updated+%3E%3D+%22"+last_commit_date+"%22"
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
            print (type(e))
    
    with open(path+"/"+source+"_modified_since_"+last_commit_date+".csv", 'r') as f:
        reader = csv.reader(f, delimiter=',')
        for row in reader:
            if (len(row) > 0 and row[0] != "# name"):
                row_hostname = row[0]
                row_update = row[24]
                row_source = source
                tab= " "*(30-len(row_hostname))
                tab2= " "*(30-len(row_update))
                print (row_hostname+tab+row_update + tab2 + row_source)