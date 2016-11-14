import ctypes  # An included library with Python install.
import subprocess

'''
# As Hanno (an admin), I want a notification on the desktop to appear when there is an update from another catalogue found
catalogue_name = "Test Catalogue"
notification_description = catalogue_name + " has been updated."
ctypes.windll.user32.MessageBoxW(0, notification_description, "Update", 1)
'''
def push(csv_file_name="Test csv file"):
    print(subprocess.Popen("git add csvFilePush.py",
                           shell=True, stdout=subprocess.PIPE).stdout.read())
    print(subprocess.Popen("git commit -m \"" + csv_file_name + " has been added.\"",
                           shell=True, stdout=subprocess.PIPE).stdout.read())  
    print(subprocess.Popen("git push -f origin master",
                           shell=True, stdout=subprocess.PIPE).stdout.read()) 
    
