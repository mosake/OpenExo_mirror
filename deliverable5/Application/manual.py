def main(command=""):
	'''(str) -> None
	Given the string of a command, prints out a message to explain how to use it
	'''
	if (command == "extract"):
		entry = """Command: extract \n\nSynopsis:\n\textract [options]\n\n
Description: Extracts planets that have been updated since the last commit date from exoplanet and NASA open archive as XML format. The new XML files are stored in the Changed_Systems directory.\n\n
Options:\n-l\t Outputs the updated planets on to the terminal in the order: [Planet hostname]\t[updated date]\t[Source]
\n-a\t Extracts and automatically commits changes right after.\n"""
		print (entry)
	elif (command == "repo"):
		entry = """Command: repo \n\nSynopsis:\n\trepo [-p PATH]\n\n
Description: For displaying and changing local repository location.\n\n
Options:\n-p\t Used to set local repository to [PATH] given. eg: repo -p /home/localRepository\n"""
		print (entry)
	elif (command == "date"):
		entry = """Command: date \n\nSynopsis:\n\tdate [-c DATE]\n\n
Description: For displaying and changing the last updated date. Extract will only 
query exteral sources for records that have been updated on and after this date.\n
Options:\n-c\t Used to set the last committed date. DATE must be in format YYYY-MM-DD. eg: date -c YYYY-MM-DD"""
		print (entry)
	elif (command == "commit"):
		entry = """Command: commit \n\nSynopsis:\n\tcommit\n\n
Description: Syncs the local repository through a git pull command, copies extracted XML files into the local repository and pushes the changes on to the remote\n
	Options: \n"""	
		print (entry)
	elif (command == "help"):
		entry = """Command: help \n\nSynopsis:\n\thelp [command]\n\n
Description: Prints the help page of given command\n
Options: \n"""	
		print (entry)
	elif (command == "exit"):
		entry = """Command: exit \n\nSynopsis:\n\texit\n\n
Description: Terminates the program\n Options: \n"""	
		print (entry)
	else:
		entry = """This page contains the list of commands that you can execute:\n\n
1) help: help [command] prints out detail message of command
2) extract: Extracts planets that have been updated since the last commit date
3) repo : Manipulate path of local repository to check
4) date : Manipulate last update date to extract systems.
5) commit : Commits the updated changes of the to the respository.
6) exit: Terminate the program.\n\n"""
		print (entry)