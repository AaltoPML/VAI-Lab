import tkinter as tk
import os
from PIL import Image, ImageTk

from tkinter.filedialog import askopenfilename, askdirectory
from scipy.io import loadmat

from aidesign.utils.plugins.dataLoader import dataLoader

_PLUGIN_CLASS_NAME = "MainPage"
_PLUGIN_CLASS_DESCRIPTION = "Splash and Menu page used as GUI entry-point"
_PLUGIN_READABLE_NAMES = {"main":"default","main page":"alias","launch page":"alias"}
_PLUGIN_MODULE_OPTIONS = {"layer_priority": 1,"required_children": ['aidCanvas', 'pluginCanvas']}
_PLUGIN_REQUIRED_SETTINGS = {}
_PLUGIN_OPTIONAL_SETTINGS = {}
class MainPage(tk.Frame):

    def __init__(self, parent, controller, config:dict):
        " Here we define the main frame displayed upon opening the program."
        " This leads to the different methods to provide feedback."
        super().__init__(parent, bg = parent['bg'])
        self.controller = controller
        self.controller.title('AI Assisted Framework Design')
        
        self.bg = parent['bg']
        
        script_dir = os.path.dirname(__file__)
        self.my_img1 = ImageTk.PhotoImage(
                            Image.open(
                                os.path.join(
                                    script_dir,
                                    'resources',
                                    'Assets',
                                    'AIFRED.png')
                                    ).resize((600, 300))
                                )
        
        self.grid_rowconfigure(tuple(range(3)), weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        frame1 = tk.Frame(self, bg = self.bg)
        frame2 = tk.Frame(self, bg = self.bg)
        frame3 = tk.Frame(self, bg = self.bg)
        
        self.my_label = tk.Label(frame1, 
                                    image = self.my_img1,
                                    bg = parent['bg'])

        self.my_label.grid(column = 0,
                            row = 0,
                            rowspan = 10,
                            columnspan = 4,
                            pady = 10,
                            sticky = tk.NE)
        
        my_label = tk.Label(frame2, 
                                text = 
                                'Indicate the data folder and define the pipeline.',
                                pady= 10,
                                font = controller.title_font,
                                bg = parent['bg'],
                                fg = 'white')
        my_label.grid(column = 0,
                            row = 11,
                            columnspan = 4)
        
        tk.Button(frame3,
                    text = 'Data file',
                    fg = 'white',
                    font = controller.title_font, 
                    bg = parent['bg'],
                    height = 3,
                    width = 20, 
                    command = self.upload_data_file,
                    ).grid(column = 0, row = 12)
        tk.Button(frame3,
                    text = 'Data folder',
                    fg = 'white',
                    font = controller.title_font, 
                    bg = parent['bg'],
                    height = 3,
                    width = 20, 
                    command = self.upload_data_folder,
                    ).grid(column = 1, row = 12)
        self.controller.Datalabel = tk.Label(frame3, 
                                text = 'Incomplete',
                                pady= 10,
                                padx= 10,
                                font = controller.title_font,
                                bg = parent['bg'],
                                fg = 'white')
        self.controller.Datalabel.grid(column = 2,
                            row = 12)
        
        tk.Button(frame3,
                    text = 'Interact with canvas',
                    fg = 'white',
                    font = controller.title_font,
                    bg = parent['bg'],
                    height = 3,
                    width = 20, 
                    command = lambda: self.canvas("aidCanvas")
                    ).grid(column = 0, row = 13)

        tk.Button(frame3,
                    text = 'Upload XML file',
                    fg = 'white',
                    font = controller.title_font, 
                    bg = parent['bg'],
                    height = 3,
                    width = 20, 
                    command = self.upload_xml,
                    ).grid(column = 1, row = 13)
        
        self.controller.XMLlabel = tk.Label(frame3, 
                                text = 'Incomplete',
                                pady= 10,
                                padx= 10,
                                font = controller.title_font,
                                bg = parent['bg'],
                                fg = 'white')
        self.controller.XMLlabel.grid(column = 2,
                            row = 13)
        self.PluginButton = tk.Button(frame3,
                    text = 'Modules plugins',
                    fg = 'white',
                    font = controller.title_font, 
                    bg = parent['bg'],
                    height = 3,
                    width = 20, 
                    state = tk.DISABLED,
                    command = lambda: self.canvas("pluginCanvas"),
                    )
        self.PluginButton.grid(column = 0, row = 14)
        self.RunButton = tk.Button(frame3,
                    text = 'Run Pipeline',
                    fg = 'white',
                    font = controller.title_font, 
                    bg = parent['bg'],
                    height = 3,
                    width = 20, 
                    state = tk.DISABLED,
                    command = self.controller.destroy,
                    )
        self.RunButton.grid(column = 1, row = 14)
        
        self.controller.XML = tk.IntVar()
        self.controller.Data = tk.IntVar()
        self.controller.Plugin = tk.IntVar()
        self.controller.XML.set(False)
        self.controller.Data.set(False)
        self.controller.Plugin.set(False)
        
        self.controller.XML.trace('w', self.trace_XML)
        self.controller.Data.trace('w', self.trace_Data)
        self.controller.Plugin.trace('w', self.trace_Plugin)
        
        frame1.grid(column=0, row=0, sticky="n")
        frame2.grid(column=0, row=1, sticky="n")
        frame3.grid(column=0, row=2, sticky="n")
        
    def set_data_in(self, _):
        pass

    def trace_XML(self,*args):
        """ Checks if XML variable has been updated
        """
        if self.controller.XML.get():
            self.controller.XMLlabel.config(text = 'Done!', fg = 'green')
            if self.controller.Data.get():
                self.PluginButton.config(state = 'normal')

    def trace_Data(self,*args):
        """ Checks if Data variable has been updated
        """
        if self.controller.Data.get():
            self.controller.Datalabel.config(text = 'Done!', fg = 'green')
            if self.controller.XML.get():
                self.PluginButton.config(state = 'normal')

    def trace_Plugin(self,*args):
        """ Checks if Plugin variable has been updated
        """
        if self.controller.Plugin.get():
            self.RunButton.config(state = 'normal')

    def canvas(self,name: str):
        """ Shows the canvas frame.
        :param name: string type of name of desired canvas.
        """
        self.controller._show_frame(name)

    def upload_xml(self):
        """ Indicates the XML file containng the desired pipeline """
        filename = askopenfilename(initialdir = os.getcwd(), 
                                   title = 'Select a file', 
                                   defaultextension = '.xml', 
                                   filetypes = [('XML file', '.xml'), 
                                                ('All Files', '*.*')])
        if filename is not None and len(filename) > 0:
            self.controller._append_to_output("xml_filename",filename)
            self.controller.XML.set(True)

    def upload_data_file(self):
        """ Loads a data file containing the data required for the pipeline """
        filename = askopenfilename(initialdir = os.getcwd(), 
                                   title = 'Select a file', 
                                   defaultextension = '.mat', 
                                   filetypes = [('mat file', '.mat'), 
                                                ('CSV', '.csv'), 
                                                ('All Files', '*.*')])
        
        if filename is not None and len(filename) > 0:
            if filename.lower().endswith(('.mat')):
                data = loadmat(filename)
                dL = dataLoader(self.controller, data, filename)
                self.controller.Data = dL.controller.Data

    def upload_data_folder(self):
        """ Stores the directory containing the data that will be later loaded 
        """
        filename = askdirectory(initialdir = os.getcwd(),
                                    title = 'Select a folder',
                                    mustexist = True)
        self.controller._append_to_output("data_filename",filename)
        if filename is not None and len(filename) > 0:
            self.controller.Data.set(True)
