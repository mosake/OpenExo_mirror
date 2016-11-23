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
            error_message = pull_errors.decode()
            print(error_message)
            print("%")
            if(error_message != ""):
                if("files would be overwritten by merge" in error_message):
                    # There is a merge conflict in pulling the master repo
                    # Any merge conflict would need to be solved manually
                    # (That way, no data is accidentally lost)
                    print("Oops! There seems to be a merge conflict.")
                    print("Please check your files and the master repository.")
                    raise
                elif("Aborting" in error_message):
                    # Some other error has occurred.
                    print("The master repository could not be pulled.")
                    raise

      #      subprocess.Popen("git pull origin master", shell=True,
      #                                             stdout=subprocess.PIPE).stdout.read()          
            add_command = subprocess.Popen("git add *", shell=True, stdout=subprocess.PIPE)
            add_command.communicate()
            commit_command = subprocess.Popen("git commit -m \"Push to main repository\"",
                                                   shell=True,
                                                   stdout=subprocess.PIPE).stdoust.read()
            commit_command.communicate()
            push_command = subprocess.Popen("git push origin master", shell=True,
                                       stdout=subprocess.PIPE).stdout.read()
            push_command.communicate()
            print('\n')
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
