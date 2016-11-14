import subprocess
import platform

'''
push_all() pushes changes from local repository to master using command line
'''


def push_all():

    try:
        if platform.system() == "Windows":
            print(subprocess.Popen("git pull origin master", shell=True,
                                   stdout=subprocess.PIPE).stdout.read())
            print(subprocess.Popen("git add *", shell=True,
                                   stdout=subprocess.PIPE).stdout.read())
            print(subprocess.Popen("git commit -m \"Push to main repository\"",
                                   shell=True,
                                   stdout=subprocess.PIPE).stdout.read())
            print(subprocess.Popen("git push origin master", shell=True,
                                   stdout=subprocess.PIPE).stdout.read())
        # Push git
        # Note: This only works if Git on Windows is installed...
        elif platform.system() == "Linux":
            # Command if run on Linux device (Could be subject to change)
            print(subprocess.Popen("git pull origin master", shell=True,
                                   stdout=subprocess.PIPE).stdout.read())
            print(subprocess.Popen("git add *", shell=True,
                                   stdout=subprocess.PIPE).stdout.read())
            print(subprocess.Popen("git commit -m \"Push to main repository\"",
                                   shell=True,
                                   stdout=subprocess.PIPE).stdout.read())
            print(subprocess.Popen("git push origin master", shell=True,
                                   stdout=subprocess.PIPE).stdout.read())
        elif platform.system() == "Darwin" or platform.system() == "darwin":
            print(subprocess.Popen("git pull origin master", shell=True,
                                   stdout=subprocess.PIPE).stdout.read())
            print(subprocess.Popen("git add *", shell=True,
                                   stdout=subprocess.PIPE).stdout.read())
            print(subprocess.Popen("git commit -m \"Push to main repository\"",
                                   shell=True,
                                   stdout=subprocess.PIPE).stdout.read())
            print(subprocess.Popen("git push origin master", shell=True,
                                   stdout=subprocess.PIPE).stdout.read())
    except:
        print("Git was unable to push your local copy to the main repository.")
