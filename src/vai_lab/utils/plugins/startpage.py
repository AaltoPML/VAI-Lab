from vai_lab._import_helper import get_lib_parent_dir

import tkinter as tk
import os
from PIL import Image, ImageTk
from tkinter import messagebox
from tkinter.filedialog import askopenfilename
import pandas as pd

_PLUGIN_READABLE_NAMES = {"start": "default",
                          "start page": "alias"}                    # type:ignore
_PLUGIN_MODULE_OPTIONS = {}                                         # type:ignore
_PLUGIN_REQUIRED_SETTINGS = {}                                      # type:ignore
_PLUGIN_OPTIONAL_SETTINGS = {}                                      # type:ignore


class StartPage(tk.Frame):
    """Main Page for launching GUI methods"""

    def __init__(self, parent, controller):
        " Here we define the main frame displayed upon opening the program."
        " This leads to the different methods to provide feedback."
        super().__init__(parent, bg=parent['bg'])
        self.controller = controller
        self.controller.title('User interaction adaptation')

        # script_dir = os.path.dirname(__file__)
        self.out_data = pd.DataFrame()
        script_dir = get_lib_parent_dir()
        self.my_img1 = ImageTk.PhotoImage(
            Image.open(
                os.path.join(
                    script_dir,
                    "utils",
                    'resources',
                    'Assets',
                    'UFAIcon_name.png')
            ).resize((600, 400))
        )

        self.my_label = tk.Label(self,
                                 image=self.my_img1,
                                 bg=parent['bg'])

        self.my_label.grid(column=0,
                           row=0,
                           rowspan=10,
                           columnspan=4)

        my_label = tk.Label(self,
                            text='Choose feedback method ...',
                            pady=10,
                            font=controller.title_font,
                            bg=parent['bg'],
                            fg='white')

        my_label.grid(column=0,
                      row=11,
                      columnspan=4)

        button_speak = tk.Button(self,
                                 text='Speak',
                                 fg='white',
                                 font=controller.title_font,
                                 bg=parent['bg'],
                                 height=3,
                                 width=20,
                                 command=self.NotImpl
                                 ).grid(column=0, row=59)

        button_write = tk.Button(self,
                                 text='Write',
                                 fg='white',
                                 font=controller.title_font,
                                 bg=parent['bg'],
                                 height=3,
                                 width=20,
                                 command=self.NotImpl
                                 ).grid(column=1, row=59)

        button_manual = tk.Button(self,
                                  text='Manual input',
                                  fg='white',
                                  font=controller.title_font,
                                  bg=parent['bg'],
                                  height=3,
                                  width=20,
                                  command=lambda: controller.show_frame(
                                      "PageManual")
                                  ).grid(column=2, row=59)

        button_canvas = tk.Button(self,
                                  text='Interact with canvas',
                                  fg='white',
                                  font=controller.title_font,
                                  bg=parent['bg'],
                                  height=3,
                                  width=20,
                                  command=lambda: controller.show_frame(
                                      "PageCanvas")
                                  ).grid(column=3, row=59)

        button_upload = tk.Button(self,
                                  text='Upoad file',
                                  fg='white',
                                  font=controller.title_font,
                                  bg=parent['bg'],
                                  height=3,
                                  width=20,
                                  command=self.upload_data
                                  ).grid(column=0, row=60)

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
        filename = askopenfilename(initialdir=os.getcwd(),
                                   title='Select a file',
                                   defaultextension='.csv',
                                   filetypes=[
            ('Text file', '.txt'),
            ('CSS file', '.css'),
            ('All Files', '*.*')
        ])
        if filename is not None:
            messagebox.showinfo("Success", "Feedback correctly uploaded.")
