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


