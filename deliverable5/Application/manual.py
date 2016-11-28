def main(command=""):
	if (command == "extract"):
		entry = "Command: extract. \n\nSynopsis:\n\textract [-l]\n\n"
		entry += "Description: Extracts planets that have been updated since the last commit date "
		entry += "from exoplanet and NASA open archive as XML format. "
		entry += "The new XML files are stored in the Changed_Systems directory.\n\n"
		entry += "Options:\n-l\tOutputs the updated planets on to the terminal in the order: "
		entry += "[Planet hostname]\t[updated date]\t[Source]"	
		print (entry)
	elif (command == "1"):
		print("")
	else:
		print("This page contains the list of commands that you can execute:\n\n",
			"1) extract: Extracts planets that have been updated since the last commit date\n",
    		"2) repo : Manipulate path of local repository to check\n\n",
    		"3) commit : Commits the updated changes of the to the respository.\n\n",
    		"4) exit: Terminate the program.\n\n")