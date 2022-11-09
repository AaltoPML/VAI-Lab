from vai_lab._plugin_templates import UI
from vai_lab._import_helper import get_lib_parent_dir
from vai_lab._types import DictT, DataInterface, GUICoreInterface

import os
import numpy as np
import pandas as pd
from typing import Tuple, List, Union
from PIL import Image, ImageTk, PngImagePlugin

import tkinter as tk
from tkinter import messagebox, ttk
from tkinter.filedialog import asksaveasfile

_PLUGIN_READABLE_NAMES = {"manual": "default",
                          "binary": "alias",
                          "classification": "alias"}            # type:ignore
_PLUGIN_MODULE_OPTIONS = {"layer_priority": 2,
                          "required_children": None}            # type:ignore
_PLUGIN_REQUIRED_SETTINGS = {"image_dir": "str"}                # type:ignore
_PLUGIN_OPTIONAL_SETTINGS = {}                                  # type:ignore
_PLUGIN_REQUIRED_DATA = {"X", "Y"}                              # type:ignore


class ManualInput(tk.Frame, UI):            # type:ignore
    """Method of user interaction for binary or classification data"""

    def __init__(self, parent, controller, config: DictT):
        self.parent = parent
        super().__init__(parent, bg=self.parent['bg'])
        self.controller: GUICoreInterface = controller
        self.controller.title('Manual Input')

        self.dirpath = get_lib_parent_dir()

        
        self.assets_path = os.path.join(self.dirpath, 'utils', 'resources', 'Assets')

        self._data_in: DataInterface
        self._class_list = None
        self._config = config
        self.save_path = ''
        self.saved = True
        

    def _load_images_from_data(self):
        self.image_list: List[Union[ImageTk.PhotoImage,Image.Image]] = []
        pixels = 500
        for f in self._data_in["X"].keys():
            self.image_list.append(
                ImageTk.PhotoImage(
                    self.expand2square(Image.fromarray(self._data_in["X"][f]), (0, 0, 0))
                    .resize((pixels, pixels))))

        # Inital window
        self.my_label = tk.Label(self, image=self.image_list[0],
                                 bg=self.parent['bg'])
        self.my_label.grid(column=0, row=0, rowspan=10, columnspan=3)
        self.N = len(self._data_in["X"])

        # Status bar in the lower part of the window
        status = tk.Label(self, text='Image 1 of '+str(self.N), bd=1,
                          relief=tk.SUNKEN, anchor=tk.E, fg='white',
                          bg=self.parent['bg'])
        status.grid(row=20, column=0, columnspan=4, pady=10,
                    sticky=tk.W+tk.E)

        self.frame1 = tk.Frame(self, bg=self.parent['bg'])
        frame4 = tk.Frame(self, bg=self.parent['bg'])
        frame5 = tk.Frame(self, bg=self.parent['bg'])
        frame6 = tk.Frame(self, bg=self.parent['bg'])

        # Buttons initialisation
        self.back_img = ImageTk.PhotoImage(Image.open(
            os.path.join(self.assets_path, 'back_arrow.png')).resize((150, 50)))
        self.forw_img = ImageTk.PhotoImage(Image.open(
            os.path.join(self.assets_path, 'forw_arrow.png')).resize((150, 50)))
        self.button_back = tk.Button(
            frame4, image=self.back_img, bg=self.parent['bg'],
            state=tk.DISABLED)
        self.button_back.grid(column=0, row=19, padx=(
            10, 0), pady=10, sticky="news")
        self.button_save = tk.Button(
            frame4, text='Save', fg='white', bg=self.parent['bg'], height=3,
            width=20, command=self.save_file)
        self.button_save.grid(column=1, row=19, sticky="news", pady=10)
        self.button_forw = tk.Button(
            frame4, image=self.forw_img, bg=self.parent['bg'],
            command=lambda: self.forward_back(2))
        self.button_forw.grid(column=2, row=19, sticky="news", pady=10)

        tk.Button(
            frame5, text="Done",
            fg='white', bg=self.parent['bg'],
            height=3, width=20,
            command=self.check_quit).grid(column=4, row=19, sticky="news", pady=10)

        img = self.image_list[0]
        self.my_img = tk.Label(self.frame1, image=img,
                               bg=self.parent['bg'])
        self.my_img.pack(fill=tk.BOTH, expand=True, padx=(10, 0), pady=(10, 0))
        self.my_img.bind("<Configure>", self.resizing)

        self.frame1.grid(row=0, column=0, sticky="nsew")
        # self.frame3.grid(row = 0, column = 2, sticky="nsew", pady=10, padx=10)
        frame4.grid(row=1, column=0, sticky="sew")
        frame5.grid(row=1, column=1, sticky="sew")
        frame6.grid(row=2, column=0, columnspan=3, sticky="sew")

        frame4.grid_columnconfigure(tuple(range(3)), weight=1)
        self.grid_rowconfigure(0, weight=3)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(tuple(range(3)), weight=1)
        self.grid_columnconfigure(0, weight=2)

    def set_data_in(self, data_in):
        req_check = [
            r for r in _PLUGIN_REQUIRED_DATA if r not in data_in.keys()]
        if len(req_check) > 0:
            raise Exception("Minimal Data Requirements not met"
                            + "\n\t{0} ".format("ManualInput")
                            + "requires data: {0}".format(_PLUGIN_REQUIRED_DATA)
                            + "\n\tThe following data is missing:"
                            + "\n\t\u2022 {}".format(",\n\t\u2022 ".join([*req_check])))
        self._data_in = data_in
        self._load_images_from_data()
        self._load_classes_from_data()

    def class_list(self):
        """Getter for required _class_list variable

        :return: list of class labels
        :rtype: list of strings
        """
        return self._class_list

    def _load_classes_from_data(self):
        """Setter for required _class_list variable

        :param value: class labels for binary classification
        :type value: list of strings
        """
        self._class_list = list(self._data_in["Y"]["Class"])
        self.out_data = np.zeros((self.N, len(self._class_list)))

        frame2 = tk.Frame(self, bg=self.parent['bg'])
        frame2.grid(row=0, column=1, sticky="nsew")

        self.button_cl = {}

        self.var = {}
        for i, cl in enumerate(self._class_list):
            self.var[0, i] = tk.IntVar(value=self.out_data[0, i])
            self.button_cl[cl] = tk.Checkbutton(
                frame2, text=cl, fg='white', bg=self.parent['bg'],
                selectcolor='black', height=3, width=20,
                variable=self.var[0, i],
                command=(lambda i=i: self.onPress(0, i)))
            self.button_cl[cl].grid(column=4, row=i)

        # Tree defintion. Output display
        style = ttk.Style()
        style.configure(
            "Treeview", background='white', foreground='white',
            rowheight=25, fieldbackground='white',
            font=self.controller.pages_font)
        style.configure("Treeview.Heading", font=self.controller.pages_font)
        style.map('Treeview', background=[('selected', 'grey')])

        tree_frame = tk.Frame(self)
        tree_frame.grid(row=0, column=2, sticky="nsew", pady=10, padx=10)

        tree_scrollx = tk.Scrollbar(tree_frame, orient='horizontal')
        tree_scrollx.pack(side=tk.BOTTOM, fill=tk.X)
        tree_scrolly = tk.Scrollbar(tree_frame)
        tree_scrolly.pack(side=tk.RIGHT, fill=tk.Y)

        self.tree = ttk.Treeview(tree_frame,
                                 yscrollcommand=tree_scrolly.set,
                                 xscrollcommand=tree_scrollx.set)
        self.tree.pack(fill='both', expand=True)

        tree_scrollx.config(command=self.tree.xview)
        tree_scrolly.config(command=self.tree.yview)

        self.tree['columns'] = self._class_list

        # Format columns
        self.tree.column("#0", width=80,
                         minwidth=50)
        for n, cl in enumerate(self._class_list):
            self.tree.column(
                cl, width=int(self.controller.pages_font.measure(str(cl)))+20,
                minwidth=50, anchor=tk.CENTER)
        # Headings
        self.tree.heading("#0", text="Image", anchor=tk.CENTER)
        for cl in self._class_list:
            self.tree.heading(cl, text=cl, anchor=tk.CENTER)
        self.tree.tag_configure('odd', foreground='black',
                                background='#E8E8E8')
        self.tree.tag_configure('even', foreground='black',
                                background='#DFDFDF')
        # Add data
        for n, sample in enumerate(self.out_data):
            if n % 2 == 0:
                self.tree.insert(parent='', index='end', iid=n, text=n+1,
                                 values=tuple(sample.astype(int)), tags=('even',))
            else:
                self.tree.insert(parent='', index='end', iid=n, text=n+1,
                                 values=tuple(sample.astype(int)), tags=('odd',))

        # Select the current row
        self.tree.selection_set(str(int(0)))

        # Define double-click on row action
        self.tree.bind("<Double-1>", self.OnDoubleClick)

    def expand2square(self,
                        pil_img :PngImagePlugin.PngImageFile,
                        background_color :Tuple):
        " Adds padding to make the image a square."
        width, height = pil_img.size
        if width == height:
            return pil_img
        elif width > height:
            result = Image.new(pil_img.mode, (width, width), background_color)
            result.paste(pil_img, (0, (width - height) // 2))
            return result
        else:
            result = Image.new(pil_img.mode, (height, height),
                               background_color)
            result.paste(pil_img, ((height - width) // 2, 0))
            return result

    def resizing(self, event):
        """ Resizes window to tree view height and buttons width """
        n = int(self.tree.selection()[0])
        iw, ih = self.image_list[n].width, self.image_list[n].height
        iw = iw() if type(iw) is not int else iw
        ih = ih() if type(ih) is not int else ih

        mw, mh = self.frame1.winfo_width()-14, self.frame1.winfo_height() - \
            14  # Frame border correction
        if (iw != mw) and (ih != mh):
            if iw > ih:
                ih = ih*(mw/iw)
                r = mh/ih if (ih/mh) > 1 else 1
                iw, ih = mw*r, ih*r
            else:
                iw = iw*(mh/ih)
                r = mw/iw if (iw/mw) > 1 else 1
                iw, ih = iw*r, mh*r
            
            if type(self.image_list[n]) == ImageTk.PhotoImage:
                _temp_img:Image = ImageTk.getimage(self.image_list[n])
            else:
                _temp_img:Image = self.image_list[n]

            self.image_list[n] = ImageTk.PhotoImage(_temp_img.resize((int(iw), int(ih))))
        self.my_img.config(image=self.image_list[n])

    def check_quit(self):

        if not self.saved:
            response = messagebox.askokcancel(
                "Exit?",
                "Do you want to leave the program without saving?")
            if response:
                self.controller.destroy()
        else:
            response = messagebox.askokcancel(
                "Exit?",
                "Are you sure you are finished?")
            self.controller.destroy()

    def save_file_as(self):

        self.save_path = asksaveasfile(mode='w')
        self.save_file()

    def save_file(self):

        if self.save_path == '':
            self.save_path = asksaveasfile(defaultextension='.txt',
                                           filetypes=[('Text file', '.txt'),
                                                      ('CSV file', '.csv'),
                                                      ('All Files', '*.*')])
        # asksaveasfile return `None` if dialog closed with "cancel".
        if self.save_path is not None:
            filedata = pd.DataFrame(
                self.out_data, columns=self._class_list).to_string()
            self.save_path.seek(0)  # Move to the first row to overwrite it
            self.save_path.write(filedata)
            self.save_path.flush()  # Save without closing
            # typically the above line would do. however this is used to ensure that the file is written
            os.fsync(self.save_path.fileno())
            self.saved = True

    def forward_back(self, image_number):
        " Forward button to continue to the next image in the folder."

        self.tree.selection_set(str(int(image_number-1)))
        # Print the corresponding image
        self.resizing((0, 0))

        # Update button commands
        self.button_forw.config(image=self.forw_img, bg=self.parent['bg'],
                                command=lambda: self.forward_back(
                                    image_number+1),
                                text='', state=tk.NORMAL)
        self.button_back.config(image=self.back_img, bg=self.parent['bg'],
                                command=lambda: self.forward_back(
                                    image_number-1),
                                text='', state=tk.NORMAL)
        if image_number == self.N:
            self.button_forw.config(state=tk.DISABLED)
        if image_number == 1:
            self.button_back.config(state=tk.DISABLED)

        # Classes buttons
        # var = {}
        for i, cl in enumerate(self._class_list):
            # print(out_data[image_number-1,i])
            self.var[image_number-1, i] = tk.IntVar(
                value=int(self.out_data[image_number-1, i]))
            # var[i] = tk.IntVar(value = int(self.out_data[image_number-1,i]))
            # I can not make this be selected when going backwards or forward
            # if it was previously selected.
            self.button_cl[cl].config(text=cl, fg='white', bg=self.parent['bg'],
                                      selectcolor='black', height=3, width=20,
                                      variable=self.var[image_number-1, i],
                                      command=(lambda i=i: self.onPress(image_number-1, i)))

        # # Status bar
        # status = tk.Label(
        #     self, text='Image ' + str(image_number) + ' of '+str(self.N),
        #     bd = 1, relief = tk.SUNKEN, anchor = tk.E, fg = 'white',
        #     bg = self.parent['bg'])
        # status.grid(row=20, column=0, columnspan=4, pady = 10,
        #             sticky = tk.W+tk.E)

    def onPress(self, n, i):
        "Updates the stored values on clicking the checkbutton."

        self.out_data[n, i] = not self.out_data[n, i]
        self.tree.item(self.tree.get_children()[n], text=n+1,
                       values=tuple(self.out_data[n, :].astype(int)))
        self.saved = False

    def OnDoubleClick(self, event):
        "Moves to the image corresponding to the row clicked on the tree."

        item = self.tree.selection()[0]
        self.forward_back(self.tree.item(item, "text"))
