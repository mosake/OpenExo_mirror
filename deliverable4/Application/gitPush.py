import subprocess
import platform
import time
'''
push_all() pushes changes from local repository to master using command line
'''


def push_all():

    try:
        if platform.system() == "Windows":
           
            subprocess.Popen("git checkout master", shell=True,
                                   stdout=subprocess.PIPE).stdout.read()
            sleep(5)
            pull_command = subprocess.Popen("git pull origin master", shell=True,
                                   stdout=subprocess.PIPE).stdout.read()
            while True:
                line = pull_command.stdout.readline()
                print(line)
                print("sdf")
                if not line:
                    break
            subprocess.Popen("git checkout master", shell=True,
                                   stdout=subprocess.PIPE).stdout.read()         
            if(b'error' not in subprocess.Popen("git pull origin master", shell=True,
                                   stdout=subprocess.PIPE).stdout.read()):
                print("FAIL????")
             
            subprocess.Popen("git add *", shell=True,
                                   stdout=subprocess.PIPE).stdout.read()
            subprocess.Popen("git commit -m \"Push to main repository\"",
                                   shell=True,
                                   stdout=subprocess.PIPE).stdout.read()
            print(subprocess.Popen("git push origin master", shell=True,
                                   stdout=subprocess.PIPE).stdout.read())
            print('Repository has been successfully pushed.\n')
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
