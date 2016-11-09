import ctypes  # An included library with Python install.
import subprocess

def push(csv_file_name):
    print(subprocess.Popen("git add " +  csv_file_name,
                           shell=True, stdout=subprocess.PIPE).stdout.read())
    print(subprocess.Popen("git commit -m \"" + csv_file_name + " has been added.\"",
                           shell=True, stdout=subprocess.PIPE).stdout.read())  
    print(subprocess.Popen("git push -f origin master",
                           shell=True, stdout=subprocess.PIPE).stdout.read()) 