# File to run command line from Python
import time
import subprocess
import platform
# Or just clone remote repository (remote), either works
try:
    # Reminder: To make push effective, need to add preceding commands:
    # git add <add files to update the existing system
    # git commit -m "some stuff here"
    # And then push, etc.
    if platform.system() == "Windows":
        time.sleep(1)
        print(subprocess.Popen("git push -f origin master", shell=True, stdout=subprocess.PIPE).stdout.read())
    # Push git
    # Note: This only works if Git on Windows is installed...
    elif platform.system() == "Linux":
        print("Command for Linux OS")
        print(subprocess.Popen("git push origin master",
                               shell=True, stdout=subprocess.PIPE).stdout.read())    
    elif platform.system() == "Darwin" or platform.system() == "darwin":
        print("Command for Mac")
        print(subprocess.Popen("git push origin master",
                               shell=True, stdout=subprocess.PIPE).stdout.read())
except:
    print("Git was unable to push your local copy to your main repository.")
'''
import subprocess
subprocess.call(["git", "pull"])
subprocess.call(["make"])
subprocess.call(["make", "test"])
'''