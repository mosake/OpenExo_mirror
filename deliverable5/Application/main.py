import list_updated as list_updated
import manual as man
import xmltools
import translate_ExoPlanet as translate_Exoplanet
import translate_NASA as translate_NASA
import compare as cmpXml
import gitPush as push
import databasecmp as matchSystems
import repo as repoTools
import glob
import os
import shutil
import ntpath, datetime

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
        pull_repo(localRepoPath)
        #go through changed_systems and copy files to local repo
        source_dir = os.path.join(os.getcwd(), "Changed_Systems")
        for filename in glob.glob(os.path.join(source_dir, '*.*')):
            try:
                shutil.copy(filename, localRepoPath)
            except:
                print ("Couldn't copy " + filename + " to " + localRepoPath +". Please close all files and try again")
        #push changes from local to remote
        push.push_all(localRepoPath) 
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
        try:
            if (command[8:].find(" -l") > -1):
                list_updated.main()
            if (translate_Exoplanet.get() != -1):
                translate_Exoplanet.parse()
            if (translate_NASA.get() != -1):
                translate_NASA.parse()
        except:
            print("Extraction from external sources failed. Try closing all opened CSV files and try again")
        localRepoPath = repoTools.getLocalRepo()
        if (localRepoPath == ""): #file is not right, print message and pass if case
            print("Problem in path. Please set the path of local repository using 'repo' command")
            pass
        extractedXmlsPath = os.path.join(os.getcwd(), 'extracted', 'Extracted_XMLs')
        #clear change_systems of old updates
        xmltools.ensure_empty_dir(os.path.join(os.getcwd(),"Changed_Systems"))
        success = True
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
        if (command[8:].find(" -a") > -1):
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

