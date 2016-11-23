import subprocess
import os
import platform
import time
'''
push_all() pushes changes from local repository to master using command line
'''


def push_all():

    try:
        if platform.system() == "Windows":
            checkout_command = subprocess.Popen("git checkout master", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            checkout_command.communicate()
            
            pull_result = subprocess.Popen(["git", "pull", "origin", "master"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            pull_output = pull_result.communicate()[0]
            pull_errors = pull_result.communicate()[1]
            pull_error_message = pull_errors.decode()
            if(pull_error_message != ""):
                if("files would be overwritten by merge" in pull_error_message):
                    # There is a merge conflict in pulling the master repo
                    # Any merge conflict would need to be solved manually
                    # (That way, no data is accidentally lost)
                    print("Oops! There seems to be a merge conflict.")
                    print("Please check your files and the master repository.")
                    raise
                elif("Aborting" in pull_error_message):
                    # Some other error has occurred.
                    print("The master repository could not be pulled.")
                    raise          
            add_command = subprocess.Popen("git add *", shell=True, stdout=subprocess.PIPE)
            add_command.communicate()
            
            commit_command = subprocess.Popen("git commit -m \"Push to main repository\"",
                                                   shell=True,
                                                   stdout=subprocess.PIPE)
            commit_command.communicate()
            push_command = subprocess.Popen("git push origin master", shell=True,
                                       stdout=subprocess.PIPE, stderr=subprocess.PIPE)           
            push_output = push_command.communicate()[0]
            push_error = push_command.communicate()[1]
            push_error_message = push_error.decode()
            if(push_error_message != "" and "error" in push_error_message):
                print("Oops! A conflict occurred when pushing to master.")
                print("Please check the repositories for further details.")
                raise
            print("Push was successful.")
            
        elif platform.system() == "Linux":
            # Command if run on Linux device (Could be subject to change)
            subprocess.Popen("git pull origin master", shell=True,
                                   stdout=subprocess.PIPE).stdout.read()
            subprocess.Popen("git add *", shell=True,
                                   stdout=subprocess.PIPE).stdout.read()
            subprocess.Popen("git push origin master", shell=True,
                                   stdout=subprocess.PIPE).stdout.read()
            print('\n')
        elif platform.system() == "Darwin" or platform.system() == "darwin":
            subprocess.Popen("git pull origin master", shell=True,
                                   stdout=subprocess.PIPE).stdout.read()
            subprocess.Popen("git add *", shell=True,
                                   stdout=subprocess.PIPE).stdout.read()
            subprocess.Popen("git commit -m \"Push to main repository\"",
                                   shell=True,
                                   stdout=subprocess.PIPE).stdout.read()
            subprocess.Popen("git push origin master", shell=True,
                                   stdout=subprocess.PIPE).stdout.read()
            print('\n')
    except:
        print("Git was unable to push your local copy to the main repository.")
