"""
Provides an interface to read and write settings from the main JSON file.
Ideally all settings should be stored using this interface.

Main functions:
```python
# Will create (or update) a new setting in the settings file.
CreateSettings(category, name, data) 

# Will get a specific setting from the settings file.
GetSettings(category, name, value=None) 
```
"""
import json
from src.logger import print
from src.variables import PATH, FRAMECOUNTER
import src.mainUI
import src.helpers as helpers
import os

currentProfile = ""
"""The currently selected profile (filename)."""

if os.name == "nt":
    currentProfile = r"profiles\currentProfile.txt"
else:
    currentProfile = "profiles/currentProfile.txt"

# Check that the current profile file exists
if not os.path.exists(currentProfile):
    with open(currentProfile, "w") as f:
        f.write("profiles/settings.json")
    print("Profile file didn't exist, created a new one")

if open(currentProfile, "r").readline().replace("\n", "") == "":
    with open(currentProfile, "w") as f:
        f.write("profiles/settings.json")
    print("Profile variable was empty, set it to settings.json")

# Check for settings file in root folder
SETPATH = str(os.path.abspath(os.path.join(PATH, os.pardir)))
# Check that settings.json exists
if os.path.exists(os.path.join(SETPATH, "settings.json")):
    # Remove import.json from profiles if it exist
    if os.path.exists(os.path.join("profiles", "import.json")):
        os.remove(os.path.join("profiles", "import.json"))
    # Move SETPATH settings.json to profiles with the name inport.json
    os.rename(os.path.join(SETPATH, "settings.json"), os.path.join("profiles", "import.json"))
    with open(currentProfile, "w") as f:
        f.write("profiles/import.json")

def EnsureFile(file:str):
    """Will check if a file exists and create it if it doesn't.

    Args:
        file (str): Filename.
    """
    try:
        with open(file, "r") as f:
            # Check if the file is valid json
            try:
                json.load(f)
            except:
                helpers.ShowFailure("\nJSON settings file corrupted, pressing OK will reset your settings and restart the app.\nPlease remember to redo the first time setup.", "Corrupted settings file")
                with open(file, "w") as ff:
                    ff.write("{}")
                src.mainUI.quit()
            pass
    except:
        with open(file, "w") as f:
            f.write("{}")
            

def ChangeProfile():
    """Will change the currently selected profile and reload the app.
    """
    global currentProfile
    
    from tkinter import filedialog
    file = filedialog.askopenfilename(initialdir=PATH+"\\profiles", title="Select a profile", filetypes=(("JSON files", "*.json"), ("All files", "*.*")))
    with open(currentProfile, "w") as f:
        f.truncate(0)
        f.write(file)
    
    import src.variables
    src.variables.RELOAD = True

def CreateProfile():
    """Will create a new profile based on the current one. Will not change the current profile.
    """
    from tkinter import filedialog
    newFile = filedialog.asksaveasfile(initialdir=PATH+"\\profiles", initialfile="newProfile.json", title="Create a new profile", filetypes=(("JSON files", "*.json"), ("All files", "*.*")))
    try:       
        # Copy the current profile
        profile = open(currentProfile, "r").readline().replace("\n", "")
            
        with open(profile, "r") as f:
            data = json.load(f)
        
        newFile.truncate(0)
        json.dump(data, newFile, indent=6)
            
        filePath = newFile.name
        
        newFile.close()
            
        # Change the current profile
        # ChangeProfile(filePath)
    
    except Exception as ex:
        print(ex.args)
        print("Failed to create profile")

# Change settings in the json file
def UpdateSettings(category:str, name:str, data:any):
    """Update a setting in the settings file.
    In case the setting doesn't exist, it will be created.

    Args:
        category (str): Json category.
        name (str): Json setting name.
        data (_type_): Data to write.
    """
    global currentFrameSettings, frameCounter
    try:
        profile = open(currentProfile, "r").readline().replace("\n", "")
        EnsureFile(profile)
        with open(profile, "r") as f:
            settings = json.load(f)

        settings[category][name] = data
        with open(profile, "w") as f:
            f.truncate(0)
            json.dump(settings, f, indent=6)
            
        currentFrameSettings = settings
        frameCounter = FRAMECOUNTER
        
    except Exception as ex:
        pass

# Get a specific setting
currentFrameSettings = {}
frameCounter = -1
def GetSettings(category:str, name:str, value:any=None):
    """Will get a specific setting from the settings file.

    Args:
        category (str): Json category.
        name (str): Json setting name.
        value (_type_, optional): Default value in case the data is not found. Defaults to None.

    Returns:
        _type_: The data from the json file. (or the default value)
    """
    global frameCounter, currentFrameSettings
    try:
        if frameCounter != FRAMECOUNTER:
            profile = open(currentProfile, "r").readline().replace("\n", "")
            EnsureFile(profile)
            with open(profile, "r") as f:
                settings = json.load(f)
                currentFrameSettings = settings
            frameCounter = FRAMECOUNTER
        else:
            settings = currentFrameSettings
        
        if settings[category][name] == None:
            return value    
        
        return settings[category][name]
    except Exception as ex:
        if value != None:
            CreateSettings(category, name, value)
            return value
        else:
            pass


# Create a new setting
def CreateSettings(category:str, name:str, data:any):
    """Will create a new setting in the settings file.

    Args:
        category (str): Json category.
        name (str): Json setting name.
        data (_type_): Data to write.
    """
    global currentFrameSettings, frameCounter
    try:
        profile = open(currentProfile, "r").readline().replace("\n", "")
        EnsureFile(profile)
        with open(profile, "r") as f:
            settings = json.load(f)

        # If the setting doesn't exist then create it 
        if not category in settings:
            settings[category] = {}
            settings[category][name] = data
        
        # If the setting exists then overwrite it
        if category in settings:
            settings[category][name] = data
            
        with open(profile, "w") as f:
            f.truncate(0)
            json.dump(settings, f, indent=6)
            
        currentFrameSettings = settings
        frameCounter = FRAMECOUNTER
    except Exception as ex:
        pass
        
def AddToList(category:str, name:str, data:any, exclusive:bool=False):
    """Will add a new item to a list in the settings file.

    Args:
        category (str): Json category.
        name (str): Json list name.
        data (str): Data to add to the list.
        exclusive (bool, optional): Whether to allow adding multiple instances of the same data. Defaults to False.
    """
    global currentFrameSettings, frameCounter
    try:
        profile = open(currentProfile, "r").readline().replace("\n", "")
        EnsureFile(profile)
        with open(profile, "r") as f:
            settings = json.load(f)

        # If the setting doesn't exist then create it 
        if not category in settings:
            settings[category] = {}
            settings[category][name] = []
            # Check if the data is a list
            if isinstance(data, list):
                for item in data:
                    settings[category][name].append(item)
            else:
                settings[category][name].append(data)
        
        if not name in settings[category]:
            settings[category][name] = []
            # Check if the data is a list
            if isinstance(data, list):
                for item in data:
                    settings[category][name].append(item)
            else:
                settings[category][name].append(data)
        
        # If the setting exists then overwrite it
        if category in settings:
            # Check if the data is a list
            if isinstance(data, list):
                for item in data:
                    if exclusive:
                        if not item in settings[category][name]:
                            settings[category][name].append(item)
                    else:
                        settings[category][name].append(item)
            else:
                if exclusive:
                    if not data in settings[category][name]:
                        settings[category][name].append(data)
                else:
                    settings[category][name].append(data)
            
        with open(profile, "w") as f:
            f.truncate(0)
            json.dump(settings, f, indent=6)
            
        currentFrameSettings = settings
        frameCounter = FRAMECOUNTER
    except Exception as ex:
        pass
        

def RemoveFromList(category:str, name:str, data:any):
    """Remove an item from a list in the settings file.

    Args:
        category (str): Json category.
        name (str): Json list name.
        data (_type_): Data to remove from the list.
    """
    global currentFrameSettings, frameCounter
    try:
        profile = open(currentProfile, "r").readline().replace("\n", "")
        EnsureFile(profile)
        with open(profile, "r") as f:
            settings = json.load(f)

        # If the setting doesn't exist then don't do anything 
        if not category in settings:
            return
        
        # If the setting exists then overwrite it
        if category in settings:
            settings[category][name].remove(data)
            
        with open(profile, "w") as f:
            f.truncate(0)
            json.dump(settings, f, indent=6)
            
        currentFrameSettings = settings
        frameCounter = FRAMECOUNTER
        
    except Exception as ex:
        pass