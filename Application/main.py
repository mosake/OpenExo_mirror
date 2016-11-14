<<<<<<< HEAD
switch = True

while (switch):

    #Prompt user to input (i.e. help)
    command = input('>>> ')

    #Redirects the main to call other python scripts accordingly
    #Refer to help page for details of each command
    if (command == "help"):
        import manual
    elif (command[0:2] == "up"):
        import update
        update.main(command)
    elif (command == "exit"):
        switch = False


=======
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
        import gitPush as gitPush
        gitPush.push_all()
    elif (command == "exit"):
        switch = False
    else:
        print("'"+command + "' is not an available command. Enter 'help' for list of available commands.")
>>>>>>> 4ef1fa568bf5eb81f087dde41b146f397d7a403a
