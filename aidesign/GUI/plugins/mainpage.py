import tkinter as tk
import os
from PIL import Image, ImageTk
from tkinter import messagebox
from tkinter.filedialog import askopenfilename, askdirectory

class MainPage(tk.Frame):

    def __init__(self, parent, controller):
        " Here we define the main frame displayed upon opening the program."
        " This leads to the different methods to provide feedback."
        super().__init__(parent, bg = parent['bg'])
        self.controller = controller
        self.controller.title('User feedback adaptation')
        
        script_dir = os.path.dirname(__file__)
        self.my_img1 = ImageTk.PhotoImage(
                            Image.open(
                                os.path.join(
                                    script_dir,
                                    'resources',
                                    'Assets',
                                    'UFAIcon_name.png')
                                    ).resize((600, 400))
                                )
        self.my_label = tk.Label(self, 
                                    image = self.my_img1,
                                    bg = parent['bg'])

        self.my_label.grid(column = 0,
                            row = 0,
                            rowspan = 10,
                            columnspan = 4)
        
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
                    text = 'Data folder',
                    fg = 'white',
                    font = controller.title_font, 
                    bg = parent['bg'],
                    height = 3,
                    width = 20, 
                    command = self.upload_data,
                    ).grid(column = 0, row = 12, padx= 10)
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
                    command = self.canvas
                    ).grid(column = 0, row = 13, padx= 10)

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
        
    # def light_theme(self):
    #     listbox_tasks.config(bg="white", fg="black")
    #     button_add_task.config(highlightbackground='white')
    #     button_delete_task.config(highlightbackground='white')
    #     button_load_tasks.config(highlightbackground='white')
    #     button_save_tasks.config(highlightbackground='white')
    #     entry_task.config(bg='white', fg='black')       
    
    def canvas(self):
        self.controller.show_frame("aidCanvas")
    
    def upload_xml(self):
        filename = askopenfilename(initialdir = os.getcwd(), 
                                   title = 'Select a file', 
                                   defaultextension = '.xml', 
                                   filetypes = [('XML file', '.xml'), 
                                                ('All Files', '*.*')])
        self.controller.core.load_config_file(filename)
        self.controller.XMLlabel.config(text = 'Done!', fg = 'green')

    def upload_data(self):
        filename = askdirectory(initialdir = os.getcwd(),
                                    title = 'Select a folder',
                                    mustexist = True)
        if filename is not None:
            self.controller.Datalabel.config(text = 'Done!', fg = 'green')