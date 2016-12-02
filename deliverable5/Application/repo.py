#!/usr/bin/python
import os
import fileinput

def getLocalRepo():
    '''None->str
    Returns the path in localRepoPath.txt, which should contain the path of the local repository
    If it does not exist or file is empty, it will return an empty string
    '''
    fname = "localRepoPath.txt" #textfile containing path to local repo
    if (os.path.isfile(fname) == False):
        return ""
    with open(fname) as f:
        content = f.readlines() #read the file path
    #if no content
    if (len(content) == 0):
        return ""
    return content[0].strip()

def changeLocalRepo(pathName):
    '''str -> None
    Changes the path stored in localRepoPath to given pathName. Creates the file if dne
    '''
    fname = "localRepoPath.txt" #textfile containing last commit date
    opened = 0
    file1 = None
    try:
        if (os.path.isdir(pathName) == False):
            print (pathName+" is not a valid directory. Please enter a valid directory")
            return -1        
        file1 = open(fname, "w")
        opened = 1        
        file1.write(pathName)
        file1.close()
    except:
        print("Something went wrong with writing to localRepoPath.txt. Please ensure it is writeable and try again.")
    finally:
        if (opened == 1):
            file1.close()

def storeSystemMatch (systemName, matchingName, inFile):
    '''(str, str, str, bool) -> None
    inFile is name of a file containing csv of system names and name of the file
    that is a match to the system that is inside the local repository. Function sets the
    systemName to the matchingName.
    '''
    newSystem = True
    # Does a list of files, and 
    # redirects STDOUT to the file in question
    for line in fileinput.input(inFile, inplace = 1): 
        #find line beginning with systemName and replace it with [systemName],[repolocation]
        if (line.find(systemName) >=0):
            print (line.rstrip().replace(line.strip(), systemName + "," + matchingName))
            #not a new system so set it to false
            newSystem = False
        else:
            print (line.strip())
    #if this is a new system that we have not encountered before, we need to add it to our
    #file
    if (newSystem):
        #append to end of file
        with open(inFile, 'a') as f:
            f.write(systemName + "," + matchingName)