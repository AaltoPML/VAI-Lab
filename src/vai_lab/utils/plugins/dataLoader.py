import tkinter as tk
import os
from PIL import ImageTk
from tkinter import ttk
import numpy as np
from vai_lab._import_helper import get_lib_parent_dir
# from ttkwidgets import CheckboxTreeview
# from sys import platform

class dataLoader():
    """ Creates a window 
    """
    def __init__(self,controller,data):
        
        self.controller = controller
        self.newWindow = tk.Toplevel(self.controller)
        
        # Window options
        self.newWindow.title('Data Importer')
        self.newWindow.tk.call('wm','iconphoto', self.newWindow._w, ImageTk.PhotoImage(
            file = os.path.join(os.path.join(
                get_lib_parent_dir(), 
                'utils', 
                'resources', 
                'Assets', 
                'VAILabsIcon.ico'))))
        
        self.newWindow.geometry("700x400")
        self.newWindow.grid_rowconfigure(2, weight=1)
        self.newWindow.grid_columnconfigure(tuple(range(2)), weight=1)
        
        frame1 = tk.Frame(self.newWindow)
        # frame2 = tk.Frame(self.newWindow)
        tree_frame1 = tk.Frame(self.newWindow, height=300,width=300)
        tree_frame2 = tk.Frame(self.newWindow, height=300,width=300)
        frame3 = tk.Frame(self.newWindow)
        frame4 = tk.Frame(self.newWindow)
        
        sizegrip=ttk.Sizegrip(frame4)     # put a sizegrip widget on the southeast corner of the window
        sizegrip.pack(side = tk.RIGHT, anchor = tk.SE)

        tk.Label(frame1,
              text ="Select variables to import", 
              justify=tk.LEFT).pack()
        # tk.Label(frame2,
        #       text ="Variables in "+filename, 
        #       justify=tk.LEFT).pack()
        
        #Treeview 1
        style = ttk.Style()
        style.configure(
            "Treeview",
            background = 'white', 
            foreground = 'black', 
            rowheight = 25, 
            fieldbackground = 'white', 
            # font = self.controller.pages_font)
            )
        # style.configure("Treeview.Heading", 
        #                 # font = self.controller.pages_font)
        #                 )
        style.map('Treeview', 
                  background = [('selected', 'grey')])
        style.layout('cb.Treeview.Row',
                     [('Treeitem.row', {'sticky': 'nswe'}),
                      ('Treeitem.image', {'side': 'right', 'sticky': 'e'})])
        
        self.tree = []
        columns = ['Name', 'Size', 'Class']
        self.add_treeview(tree_frame1, data, columns)
        self.add_treeview(tree_frame2, None, [])
        tk.Button(
            frame3, text = 'Finish', fg = 'black', 
            height = 2, width = 10, #font = self.controller.pages_font, 
            command = lambda: self.check_quit()).pack(side = tk.RIGHT, anchor = tk.W)

        tree_frame1.grid(column=0, row=2, sticky="nsew")
        tree_frame2.grid(column=1, row=2, sticky="nsew")
        frame1.grid(column=0, row=0, columnspan=2, sticky="nw")
        # frame2.grid(column=0, row=1, columnspan=2, sticky="nw")
        frame3.grid(column=0, row=3, columnspan=2, sticky="n")
        frame4.grid(column=0, row=4, columnspan=2, sticky="se")

    def add_treeview(self,frame,data,columns):
        """ Add a treeview"""

        tree_scrollx = tk.Scrollbar(frame, orient = 'horizontal')
        tree_scrollx.pack(side = tk.BOTTOM, fill = tk.BOTH)
        tree_scrolly = tk.Scrollbar(frame)
        tree_scrolly.pack(side = tk.RIGHT, fill = tk.BOTH)
        if data is not None:
            self.tree.append(ttk.Treeview(
                frame, 
                yscrollcommand = tree_scrolly.set, 
                xscrollcommand = tree_scrollx.set,
                show=("headings", "tree")))
        else:
            self.tree.append(ttk.Treeview(
                frame, 
                yscrollcommand = tree_scrolly.set, 
                xscrollcommand = tree_scrollx.set))

        tree_scrollx.config(command = self.tree[-1].xview)
        tree_scrolly.config(command = self.tree[-1].yview)
        # self.tree[-1].pack_propagate(0)
        
        self.tree[-1].pack(expand = True, side = tk.LEFT, fill = tk.BOTH)
        self.fill_treeview(self.tree[-1], data, columns)

    def fill_treeview(self,tree,data,columns):
        if data is not None:
            tree['columns'] = columns

            # Format columns
            tree.column("#0", width = 0, stretch=tk.NO)
            for cl in tree['columns']:
                tree.column(
                    cl, width = int(
                        self.controller.pages_font.measure(str(cl)))+30, 
                    minwidth = 50, anchor = tk.CENTER, stretch=tk.NO)

            # Headings
            tree.heading("#0")
            for cl in tree['columns']:
                tree.heading(cl, text = cl, anchor = tk.CENTER)
            
            variables = [key for key in data.keys() if (key[:1] != '__') and (key[-2:] != '__')]
            for n, var in enumerate(variables):
                if n%2 == 0:
                    tree.insert(parent = '', index = 'end', iid = n, text = '', 
                                     values = (var, data[var].values.shape, data[var].values.dtype), tags = ('even',))
                else:
                    tree.insert(parent = '', index = 'end', iid = n, text = '', 
                                     values = (var, data[var].shape, data[var].values.dtype), tags = ('odd',))

            # Define double-click on row action
            if len(self.tree) == 1:
                tree.bind("<Button-1>", lambda event, d = data: self.OnClick(event, d))
        else:
            tree.heading("#0", text = 'No variable selected for preview.', anchor = tk.CENTER)

    def check_quit(self):
        """ Saves the information and closes the window """
        self.newWindow.destroy()

    def OnClick(self,event,d):
        """ On data variable click, updates variable display. """
        if self.tree[0].identify_column(event.x) == '#1':
            treerow = self.tree[0].identify_row(event.y)
            if len(self.tree[0].item(treerow,"values")) > 1:
                data = d[self.tree[0].item(treerow,"values")[0]]
                # Reset treeview
                self.resetTree(self.tree[1])
                # refill second treeview
                self.tree[1]['columns'] = list(d[self.tree[0].item(treerow,"values")[0]].columns)
                # Format columns
                self.tree[1].column("#0", width = self.controller.pages_font.measure('0'*3)+20, 
                        minwidth = 0, stretch=tk.NO)
                for n, cl in enumerate(self.tree[1]['columns']):
                    self.tree[1].column(
                        cl, width = int(
                            self.controller.pages_font.measure(str(cl)*5))+20, 
                            anchor = tk.CENTER, 
                            stretch=tk.NO)
                # Headings
                self.tree[1].heading("#0", text = '', anchor = tk.CENTER)
                for cl in self.tree[1]['columns']:
                    self.tree[1].heading(cl, text = cl, anchor = tk.CENTER)
                # Data filling
                for n,row in enumerate(data.values):
                    if n%2 == 0:
                        self.tree[1].insert(parent = '', index = 'end', iid = n, text = n, 
                                         values = tuple(np.around(row, 3)), tags = ('even',))
                    else:
                        self.tree[1].insert(parent = '', index = 'end', iid = n, text = n, 
                                         values = tuple(np.around(row, 3)), tags = ('odd',))
                self.tree[1].event_generate("<<ThemeChanged>>")
            else:
                self.resetTree(self.tree[1])
                self.tree[1].column("#0", width = self.controller.pages_font.measure('No variable selected for preview.')+20, 
                        minwidth = 0, stretch=tk.NO)
                self.tree[1].heading("#0", text = 'No variable selected for preview.', anchor = tk.CENTER)

    def resetTree(self,tree):
        tree.delete(*tree.get_children())
        tree["columns"] = ()