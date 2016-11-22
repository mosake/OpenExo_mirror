import subprocess
import platform

'''
push_all() pushes changes from local repository to master using command line
'''


def push_all():

    try:
        if platform.system() == "Windows":
           
            subprocess.Popen("git checkout master", shell=True,
                                   stdout=subprocess.PIPE).stdout.read()         
            if(b'error' in subprocess.Popen("git pull origin master", shell=True,
                                   stdout=subprocess.PIPE).stdout.read()):
                print("error detected")

             
            subprocess.Popen("git add *", shell=True,
                                   stdout=subprocess.PIPE).stdout.read()
            subprocess.Popen("git commit -m \"Push to main repository\"",
                                   shell=True,
                                   stdout=subprocess.PIPE).stdout.read()
            print(subprocess.Popen("git push origin master", shell=True,
                                   stdout=subprocess.PIPE).stdout.read())
            print('Repository has been successfully pushed.\n')
        # Push git
        # Note: This only works if Git on Windows is installed...
        elif platform.system() == "Linux":
            # Command if run on Linux device (Could be subject to change)
            subprocess.Popen("git pull origin master", shell=True,
                                   stdout=subprocess.PIPE).stdout.read()
            subprocess.Popen("git add *", shell=True,
                                   stdout=subprocess.PIPE).stdout.read()
            subprocess.Popen("git commit -m \"Push to main repository\"",
                                   shell=True,
                                   stdout=subprocess.PIPE).stdout.read()
            print(subprocess.Popen("git push origin master", shell=True,
                                   stdout=subprocess.PIPE).stdout.read())
            print('Repository has been successfully pushed.\n')
        elif platform.system() == "Darwin" or platform.system() == "darwin":
            subprocess.Popen("git pull origin master", shell=True,
                                   stdout=subprocess.PIPE).stdout.read()
            subprocess.Popen("git add *", shell=True,
                                   stdout=subprocess.PIPE).stdout.read()
            subprocess.Popen("git commit -m \"Push to main repository\"",
                                   shell=True,
                                   stdout=subprocess.PIPE).stdout.read()
            print(subprocess.Popen("git push origin master", shell=True,
                                   stdout=subprocess.PIPE).stdout.read())
            print('Repository has been successfully pushed.\n')
    except:
        print("Git was unable to push your local copy to the main repository.")
