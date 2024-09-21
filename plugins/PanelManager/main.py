from plugins.plugin import PluginInformation
from src.logger import print

PluginInfo = PluginInformation(
    name="PanelManager",
    description="Allows you to open different panels.",
    version="0.1",
    author="Tumppi066",
    url="https://github.com/BNGLA/Euro-Truck-Simulator-2-Lane-Assist",
    type="static"
)


from src.loading import LoadingWindow
import tkinter as tk
from tkinter import ttk
import src.helpers as helpers
from src.mainUI import quit, switchSelectedPlugin
import src.variables as variables
import src.settings as settings
import os
from PIL import Image, ImageTk


class UI():
    try:
        def findPlugins(self):
            # Find plugins
            print("Importing plugins...")
            #loading = LoadingWindow("Importing plugins...")
            path = os.path.join(variables.PATH, "plugins")
            plugins = []
            print_ui_events = settings.GetSettings("Dev", "print_ui_events", False)
            for file in os.listdir(path):
                if os.path.isdir(os.path.join(path, file)):
                    # Check for main.py
                    if "main.py" in os.listdir(os.path.join(path, file)):
                        # Check for PluginInformation class
                        try:
                            pluginPath = "plugins." + file + ".main"
                            plugin = __import__(pluginPath, fromlist=["PluginInformation"])
                            if plugin.PluginInfo.type == "static":
                                plugins.append(plugin.PluginInfo)
                                if print_ui_events == True:
                                    print("Found panel: " + pluginPath)
                        except Exception as ex:
                            print(ex.args)
                            pass
                        
            #loading.destroy()
            
            return plugins
        

        
        def __init__(self, master) -> None:
            self.done = False
            self.master = master
            self.page0()
        
        def destroy(self):
            self.done = True
            self.root.destroy()
            del self

        
        def page0(self):
            
            try:
                self.root.destroy()
            except: pass
            
            self.root = tk.Canvas(self.master, width=800, height=700, border=0, highlightthickness=0)
            self.root.grid_propagate(0)
            
            self.plugins = self.findPlugins()
            
            self.listVariable = tk.StringVar()
            self.listVariable.set([helpers.ConvertCapitalizationToSpaces(p.name) for p in self.plugins])
            
            self.pluginList = tk.Listbox(self.root, width=23, height=25, listvariable=self.listVariable, font=("Roboto", 12), selectmode="single", activestyle="none")
            self.pluginList.grid(row=1, column=0, padx=0, pady=2)
            
            # Double click to open
            self.pluginList.bind('<Double-Button>', lambda x: switchSelectedPlugin("plugins." + (self.plugins[self.pluginList.curselection()[0]].name) + ".main"))
            # Arrow keys to change selection up and down
            def select(event):
                # If up arrow
                curSelection = self.pluginList.curselection()[0]
                if event.keysym == "Up":
                    # If not at the top
                    if curSelection != 0:
                        # Select the one above
                        self.pluginList.select_clear(curSelection)
                        self.pluginList.select_set(curSelection-1)
                        self.pluginList.activate(curSelection)
                        self.pluginList.see(curSelection)
                # If down arrow
                elif event.keysym == "Down":
                    # If not at the bottom
                    if curSelection != len(self.plugins)-1:
                        # Select the one below
                        self.pluginList.select_clear(curSelection)
                        self.pluginList.select_set(curSelection+1)
                        self.pluginList.activate(curSelection)
                        self.pluginList.see(curSelection)
                
            self.pluginList.bind('<Up>', select)
            self.pluginList.bind('<Down>', select)
            
            helpers.MakeLabel(self.root, "Select a panel to load:\n(the list is scrollable)", 0,0, font=("Roboto", 8), padx=5, pady=10, columnspan=1)
            
            # Select the first plugin
            self.pluginList.select_set(0)
            self.pluginList.activate(0)
            self.pluginList.see(0)
            
            self.root.pack(anchor="center", expand=False)
            
            self.root.update()
        
        
        def selectedPlugin(self, plugin):
            try:
                self.pluginInfoFrame.destroy()
            except:
                pass
            
            self.plugin = plugin
            
            self.pluginInfoFrame = ttk.LabelFrame(self.root, text=plugin.name, width=430, height=530)
            self.pluginInfoFrame.pack_propagate(0)
            self.pluginInfoFrame.grid_propagate(0)
            self.pluginInfoFrame.grid(row=0, column=1, padx=10, pady=2, rowspan=3)
            
            if plugin.image != None:
                # Load the logo
                self.logo = Image.open(os.path.join(variables.PATH, "plugins", plugin.name, plugin.image))
                # Resize to height keeping the aspect ratio
                height = 130
                self.logo = self.logo.resize((int(height*self.logo.width/self.logo.height), height), Image.ANTIALIAS)
                self.logo = ImageTk.PhotoImage(self.logo)
                self.logoLabel = tk.Label(self.pluginInfoFrame, image=self.logo)
                self.logoLabel.grid(row=0, column=0, columnspan=1, pady=10, padx=30)
                
                helpers.MakeLabel(self.pluginInfoFrame, plugin.name, 0,1, font=("Roboto", 16, "bold"), padx=10, pady=10, columnspan=1, sticky="w", translate=False)
                
            else:
                helpers.MakeLabel(self.pluginInfoFrame, plugin.name, 0,0, font=("Roboto", 16, "bold"), padx=10, pady=10, columnspan=2, sticky="w", translate=False)
                
            helpers.MakeLabel(self.pluginInfoFrame, "Description", 1,0, font=("Roboto", 12), padx=10, pady=10, columnspan=2, sticky="w")
            helpers.MakeLabel(self.pluginInfoFrame, plugin.description, 2,0, font=("Roboto", 8), padx=10, pady=2, columnspan=2, sticky="w")
            helpers.MakeLabel(self.pluginInfoFrame, "Version", 3,0, font=("Roboto", 12), padx=10, pady=10, columnspan=2, sticky="w")
            helpers.MakeLabel(self.pluginInfoFrame, plugin.version, 4,0, font=("Roboto", 8), padx=10, pady=2, columnspan=2, sticky="w")
            helpers.MakeLabel(self.pluginInfoFrame, "Author", 5,0, font=("Roboto", 12), padx=10, pady=10, columnspan=2, sticky="w")
            helpers.MakeLabel(self.pluginInfoFrame, plugin.author, 6,0, font=("Roboto", 8), padx=10, pady=2, columnspan=2, sticky="w")
            helpers.MakeLabel(self.pluginInfoFrame, "URL", 7,0, font=("Roboto", 12), padx=10, pady=10, columnspan=2, sticky="w")
            helpers.MakeLabel(self.pluginInfoFrame, plugin.url, 8,0, font=("Roboto", 8), padx=10, pady=2, columnspan=2, sticky="w")

            helpers.MakeButton(self.pluginInfoFrame, "Load plugin", lambda: switchSelectedPlugin("plugins." + plugin.name + ".main"), 9, 0, width=15, padx=8)        

        
        def update(self, data):
            
            try:
                if self.plugins[self.pluginList.curselection()[0]].name != self.plugin.name:
                    self.selectedPlugin(self.plugins[self.pluginList.curselection()[0]])
            except:
                try:
                    self.plugin
                except:
                    self.selectedPlugin(self.plugins[0])
                    
            self.root.update()
    
    except Exception as ex:
        print(ex.args)