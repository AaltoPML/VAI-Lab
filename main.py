# -*- coding: utf-8 -*-
"""
Created on Wed Mar  2 12:51:28 2022

@author: Sevisal
"""

import tkinter as tk                # python 3
from tkinter import font  as tkfont # python 3
import os
from PIL import Image, ImageTk
from tkinter import messagebox
from tkinter.filedialog import askopenfilename

from Inputs_general import PageManual, PageCanvas

class UFA(tk.Tk):
    """  """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title_font = tkfont.Font(family='Helvetica', 
                                      size=14, weight="bold")#, slant="italic")
        self.pages_font = tkfont.nametofont("TkDefaultFont")

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = tk.Frame(self, bg = '#19232d')
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        self.frames = {}
        for F in (StartPage, PageManual, PageCanvas):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()

class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        " Here we define the main frame displayed upon opening the program."
        " This leads to the different methods to provide feedback."
        super().__init__(parent, bg = parent['bg'])
        self.controller = controller
        self.controller.title('User feedback adaptation')
        self.controller.iconbitmap(
            os.path.join(os.getcwd(),'Icons','UFAIcon.ico'))
        
        self.my_img1 = ImageTk.PhotoImage(Image.open(os.path.join(
                os.getcwd(), 'Icons', 'UFAIcon_name.png')).resize((600, 400)))
        self.my_label = tk.Label(self, image = self.my_img1, bg = parent['bg'])
        self.my_label.grid(column = 0, row = 0, rowspan = 10, columnspan = 4)
        
        my_label = tk.Label(
            self, 
            text = 'Choose your prefered method '
            +'to give feedback to the model.', 
            pady= 10, font = controller.title_font, 
            bg = parent['bg'], fg = 'white')
        my_label.grid(column = 0, row = 11,columnspan = 4)

        button_speak = tk.Button(
            self, text = 'Speak', fg = 'white', font = controller.title_font, 
            bg = parent['bg'], height = 3, width = 20, 
            command = self.NotImpl).grid(column = 0, row = 59)
        button_write = tk.Button(
            self, text = 'Write', fg = 'white', font = controller.title_font, 
            bg = parent['bg'], height = 3, width = 20, 
            command = self.NotImpl).grid(column = 1, row = 59)
        button_manual = tk.Button(
            self, text = 'Manual input', fg = 'white', 
            font = controller.title_font, bg = parent['bg'], height = 3, 
            width = 20, command = lambda:  controller.show_frame(
                "PageManual")).grid(column = 2, row = 59)
        button_canvas = tk.Button(
            self, text = 'Interact with canvas', fg = 'white', 
            font = controller.title_font, bg = parent['bg'], height = 3, 
            width = 20, command = lambda:  controller.show_frame(
                "PageCanvas")).grid(column = 3, row = 59)
        button_upload = tk.Button(
            self, text = 'Upoad file', fg = 'white', 
            font = controller.title_font, bg = parent['bg'], height = 3, 
            width = 20, command = self.upload_data).grid(column = 0, row = 60)
        
    # def light_theme(self):
    #     listbox_tasks.config(bg="white", fg="black")
    #     button_add_task.config(highlightbackground='white')
    #     button_delete_task.config(highlightbackground='white')
    #     button_load_tasks.config(highlightbackground='white')
    #     button_save_tasks.config(highlightbackground='white')
    #     entry_task.config(bg='white', fg='black')       
        
    def NotImpl(self):
        messagebox.showwarning(
            "Error", "This functionality is not implemented yet.")
        
    def upload_data(self):
        filename = askopenfilename(
            initialdir = os.getcwd(), title = 'Select a file', 
            defaultextension = '.csv', filetypes = [('Text file', '.txt'), 
                                                    ('CSS file', '.css'), 
                                                    ('All Files', '*.*')])
        if filename is not None:
            messagebox.showinfo("Success", "Feedback correctly uploaded.")

if __name__ == "__main__":
    app = UFA()
    app.mainloop()