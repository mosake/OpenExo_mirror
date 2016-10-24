import updated.list_updated as list_updated
import push.push as push
import manual as man

switch = True
while (switch):

    #Prompt user to input (i.e. help)
    command = input('>>>')
    
    #Redirects the main to call other python scripts accordingly
    #Refer to help page for details of each command
    if (command == "help"):
        man.main()
    elif (command[0:7] == "updated"):
        list_updated.main()    
    elif (command[0:4] == "push"):
        push.main()
    elif (command == "exit"):
        switch = False
    else:
        print("'"+command + "' is not an available command. Enter 'help' for list of available commands.")