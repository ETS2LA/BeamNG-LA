import requests
import src.variables as variables
import src.settings as settings
import src.console as console
import src.helpers as helpers
import os
from src.logger import print

def UpdateChecker():
    disable = settings.GetSettings("Dev", "disable_update_checker", False)
    if disable:
        print("Dev mode is enabled, skipping update check")
        return
    
    currentVer = variables.VERSION.split(".")
    githubUrl = "https://raw.githubusercontent.com/ETS2LA/BeamNG-LA/refs/heads/main/"
    remoteVer = requests.get(githubUrl + "version.txt").text.strip().split(".")
    if int(currentVer[0]) < int(remoteVer[0]):
        update = True
    elif int(currentVer[1]) < int(remoteVer[1]):
        update = True
    elif int(currentVer[2]) < int(remoteVer[2]):
        update = True
    else:
        update = False
    
    if update:
        changelog = requests.get(githubUrl + "changelog.txt").text
            
        print(f"An update is available: {'.'.join(remoteVer)}")

        print(f"Changelog:\n{changelog}")
        from tkinter import messagebox
        if helpers.AskOkCancel("Updater", f"We have detected an update, do you want to install it?\nCurrent - {'.'.join(currentVer)}\nUpdated - {'.'.join(remoteVer)}\n\nChangelog:\n{changelog}"):
            if variables.IN_VENV:
                # Make a new cmd outside of the current venv and use it to run git pull in the app folder
                import subprocess
                subprocess.run('start cmd /k "cd .. & cd venv & cd Scripts & deactivate & cd .. & cd .. & cd app & git stash & git pull"', shell=True)
            else:
                os.chdir(variables.PATH)
                os.system("git stash")
                os.system("git pull")
            if helpers.AskOkCancel("Updater", "The update has been installed and the application needs to be restarted. Do you want to quit the app?", yesno=True):
                try:
                    if settings.GetSettings("User Interface", "hide_console") == True:
                        console.RestoreConsole()
                        console.CloseConsole()
                except:
                    pass
                quit()
            else:
                variables.UPDATEAVAILABLE = remoteVer
                variables.RELOAD = True
        else:
            variables.UPDATEAVAILABLE = remoteVer
            variables.RELOAD = True
            pass
    else:
        print(f"No update available, current version: {'.'.join(currentVer)}")
