from vai_lab._plugin_templates import UI
from vai_lab._import_helper import get_lib_parent_dir

import os
import numpy as np
import pandas as pd
from typing import Tuple, List, Union
from PIL import Image, ImageTk, PngImagePlugin
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import tkinter as tk
from tkinter import messagebox, ttk
from tkinter.filedialog import asksaveasfile

_PLUGIN_READABLE_NAMES = {"OptimisationInput": "default",
                          "BOUI": "alias",
                          "optimisationUI": "alias"}            # type:ignore
_PLUGIN_MODULE_OPTIONS = {"layer_priority": 2,
                          "required_children": None}            # type:ignore
_PLUGIN_REQUIRED_SETTINGS = {}                                  # type:ignore
_PLUGIN_OPTIONAL_SETTINGS = {"Bounds": "list"}                      # type:ignore
_PLUGIN_REQUIRED_DATA = {"X"}                                   # type:ignore


class OptimisationInput(tk.Frame, UI):            # type:ignore
    """Method of user interaction for optimisation problems"""

    def __init__(self, parent, controller, config):
        self.parent = parent
        super().__init__(parent, bg=self.parent['bg'])
        self.controller = controller
        self.controller.title('Optimisation Interaction')

        self.dirpath = get_lib_parent_dir()
        self.tk.call('wm', 'iconphoto', self.controller._w, ImageTk.PhotoImage(
            file=os.path.join(os.path.join(
                self.dirpath,
                'utils',
                'resources',
                'Assets',
                'VAILabsIcon.ico'))))
        
        self.assets_path = os.path.join(self.dirpath, 'utils', 'resources', 'Assets')

        self._data_in
        self._config = config
        self.save_path = ''
        self.saved = True
        

    def _load_values_from_data(self):

        self.frame1 = tk.Frame(self, bg=self.parent['bg'])
        frame4 = tk.Frame(self, bg=self.parent['bg'])
        frame5 = tk.Frame(self, bg=self.parent['bg'])
        # frame6 = tk.Frame(self, bg=self.parent['bg'])

        self.opt_var = list(self._data_in["X"].columns.values)
        if len(self.opt_var) < 3:
            figure = plt.Figure(figsize=(5, 4), dpi=100)
            self.ax = figure.add_subplot(111)

            self.plot_points(self._data_in["X"], self.opt_var)

            self.canvas = FigureCanvasTkAgg(figure, self.frame1)
            plot_frame = self.canvas.get_tk_widget()
            plot_frame.grid(column=0, row=0, pady=10, padx=10, sticky="nsew")
            self.frame1.grid_rowconfigure(0, weight=1)
            self.frame1.grid_columnconfigure(0, weight=1)

        # Inital window
        self.N = len(self._data_in["X"])

        # Buttons
        self.button_save = tk.Button(
            frame4, text='Save', fg='white', bg=self.parent['bg'], height=3,
            width=20, command=self.save_file)
        self.button_save.grid(column=0, row=0, sticky="news", pady=2, padx=[2,0])

        tk.Button(
            frame5, text="Done",
            fg='white', bg=self.parent['bg'],
            height=3, width=20,
            command=self.check_quit).grid(column=0, row=0, sticky="news", pady=2, padx=[0,2])

        self.frame1.grid(row=0, column=0, sticky="nsew")
        frame4.grid(row=1, column=0, sticky="nsew")
        frame5.grid(row=1, column=1, sticky="nsew")

        frame4.grid_columnconfigure(0, weight=1)
        frame5.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(tuple(range(2)), weight=1)

    def plot_points(self, data, labels, x=[None]):
        """Plots points in pre-existing axis. If some extra points are given,
        these are plotted with a different colour.
        :param data: dict, dictionary to be plotted
        :param labels: list, column and axis labels
        :param x: array, extra points to be plotted
         """
        
        self.ax.clear()         # clear axes from previous plot
        self.ax.scatter(data[labels[0]], data[labels[1]])
        self.ax.set_xlabel(labels[0])
        self.ax.set_ylabel(labels[1])
        # self.ax.set_xlim(min(data[labels[0]]), max(data[labels[0]]))
        # self.ax.set_ylim(min(data[labels[0]]), max(data[labels[0]]))
        self.ax.set_title('Suggested points')
        if None not in x: 
            self.ax.scatter(x[0], x[1], color='r')

    def set_data_in(self, data_in):
        req_check = [
            r for r in _PLUGIN_REQUIRED_DATA if r not in data_in.keys()]
        if len(req_check) > 0:
            raise Exception("Minimal Data Requirements not met"
                            + "\n\t{0} ".format("OptimisationInput")
                            + "requires data: {0}".format(_PLUGIN_REQUIRED_DATA)
                            + "\n\tThe following data is missing:"
                            + "\n\t\u2022 {}".format(",\n\t\u2022 ".join([*req_check])))
        self._data_in = data_in
        self._load_values_from_data()
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
        self.out_data = self._data_in["X"]

        self.button_cl = {}

        # Tree defintion. Output display
        style = ttk.Style()
        style.configure(
            "Treeview", background='white', foreground='white',
            rowheight=25, fieldbackground='white',
            font=self.controller.pages_font)
        style.configure("Treeview.Heading", font=self.controller.pages_font)
        style.map('Treeview', background=[('selected', 'grey')])

        tree_frame = tk.Frame(self)
        if len(self.opt_var) < 3:
            tree_frame.grid(row=0, column=1, sticky="nsew", pady=10, padx=10)
        else:
            tree_frame.grid(row=0, column=0, columnspan = 2, sticky="nsew", pady=10, padx=10)

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

        self.tree['columns'] = self.opt_var

        # Format columns
        self.tree.column("#0", width=80,
                         minwidth=50)
        for n, cl in enumerate(self.opt_var):
            self.tree.column(
                cl, width=int(self.controller.pages_font.measure(str(cl)))+20,
                minwidth=50, anchor=tk.CENTER)
        # Headings
        self.tree.heading("#0", text="Sample", anchor=tk.CENTER)
        for cl in self.opt_var:
            self.tree.heading(cl, text=cl, anchor=tk.CENTER)
        self.tree.tag_configure('odd', foreground='black',
                                background='#E8E8E8')
        self.tree.tag_configure('even', foreground='black',
                                background='#DFDFDF')
        # Add data
        for n, sample in enumerate(self.out_data.values):
            if n % 2 == 0:
                self.tree.insert(parent='', index='end', iid=n, text=n+1,
                                 values=tuple(sample.astype(float)), tags=('even',))
            else:
                self.tree.insert(parent='', index='end', iid=n, text=n+1,
                                 values=tuple(sample.astype(float)), tags=('odd',))

        # Select the current row
        self.tree.selection_set(str(int(0)))

        # Define click on row action
        if len(self.opt_var) < 3:
            self.tree.bind('<ButtonRelease-1>', self.OnClick)

        # Define double-click on row action
        self.tree.bind("<Double-1>", self.OnDoubleClick)

    def OnClick(self, event):
        "Displays the corresponding ."

        item = self.tree.selection()[0]
        x = [float(i) for i in self.tree.item(item)['values']] 
        if len(self.opt_var) < 3:
            self.plot_points(self.out_data, self.opt_var, x = x)
            self.canvas.draw()

    def OnDoubleClick(self, event):
        """ Executed when a row is double clicked.
        Opens an entry box to edit a cell and updates the plot and the 
        stored data. """

        self.treerow = int(self.tree.identify_row(event.y))
        self.treecol = self.tree.identify_column(event.x)

        # get column position info
        x, y, width, height = self.tree.bbox(self.treerow, self.treecol)

        # y-axis offset
        pady = height // 2
        # pady = 0

        if hasattr(self, 'entry'):
            self.entry.destroy()

        self.entry = tk.Entry(self.tree, justify='center')

        if int(self.treecol[1:]) > 0:
            self.entry.insert(
                0, self.tree.item(self.treerow)['values'][int(str(self.treecol[1:]))-1])
            self.entry['exportselection'] = False

            self.entry.focus_force()
            self.entry.bind("<Return>", self.OnReturn)
            self.entry.bind("<Escape>", lambda *ignore: self.entry.destroy())

            self.entry.place(x=x,
                             y=y + pady,
                             anchor=tk.W, width=width)

    def OnReturn(self, event):
        """ Updates the stored data with the values in the entry. """
        val = self.tree.item(self.treerow)['values']
        val = [float(i) for i in val]
        val[int(self.treecol[1:])-1] = float(self.entry.get())
        self.tree.item(self.treerow, values=val)
        self.entry.destroy()
        self.saved = False

        self.out_data.loc[self.treerow] = val

        self.OnClick(0)
        self.saved = False
        
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
                self.out_data, columns=self.opt_var).to_string()
            self.save_path.seek(0)  # Move to the first row to overwrite it
            self.save_path.write(filedata)
            self.save_path.flush()  # Save without closing
            # typically the above line would do. however this is used to ensure that the file is written
            os.fsync(self.save_path.fileno())
            self.saved = True