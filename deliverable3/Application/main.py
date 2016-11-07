import list_updated as list_updated
import manual as man
import translate_ExoPlanet as translate_Exoplanet
import translate_NASA as translate_NASA

switch = True
while (switch):

    #Prompt user to input (i.e. help)
    command = input('>>>')
    
    #Redirects the main to call other python scripts accordingly
    #Refer to help page for details of each command
    if (command == "help"):
        man.main()
    elif (command[0:7] == "updated"):
        #TODO: handle opened file exceptions
        list_updated.main()
        translate_Exoplanet.get()
        translate_Exoplanet.parse()
        translate_NASA.get()
        translate_NASA.parse()
    elif (command[0:4] == "push"):
        push.main()
    elif (command == "exit"):
        switch = False
    else:
        print("'"+command + "' is not an available command. Enter 'help' for list of available commands.")