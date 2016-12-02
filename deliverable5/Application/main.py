import list_updated as list_updated
import manual as man
import xmltools
import extract_ExoPlanet as extract_ExoPlanet
import translate_NASA as extract_NASA
import cleanup as cleanUp
import compare as cmpXml
import gitPush as git
import databasecmp as matchSystems
import repo as repoTools
import glob
import os, sys
import shutil
import ntpath, datetime
#from io import StringIO

def commitCommand():
    '''(None) -> None
    Checks if localRepoPath is a valid path. If it is, syncs the local repository,
    copies all the extracted XMLs from Changed_Systems into the local repository,
    and pushes changes to the remote. Changes the last update date to current date
    '''
    localRepoPath = repoTools.getLocalRepo()
    if (os.path.isdir(localRepoPath) == False): #file is not right, print message and pass if case
        print("Problem in path. Please set the path of local repository using 'repo' command")   
    else:
        #pull from remote to make sure local is up to date
        git.pull_repo()
        
        #print clean up report in a text file
        stdout = sys.stdout  #keep a handle on the real standard output
        if (os.path.isfile('cleanUpReport.txt')):
            with open('cleanUpReport.txt', 'w') as f:
                f.write("")
        sys.stdout = open('cleanUpReport.txt', 'w', encoding='utf-8')
        try:
            cleanUp.cleanUp()
        except:
            print("Fail to run clean up script")
        #reset stdout
        sys.stdout = stdout
        #go through changed_systems and copy files to local repo
        source_dir = os.path.join(os.getcwd(), "Changed_Systems")
        print("Copying files...")
        for filename in glob.glob(os.path.join(source_dir, '*.*')):
            try:
                shutil.copy(filename, localRepoPath)
            except:
                print ("Couldn't copy " + filename + " to " + localRepoPath +". Please close all files and try again")
        #push changes from local to remote
        git.push_all() 
        #change updated date
        today = str(datetime.date.today())
        fname = "last_commit_date.txt"
        with open(fname, 'w') as f:
            f.write(today)
        print("Changes successfully made. Last updated date is now "+today)

switch = True
while (switch):

    #Prompt user to input (i.e. help)
    command = input('>>> ')

    #Redirects the main to call other python scripts accordingly
    #Refer to help page for details of each command
    if (command[0:4] == "help"):
        if (len(command) > 4):
            entry = command[5:].strip()
            man.main(entry)
        else: 
            man.main()
    elif (command[0:7] == "extract"):
        success = True
        try:
            if (command[7:].find(" -l") > -1):
                list_updated.main()
            if (extract_ExoPlanet.get() != -1):
                extract_ExoPlanet.parse()
            if (extract_NASA.get() != -1):
                extract_NASA.parse()
        except:
            print("Extraction from external sources failed. Try closing all opened CSV files and try again")
            success = False
        localRepoPath = repoTools.getLocalRepo()
        if (localRepoPath == ""): #file is not right, print message and pass if case
            print("Problem in path. Please set the path of local repository using 'repo' command")
            success = False
        extractedXmlsPath = os.path.join(os.getcwd(), 'extracted', 'Extracted_XMLs')
        #clear change_systems of old updates
        xmltools.ensure_empty_dir(os.path.join(os.getcwd(),"Changed_Systems"))
        #if not success, let's save time from going through anything
        if (success):
            for filename in glob.iglob(os.path.join(extractedXmlsPath,"*.xml")):
                #performance improv: check matchedSystems file to see if there is a previous match of this planetary system
                pairFile = "matchedSystems.txt" #textfile containing name of matched system in local repo
                #get system name from filename, i.e. remove NASA_ or ExoPlanet_
                systemName = ntpath.basename(filename).split("_",1)[1]       
                matchedSystem = None
                if (os.path.isfile(pairFile) == False): 
                    #create file if it got deleted
                    f = open(pairFile, "w")
                    f.write("")
                    f.close()
                with open(pairFile) as f:
                    for line in f:
                        if systemName in line:
                            #get name of file in local repo stored in matchedSystem file
                            #lines are in format: [system name], [filename]
                            matchedSystem = line.split(",",1)[1].strip()
                matchingFile = matchSystems.matchXml(os.path.abspath(filename), localRepoPath, matchedSystem)
                #if found, add/update this matched pairing to our matchedSystem file
                if (matchingFile != None):
                    #extract filename from matchingFile i.e. ../../[matchingSystem].xml
                    matchedSystem = ntpath.basename(matchingFile)  
                    repoTools.storeSystemMatch(systemName, matchedSystem, pairFile)
                try:
                    cmpXml.main(matchingFile, filename, os.path.join(os.getcwd(),"Changed_Systems"))
                except:
                    print ("failed to compare " + matchingFile +" and " + filename)
                    success = False
        if (success):
            print ("Files extracted. Please review XML files in "+os.path.join(os.getcwd(),"Changed_Systems"))
        #if -a tag is entered, we commit automatically
        if (command[7:].find(" -a") > -1):
            commitCommand()

    elif (command[0:4] == "repo"):
        if (command[5:8] == "-p "):
            l = command.split(" ")
            if (len(l) < 3):
                print ("Usage Error: Path argument not specified.")
            else:
                repoPath = command[8:]
                repoTools.changeLocalRepo(repoPath)
        else:
            print("Path of local repository is set as: " + repoTools.getLocalRepo())

    elif (command[0:4] == "date"):
        args = command.split(" ",2)
        if (len(command) > 4 and command [5:7]== "-c"):
            #get the rest of command and try to parse as a date
            if (len(args) < 3):
                print ("Date argument not provided. Please enter 'help [command]' to read 'date' command")
            else:
                dateArg = args[2].strip()
                try:
                    #try parsing as yyyy-mm-dd
                    dateString = str(datetime.datetime.strptime(dateArg, "%Y-%m-%d").date())
                    fname = "last_commit_date.txt"
                    with open(fname, 'w') as f:
                        f.write(dateString)
                    print ("Last commit date has been changed to: " + dateString)
                except:
                    print("Could not parse "+ dateArg + " as date. Please try again with date format YYYY-MM-DD")
        else:
            fname = "last_commit_date.txt"
            with open(fname) as f:
                print (f.readlines()[0].strip()) 
                
    elif (command[0:6] == "commit"):
        commitCommand()

    elif (command == "exit"):
        switch = False
        
    else:
        print("'"+command + "' is not an available command. Enter 'help' for list of available commands.")

