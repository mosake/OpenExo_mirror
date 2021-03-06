import list_updated as list_updated
import manual as man
import translate_ExoPlanet as translate_Exoplanet
import translate_NASA as translate_NASA
import xmlcmp as cmp
import gitPush as push

switch = True
while (switch):

    #Prompt user to input (i.e. help)
    command = input('>>> ')

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
    elif (command[0: 7] == "compare"):
        try:
            l = command.split(" ")
            cmp.main(l[1], l[2])
        except:
            print("Please enter a valid input: compare file1.xml file2.xml")
            pass
    elif (command[0:4] == "push"):
        push.push_all()
    elif (command == "exit"):
        switch = False
    else:
        print("'"+command + "' is not an available command. Enter 'help' for list of available commands.")