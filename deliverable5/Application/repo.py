#!/usr/bin/python
import os

def getLocalRepo():
    '''(None->str
    Returns the path in localRepoPath.txt, which should contain the path of the local repository
    If it does not exist, it will return an empty string
    '''
    fname = "localRepoPath.txt" #textfile containing path to local repo
    if (os.path.isfile(fname) == False):
        return ""
    with open(fname) as f:
        content = f.readlines() #read the file path
    return content[0].strip()

def changeLocalRepo(pathName):
    '''str -> None
    Changes the path stored in localRepoPath to given pathName. Creates the file if dne
    '''
    fname = "localRepoPath.txt" #textfile containing last commit date
    opened = 0
    file1 = None
    try:
        file1 = open(fname, "w")
        opened = 1
        if (os.path.isdir(pathName) == False):
            print (pathName+" is not a valid directory. Please enter a valid directory")
            file1.close()
            return   
        file1.write(pathName)
    except:
        print("Something went wrong with writing to localRepoPath.txt. Please ensure it is writeable and try again.")
    finally:
        if (opened == 1):
            file1.close()
