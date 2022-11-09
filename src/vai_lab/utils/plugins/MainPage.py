import tkinter as tk
import os
from PIL import Image, ImageTk

from tkinter.filedialog import askopenfilename, askdirectory
import pandas as pd

from vai_lab.Data.xml_handler import XML_handler
from vai_lab.utils.plugins.dataLoader import dataLoader
from vai_lab._import_helper import get_lib_parent_dir

_PLUGIN_READABLE_NAMES = {"main": "default",
                          "main page": "alias",
                          "launch page": "alias"}                               # type:ignore
_PLUGIN_MODULE_OPTIONS = {"layer_priority": 1,
                          "required_children": ['aidCanvas', 'pluginCanvas']}   # type:ignore
_PLUGIN_REQUIRED_SETTINGS = {}                                                  # type:ignore
_PLUGIN_OPTIONAL_SETTINGS = {}                                                  # type:ignore


class MainPage(tk.Frame):
    """Splash and Menu page used as GUI entry-point"""

    def __init__(self, parent, controller, config: dict):
        " Here we define the main frame displayed upon opening the program."
        " This leads to the different methods to provide feedback."
        super().__init__(parent, bg=parent['bg'])
        self.controller = controller
        self.controller.title('AI Assisted Virtual Laboratories')

        self.controller.output_type = 'regression'
        self.out_data = pd.DataFrame()
        self.bg = parent['bg']

        self.script_dir = get_lib_parent_dir()
        self.my_img1 = ImageTk.PhotoImage(
            Image.open(
                os.path.join(
                    self.script_dir,
                    'utils',
                    'resources',
                    'Assets',
                    'VAILabs.png')
            ).resize((350, 350))
        )

        self.grid_columnconfigure(0, weight=1)

        frame1 = tk.Frame(self, bg=self.bg)
        frame2 = tk.Frame(self, bg=self.bg)
        frame3 = tk.Frame(self, bg=self.bg)

        self.my_label = tk.Label(frame1,
                                 image=self.my_img1,
                                 bg=parent['bg'])

        self.my_label.grid(column=0,
                           row=0,
                           rowspan=10,
                           columnspan=4,
                           pady=10,
                           sticky=tk.NE)

        my_label = tk.Label(frame2,
                            text='Indicate the data folder and define the pipeline.',
                            pady=10,
                            font=controller.title_font,
                            bg=parent['bg'],
                            fg='white')
        my_label.grid(column=0,
                      row=11,
                      columnspan=4)

        tk.Button(frame3,
                  text='Upload data matrix',
                  fg='white',
                  font=controller.title_font,
                  bg=parent['bg'],
                  height=3,
                  width=20,
                  command=self.upload_data_folder,
                  ).grid(column=0, row=12)
        tk.Button(frame3,
                  text='Upload data path',
                  fg='white',
                  font=controller.title_font,
                  bg=parent['bg'],
                  height=3,
                  width=20,
                  command=self.upload_data_path,
                  ).grid(column=1, row=12)
        self.controller.Datalabel = tk.Label(frame3,
                                             text='Optional',
                                             pady=10,
                                             padx=10,
                                             font=controller.title_font,
                                             bg=parent['bg'],
                                             fg='white')
        self.controller.Datalabel.grid(column=2,
                                       row=12)

        self.interactButton = tk.Button(frame3,
                                        text='Interact with canvas',
                                        fg='white',
                                        font=controller.title_font,
                                        bg=parent['bg'],
                                        height=3,
                                        width=20,
                                        # state=tk.DISABLED,
                                        command=lambda: self.canvas(
                                            "aidCanvas")
                                        )
        self.interactButton.grid(column=0, row=13)

        self. uploadButton = tk.Button(frame3,
                                       text='Upload XML file',
                                       fg='white',
                                       font=controller.title_font,
                                       bg=parent['bg'],
                                       height=3,
                                       width=20,
                                    #    state=tk.DISABLED,
                                       command=self.upload_xml,
                                       )
        self. uploadButton.grid(column=1, row=13)

        self.controller.XMLlabel = tk.Label(frame3,
                                            text='Incomplete',
                                            pady=10,
                                            padx=10,
                                            font=controller.title_font,
                                            bg=parent['bg'],
                                            fg='white')
        self.controller.XMLlabel.grid(column=2,
                                      row=13)
        self.PluginButton = tk.Button(frame3,
                                      text='Modules plugins',
                                      fg='white',
                                      font=controller.title_font,
                                      bg=parent['bg'],
                                      height=3,
                                      width=20,
                                      state=tk.DISABLED,
                                      command=lambda: self.canvas(
                                          "pluginCanvas"),
                                      )
        self.PluginButton.grid(column=0, row=14)
        self.RunButton = tk.Button(frame3,
                                   text='Run Pipeline',
                                   fg='white',
                                   font=controller.title_font,
                                   bg=parent['bg'],
                                   height=3,
                                   width=20,
                                   state=tk.DISABLED,
                                   command=self.controller.destroy,
                                   )
        self.RunButton.grid(column=1, row=14)

        self.controller.XML = tk.IntVar()
        self.controller.Data = tk.IntVar()
        self.controller.Plugin = tk.IntVar()
        self.controller.XML.set(False)
        self.controller.Data.set(False)
        self.controller.Plugin.set(False)

        self.controller.XML.trace('w', self.trace_XML)
        # self.controller.Data.trace('w', self.trace_Data)
        self.controller.Plugin.trace('w', self.trace_Plugin)

        frame1.grid(column=0, row=0, sticky="n")
        frame2.grid(column=0, row=1, sticky="n")
        frame3.grid(column=0, row=2, sticky="n")

    def set_data_in(self, _):
        pass

    def trace_XML(self, *args):
        """ Checks if XML variable has been updated
        """
        if self.controller.XML.get():
            self.controller.XMLlabel.config(text = 'Done!', fg = 'green')
            # if self.controller.Data.get():
            self.PluginButton.config(state = 'normal')
            if self.controller.Plugin.get():
                self.RunButton.config(state='normal')

    # def trace_Data(self, *args):
    #     """ Checks if Data variable has been updated
    #     """
    #     if self.controller.Data.get():
    #         self.controller.Datalabel.config(text='Done!', fg='green')
    #         self.interactButton.config(state='normal')
    #         self.uploadButton.config(state='normal')

    def trace_Plugin(self, *args):
        """ Checks if Plugin variable has been updated
        """
        if self.controller.Plugin.get():
            self.RunButton.config(state='normal')

    def canvas(self, name: str):
        """ Shows the canvas frame.
        :param name: string type of name of desired canvas.
        """
        self.controller._show_frame(name)

    def upload_xml(self):
        """ Indicates the XML file containng the desired pipeline """
        filename = askopenfilename(initialdir=os.getcwd(),
                                   title='Select a file',
                                   defaultextension='.xml',
                                   filetypes=[('XML file', '.xml'),
                                              ('All Files', '*.*')])
        if filename is not None and len(filename) > 0:
            self.controller._append_to_output("xml_filename", filename)
            self.controller.XML.set(True)

    def upload_data_file(self):
        """ Opens a window to indicate the path to the data. """

        self.newWindow = tk.Toplevel(self.controller)
        # Window options
        self.newWindow.title('Data upload')
        self.tk.call('wm', 'iconphoto', self.newWindow, ImageTk.PhotoImage(
            file=os.path.join(os.path.join(
                self.script_dir,
                'utils',
                'resources',
                'Assets',
                'VAILabsIcon.ico'))))
        # self.newWindow.geometry("600x200")

        frame1 = tk.Frame(self.newWindow)
        self.label_list = []
        self.var = ['X', 'Y', 'X_test', 'Y_test']
        self.filenames = ['']*len(self.var)
        for r, v in enumerate(self.var):
            v = v + '*' if r == 0 else v
            tk.Label(frame1, text=v,
                     pady=10,
                     padx=10,
                     fg='black'
                     ).grid(column=0, row=r)
            tk.Button(frame1,
                      text="Browse",
                      command=lambda a=r: self.upload_file(a)
                      ).grid(column=1, row=r)
            tk.Button(frame1,
                      text="Delete",
                      command=lambda a=r: self.delete_file(a)
                      ).grid(column=2, row=r)
            self.label_list.append(tk.Label(frame1, text=' '*120,
                                            pady=10,
                                            padx=10,
                                            fg='black'
                                            ))
            self.label_list[-1].grid(column=3, row=r)
        frame2 = tk.Frame(self.newWindow)
        tk.Label(frame2, text='* This data file is mandatory.',
                 pady=10,
                 padx=10,
                 fg='black'
                 ).pack(side=tk.LEFT)
        tk.Button(frame2,
                  text="Done",
                  command=self.start_dataloader
                  ).pack(side=tk.RIGHT, padx=(0, 5))
        frame1.grid(column=0, row=0, sticky="nsew")
        frame2.grid(column=0, row=1, sticky="nsew")

    def upload_file(self, r):
        """ Asks for a file and stores the path and displays it.
        :param r: int type of data variable number.
        """
        filename = askopenfilename(initialdir=os.getcwd(),
                                   title='Select a file',
                                   defaultextension='.csv',
                                   filetypes=[('CSV', '.csv'),
                                              ('All Files', '*.*')])
        self.filenames[r] = filename
        width = 63
        filename = '...' + \
            filename[-width +
                     3:] if filename and len(filename) > width else filename
        self.label_list[r].config(text=filename)

    def delete_file(self, r):
        """ Deletes the specified file from storage and display.
        :param r: int type of data variable number.
        """
        self.filenames[r] = ''
        self.label_list[r].config(text='')

    def start_dataloader(self):
        """ Reads all the selected files, loads the data and passes it to 
        dataLoader.
        """

        # s = XML_handler()
        # s.new_config_file(self.save_path.name)
        # s.filename = self.save_path.name

        # self.s = XML_handler()
        # self.s.new_config_file()

        # self.s._print_xml_config()
        # self.s.load_XML(self.controller.output["xml_filename"])

        data = {}
        isVar = [0] * len(self.var)
        if len(self.label_list[0].cget("text")) > 0:
            for i, filename in enumerate(self.filenames):
                variable = self.var[i]
                if filename is not None and len(filename) > 0:
                    if filename.lower().endswith(('.csv')):
                        # Infers by default, should it be None?
                        data[variable] = pd.read_csv(filename)
                        isVar[i] = 1
                        self.controller.s.append_input_data(variable, self.rel_path(filename))
                        if i == 0:
                            self.controller.Data.set(True)
                        if any(isVar[1::2]) and (
                                len(pd.unique(data[variable].to_numpy().flatten())) < len(data[variable].to_numpy().flatten())*0.2):
                            self.controller.output_type = 'classification' * \
                                all([float(i).is_integer()
                                    for i in data[variable].to_numpy().flatten()])
            if not any(isVar[1::2]):
                self.controller.output_type = 'unsupervised'
            self.newWindow.destroy()
            dataLoader(self.controller, data)
        else:
            tk.messagebox.showwarning(title='Error - X not specified',
                                      message='You need to specify X before proceeding.')

    def rel_path(self, path):
        """ Returns relative path if available. """
        if path[0].lower() == os.getcwd()[0].lower():
            #Same drive
            _folder = os.path.relpath(path, os.getcwd())
            if _folder[:2] == '..':
                # Absolute path
                return path
            else:
                # Relative path
                return os.path.join('.',_folder)
        else: 
            #Different drive -> Absolute path
            return path

    def upload_data_path(self):
        """ Stores the directory containing the data that will be later loaded 
        """
        folder = askdirectory(initialdir=os.getcwd(),
                              title='Select a folder',
                              mustexist=True)
        if folder is not None and len(folder) > 0:
            self.controller.s.append_input_data('X', self.rel_path(folder))
        
    def upload_data_folder(self):
        """ Stores the directory containing the data that will be later loaded 
        """
        folder = askdirectory(initialdir=os.getcwd(),
                              title='Select a folder',
                              mustexist=True)
        if folder is not None and len(folder) > 0:
            onlyfiles = [f for f in os.listdir(
                folder) if os.path.isfile(os.path.join(folder, f))]
            self.upload_data_file()
            for file in onlyfiles:
                name = file.lower()
                filename = os.path.join(folder, file)
                width = 63
                filenm = '...' + \
                    filename[-width +
                             3:] if filename and len(filename) > width else filename
                if name.endswith(('.csv')):
                    name = ''.join(ch for ch in name if ch.isalnum())
                    if 'test' in name or 'tst' in name:
                        if name[0] == 'x':
                            self.filenames[2] = filename
                            self.label_list[2].config(text=filenm)
                        elif name[0] == 'y':
                            self.filenames[3] = filename
                            self.label_list[3].config(text=filenm)
                    else:
                        if name[0] == 'x':
                            self.filenames[0] = filename
                            self.label_list[0].config(text=filenm)
                        elif name[0] == 'y':
                            self.filenames[1] = filename
                            self.label_list[1].config(text=filenm)
