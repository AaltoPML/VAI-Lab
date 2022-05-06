import tkinter as tk
import os
from PIL import Image, ImageTk
from tkinter import messagebox, ttk

from tkinter.filedialog import askopenfilename, askdirectory
from scipy.io import loadmat

_PLUGIN_CLASS_NAME = "MainPage"
_PLUGIN_CLASS_DESCRIPTION = "Splash and Menu page used as GUI entry-point"
_PLUGIN_READABLE_NAMES = {"main","main page","launch page"}
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
        self.my_label = tk.Label(self, 
                                    image = self.my_img1,
                                    bg = parent['bg'])

        self.my_label.grid(column = 0,
                            row = 0,
                            rowspan = 10,
                            columnspan = 4,
                            pady = 10,
                            sticky = tk.NE)
        
        my_label = tk.Label(self, 
                                text = 
                                'Indicate the data folder and define the pipeline.',
                                pady= 10,
                                font = controller.title_font,
                                bg = parent['bg'],
                                fg = 'white')
        my_label.grid(column = 0,
                            row = 11,
                            columnspan = 4)
        
        tk.Button(self,
                    text = 'Data file',
                    fg = 'white',
                    font = controller.title_font, 
                    bg = parent['bg'],
                    height = 3,
                    width = 20, 
                    command = self.upload_data_file,
                    ).grid(column = 0, row = 12)
        tk.Button(self,
                    text = 'Data folder',
                    fg = 'white',
                    font = controller.title_font, 
                    bg = parent['bg'],
                    height = 3,
                    width = 20, 
                    command = self.upload_data_folder,
                    ).grid(column = 1, row = 12)
        self.controller.Datalabel = tk.Label(self, 
                                text = 'Incomplete',
                                pady= 10,
                                padx= 10,
                                font = controller.title_font,
                                bg = parent['bg'],
                                fg = 'white')
        self.controller.Datalabel.grid(column = 2,
                            row = 12)
        
        tk.Button(self,
                    text = 'Interact with canvas',
                    fg = 'white',
                    font = controller.title_font,
                    bg = parent['bg'],
                    height = 3,
                    width = 20, 
                    command = lambda: self.canvas("aidCanvas")
                    ).grid(column = 0, row = 13)

        tk.Button(self,
                    text = 'Upoad XML file',
                    fg = 'white',
                    font = controller.title_font, 
                    bg = parent['bg'],
                    height = 3,
                    width = 20, 
                    command = self.upload_xml,
                    ).grid(column = 1, row = 13)
        
        self.controller.XMLlabel = tk.Label(self, 
                                text = 'Incomplete',
                                pady= 10,
                                padx= 10,
                                font = controller.title_font,
                                bg = parent['bg'],
                                fg = 'white')
        self.controller.XMLlabel.grid(column = 2,
                            row = 13)
        self.PluginButton = tk.Button(self,
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
        self.RunButton = tk.Button(self,
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
                                                ('All Files', '*.*')])
        
        if filename is not None and len(filename) > 0:
            self.controller.Data.set(True)
            if filename.lower().endswith(('.mat')):
                data = loadmat(filename)
                self.data_loading_window(data, filename)

    def data_loading_window(self,data, filename):
        
        self.newWindow = tk.Toplevel(self.controller)
        
        # Window options
        self.newWindow.title('Data importing helper')
        script_dir = os.path.dirname(__file__)
        self.tk.call('wm','iconphoto', self.newWindow, ImageTk.PhotoImage(
            file = os.path.join(os.path.join(
                script_dir, 
                'resources', 
                'Assets', 
                'AIDIcon.ico'))))
        self.newWindow.geometry("700x400")
        self.newWindow.grid_rowconfigure(0, weight=1)
        self.newWindow.grid_columnconfigure(0, weight=1)
        
        tk.Label(self.newWindow,
              text ="Select variables to import", anchor = tk.N, 
              justify=tk.LEFT).grid(row=0,column=0, columnspan=16)
        tk.Label(self.newWindow,
              text ="Variables in "+filename, anchor = tk.N, 
              justify=tk.LEFT).grid(row=1,column=0, columnspan=16)
        
        #Treeview 1
        style = ttk.Style()
        style.configure(
            "Treeview", background = 'white', foreground = 'white', 
            rowheight = 25, fieldbackground = 'white', 
            font = self.controller.pages_font)
        style.configure("Treeview.Heading", 
                        font = self.controller.pages_font)
        style.map('Treeview', background = [('selected', 'grey')])

        tree_frame1 = tk.Frame(self.newWindow)
        tree_frame1.grid(row = 2, column = 0, columnspan = 8, rowspan = 25)
        tree_frame2 = tk.Frame(self.newWindow)
        tree_frame2.grid(row = 2, column = 3, columnspan = 8, rowspan = 25)
        
        self.tree = []
        self.add_treeview(tree_frame1, data)
        self.add_treeview(tree_frame2, None)
        # self.tree2 = ttk.Treeview(
        #     tree_frame1, 
        #     yscrollcommand = tree_scrolly.set, 
        #     xscrollcommand = tree_scrollx.set)
        # self.tree2.pack(expand = True, side = tk.LEFT, fill = tk.BOTH)
        tk.Button(
            self.newWindow, text = 'Finish', fg = 'black', 
            height = 2, width = 10, font = self.controller.pages_font, 
            command = self.check_quit).grid(column = 3, row = 27, sticky = tk.SW)

    def add_treeview(self, frame, data):
        """ Add a treeview"""
        
        tree_scrollx = tk.Scrollbar(frame, orient = 'horizontal')
        tree_scrollx.pack(side = tk.BOTTOM, fill = tk.X)
        tree_scrolly = tk.Scrollbar(frame)
        tree_scrolly.pack(side = tk.RIGHT, fill = tk.Y)
        self.tree.append(ttk.Treeview(
            frame, 
            yscrollcommand = tree_scrolly.set, 
            xscrollcommand = tree_scrollx.set))
        self.tree[-1].pack(expand = True, side = tk.LEFT, fill = tk.BOTH)
        
        if data is not None:
            columns = ['Import', 'Name', 'Size', 'Class']
            self.tree[-1]['columns'] = columns[1:]
                
            # Format columns
            self.tree[-1].column("#0", width = 50)
            for n, cl in enumerate(self.tree[-1]['columns']):
                self.tree[-1].column(
                    cl, width = int(
                        self.controller.pages_font.measure(str(cl)))+20, 
                    minwidth = 50, anchor = tk.CENTER)
                    
            # Headings
            self.tree[-1].heading("#0", text = columns[0], anchor = tk.CENTER)
            for cl in self.tree[-1]['columns']:
                self.tree[-1].heading(cl, text = cl, anchor = tk.CENTER)
            
            variables = [key for key in data.keys() if (key[:1] != '__') and (key[-2:] != '__')]
            for n, var in enumerate(variables):
                if n%2 == 0:
                    self.tree[-1].insert(parent = '', index = 'end', iid = n, text = n, 
                                     values = (var, data[var].shape, type(data[var])), tags = ('even',))
                else:
                    self.tree[-1].insert(parent = '', index = 'end', iid = n, text = n, 
                                     values = (var, data[var].shape, type(data[var])), tags = ('odd',))
            
            # self.tree[-1].tag_configure('odd', foreground = 'black', 
            #                             background='#E8E8E8')
            # self.tree[-1].tag_configure('even', foreground = 'black', 
            #                             background='#DFDFDF')
        
            # Define double-click on row action
            if len(self.tree) == 1:
                self.tree[-1].bind("<Button-1>", self.OnClick)
        else:
            self.tree[-1].heading("#0", text = 'No variable selected for preview.', anchor = tk.CENTER)

    def check_quit(self):
        """ Saves the information and closes the window """
        self.newWindow.destroy()

    def OnClick(self,event):
        if self.tree[0].identify_column(event.x) == '#1':
            print(self.tree[0].identify_row(event.y))

    def upload_data_folder(self):
        """ Stores the directory containing the data that will be later loaded 
        """
        filename = askdirectory(initialdir = os.getcwd(),
                                    title = 'Select a folder',
                                    mustexist = True)
        self.controller._append_to_output("data_filename",filename)
        if filename is not None and len(filename) > 0:
            self.controller.Data.set(True)
