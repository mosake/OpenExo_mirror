import subprocess
import os
import platform
import time
'''
push_all() pushes changes from local repository to master using command line
'''


def push_all(directory="*"):
    platform_names = ['Windows', 'Linux', 'Darwin', 'darwin']
    try:
        if platform.system() in platform_names:
            branch_command = subprocess.Popen("git branch", shell=True,
                                              stdout=subprocess.PIPE,
                                              stderr=subprocess.PIPE)
            branch_output, branch_error = branch_command.communicate()
            branch_output_str = branch_output.decode()
            branch_name = branch_output_str.split('\n')[0][1:]

            checkout_command = subprocess.Popen("git checkout " + branch_name,
                                                shell=True,
                                                stdout=subprocess.PIPE,
                                                stderr=subprocess.PIPE)
            checkout_command.communicate()
            pull_result = subprocess.Popen(["git", "pull"],
                                           stdout=subprocess.PIPE,
                                           stderr=subprocess.PIPE)
            pull_output, pull_err = pull_result.communicate()
            pull_error_msg = pull_err.decode()
            if(pull_error_msg != ""):
                if("files would be overwritten by merge" in pull_error_msg):
                    # There is a merge conflict in pulling the master repo
                    # Any merge conflict would need to be solved manually
                    # (That way, no data is accidentally lost)
                    print("Oops! There seems to be a merge conflict.")
                    print("Please check your files and the master repository.")
                    raise
                elif("Aborting" in pull_error_msg):
                    # Some other error has occurred.
                    print("The master repository could not be pulled.")
                    raise
            add_command = subprocess.Popen("git add \"" + directory + "\"",
                                           stdout=subprocess.PIPE,
                                                stderr=subprocess.PIPE)
            add_output, add_err = add_command.communicate()
            add_error_msg = add_err.decode()
            print(add_error_msg)
            if ("fatal" in add_error_msg):
                print("Oops! Are you adding an invalid file/directory?")
                raise
            commit_command = subprocess.Popen("git commit"\
                                              " -m \"Push to main repository\"",
                                              shell=True,
                                              stdout=subprocess.PIPE)
            commit_command.communicate()
            push_command = subprocess.Popen("git push origin " + branch_name,
                                            shell=True,
                                            stdout=subprocess.PIPE,
                                            stderr=subprocess.PIPE)
            push_output, push_error = push_command.communicate()
            push_error_message = push_error.decode()
            if(push_error_message != "" and "error" in push_error_message):
                print("Oops! A conflict occurred when pushing to remote.")
                print("Please check the repositories for further details.")
                raise
            print("Push was successful.")
    except:
        print("Git was unable to push your local copy to the main repository.")
