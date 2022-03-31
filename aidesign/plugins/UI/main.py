# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import font  as tkfont
import os
from PIL import Image, ImageTk
from tkinter import messagebox
from tkinter.filedialog import askopenfilename
from sys import modules as get_module_name
from . import PageCanvas
from . import PageManual

class Container(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title_font = tkfont.Font(family='Helvetica', 
                                        size=14, 
                                        weight="bold")
        self.pages_font = tkfont.nametofont("TkDefaultFont")
        self.current_module_name = get_module_name[__name__]

        self.desired_ui_types = []
        self.top_ui_layer = None
        self.startpage_exist = False
        self.available_ui_types = {
            "StartPage":{
                            "name":"startpage",
                            "layer_priority":1,
                            "required_children":["PageManual","PageCanvas"]
                            },
            "PageManual":{
                            "name":"manual",
                            "layer_priority":2,
                            "required_children":None
                            },
            "PageCanvas":{
                            "name":"canvas",
                            "layer_priority":2,
                            "required_children":None
                            }
        }

    def compare_layer_priority(self,ui_name):
        """Check if a new module should have higher layer priority than the existing one

        :param ui_name: name of the UI method being compared
        :type ui_name: str
        """
        if self.top_ui_layer == None:
            self.top_ui_layer = ui_name
        else:
            current_top_layer = self.available_ui_types[self.top_ui_layer]["layer_priority"]
            candidate_layer = self.available_ui_types[ui_name]["layer_priority"]
            self.top_ui_layer = candidate_layer \
                                    if candidate_layer < current_top_layer \
                                    else self.top_ui_layer


    def add_UI_type_to_frames(self,ui_name):
        """Add user defined UI method to list of frames to be loaded
        
        :param ui_name: name of the UI method being loaded
        :type ui_name: str 
        """
        self.desired_ui_types.append(getattr(self.current_module_name,ui_name))
        self.compare_layer_priority(ui_name)
        if self.available_ui_types[ui_name]["required_children"] != None:
            for children in self.available_ui_types[ui_name]["required_children"]:
                self.add_UI_type_to_frames(children)
        

    def set_UI_type(self,ui_type):
        """"Given user input, create a list of classes of the corresponding User Interface Type 

        :param ui_name: name of the desired User Interface Method
        :type ui_name: str or list
        """        
        ui_type = ui_type\
                    if isinstance(ui_type, list)\
                    else [ui_type] # put ui_type in list if not already

        for ui in ui_type:
            ui_name = ''.join(kn for kn in self.available_ui_types.keys()\
                            if ui.lower() == self.available_ui_types[kn]["name"])
            try:
                self.add_UI_type_to_frames(ui_name)
                self.startpage_exist = 1 if ui_name == "StartPage" else self.startpage_exist
            except:
                from sys import exit
                print ("Error: User Interface \"{0}\" not recognised.".format(ui))
                print ("Available methods are:")
                print ("   - {}".format(",\n   - ".join([i["name"] for i in self.available_ui_types.values()])))
                exit(1)

    def set_class_list(self,class_list):
        self._class_list = class_list

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()

    def launch(self):
        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = tk.Frame(self, bg = '#19232d')
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        # for F in (StartPage, PageManual, PageCanvas):
        for F in self.desired_ui_types:
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            if page_name != "StartPage":
                frame.class_list(self._class_list)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(self.top_ui_layer)
        self.mainloop()

class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        " Here we define the main frame displayed upon opening the program."
        " This leads to the different methods to provide feedback."
        super().__init__(parent, bg = parent['bg'])
        self.controller = controller
        self.controller.title('User feedback adaptation')
        # self.controller.iconbitmap(os.path.join(os.getcwd(),'Icons','UFAIcon.ico'))
        
        script_dir = os.path.dirname(__file__)
        # self.my_img1 = ImageTk.PhotoImage(Image.open(os.path.join(os.getcwd(), 'resources', 'Assets', 'UFAIcon_name.png')).resize((600, 400)))
        self.my_img1 = ImageTk.PhotoImage(Image.open(os.path.join(script_dir, 'resources', 'Assets', 'UFAIcon_name.png')).resize((600, 400)))
        self.my_label = tk.Label(self, image = self.my_img1, bg = parent['bg'])
        self.my_label.grid(column = 0, row = 0, rowspan = 10, columnspan = 4)
        
        my_label = tk.Label(self, text = 'Choose your prefered method to give feedback to the model.', 
                            pady= 10, font = controller.title_font, bg = parent['bg'], fg = 'white')
        my_label.grid(column = 0, row = 11,columnspan = 4)

        button_speak = tk.Button(self, text = 'Speak', fg = 'white', font = controller.title_font, 
                                 bg = parent['bg'], height = 3, width = 20, command = self.NotImpl).grid(column = 0, row = 59)
        button_write = tk.Button(self, text = 'Write', fg = 'white', font = controller.title_font, 
                                 bg = parent['bg'], height = 3, width = 20, command = self.NotImpl).grid(column = 1, row = 59)
        button_manual = tk.Button(self, text = 'Manual input', fg = 'white', font = controller.title_font, 
                                  bg = parent['bg'], height = 3, width = 20, 
                                  command = lambda:  controller.show_frame("PageManual")).grid(column = 2, row = 59)
        button_canvas = tk.Button(self, text = 'Interact with canvas', fg = 'white', font = controller.title_font, 
                                  bg = parent['bg'], height = 3, width = 20, 
                                  command = lambda:  controller.show_frame("PageCanvas")).grid(column = 3, row = 59)
        button_upload = tk.Button(self, text = 'Upoad file', fg = 'white', font = controller.title_font, 
                                  bg = parent['bg'], height = 3, width = 20, 
                                  command = self.upload_data).grid(column = 0, row = 60)
        
    # def light_theme(self):
    #     listbox_tasks.config(bg="white", fg="black")
    #     button_add_task.config(highlightbackground='white')
    #     button_delete_task.config(highlightbackground='white')
    #     button_load_tasks.config(highlightbackground='white')
    #     button_save_tasks.config(highlightbackground='white')
    #     entry_task.config(bg='white', fg='black')       
        
    def NotImpl(self):
        messagebox.showwarning("Error", "This functionality is not implemented yet.")
        
    def upload_data(self):
        filename = askopenfilename(initialdir = os.getcwd(), title = 'Select a file', defaultextension = '.csv', 
                                   filetypes = [('Text file', '.txt'), ('CSS file', '.css'), ('All Files', '*.*')])
        if filename is not None:
            messagebox.showinfo("Success", "Feedback correctly uploaded.")

# class PageCanvas(tk.Frame):

#     def __init__(self, parent, controller):
#         tk.Frame.__init__(self, parent, bg = parent['bg'])
#         self.controller = controller
#         label = tk.Label(self, text="This is page 2", font=controller.title_font)
#         label.pack(side="top", fill="x", pady=10)
#         button = tk.Button(self, text="Go to the start page",
#                            command=lambda: controller.show_frame("StartPage"))
#         button.pack()


if __name__ == "__main__":
    app = Container()
    app.mainloop()