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

switch = True
while (switch):

    #Prompt user to input (i.e. help)
    command = input('>>> ')

    #Redirects the main to call other python scripts accordingly
    #Refer to help page for details of each command
    if (command[0:4] == "help"):
        if (len(command) > 4):
            entry = command[5:].strip()
            print(entry)
            man.main(entry)
        else: 
            man.main()
    elif (command[0:7] == "extract"):
        try:
            if (command[8:].strip() == "-l"):
                list_updated.main()
            translate_Exoplanet.get()
            translate_Exoplanet.parse()
            translate_NASA.get()
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
            match = matchSystems.matchXml(os.path.abspath(filename), localRepoPath)
            try:
                cmpXml.main(match, filename)
            except:
                print ("failed to compare " + match +" and " + filename)
                success = False
        if (success):
            print ("Files extracted. Please review XML files in "+os.path.join(os.getcwd(),"Changed_Systems"))

    elif (command[0:4] == "repo"):
        if (command[5:8] == "-p "):
            l = command.split(" ")
            if (len(l) < 3):
                print ("Usage Error: Path argument not specified.")
            else:
                repoPath = command[8:]
                repoTools.changeLocalRepo(repoPath)
        elif (command[5:8].strip() == "-l"):
            print(repoTools.getLocalRepo())
        else:
            print ("Usage Error: "+command+". Please enter 'help' to read 'repo' command")

    elif (command[0:6] == "commit"):
        push.push_all()

    elif (command == "exit"):
        switch = False
        
    else:
        print("'"+command + "' is not an available command. Enter 'help' for list of available commands.")

