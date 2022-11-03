
from typing import List
from vai_lab._plugin_templates import UI

import tkinter as tk
from tkinter import messagebox, ttk
from tkinter.filedialog import asksaveasfile, askopenfile, askopenfilename

import os
import numpy as np
import pandas as pd
import math

_PLUGIN_READABLE_NAMES = {"canvas": "default",
                          "state-action": "alias", "robot": "alias"}    # type:ignore
_PLUGIN_MODULE_OPTIONS = {"layer_priority": 2,
                          "required_children": None}                    # type:ignore
_PLUGIN_REQUIRED_SETTINGS = {}                                          # type:ignore
_PLUGIN_OPTIONAL_SETTINGS = {}                                          # type:ignore
_PLUGIN_REQUIRED_DATA = {"X"}                                           # type:ignore


class CanvasInput(tk.Frame, UI):
    """Method of user interaction for state-action pairs"""

    def __init__(self, parent, controller, config: dict):
        self.parent = parent
        super().__init__(self.parent, bg=self.parent['bg'])
        self.controller = controller

        self.controller.title('Canvas Input')
        self.notebook = ttk.Notebook(self)
        self.notebook.grid(row=0, column=0, columnspan=7,
                           rowspan=12, pady=15)
        self.frame: List[tk.Frame] = []
        self.tree: List[ttk.Treeview] = []
        self.canvas: List[tk.Canvas] = []
        self.draw: List[tk.StringVar] = []
        self.state: List[tk.StringVar] = []
        self.type: List[str] = []
        self.clock: List[tk.StringVar] = []
        self.save_path = ''
        self.saved = True

    def set_data_in(self, data_in):
        req_check = [
            r for r in _PLUGIN_REQUIRED_DATA if r not in data_in.keys()]
        if len(req_check) > 0:
            raise Exception("Minimal Data Requirements not met"
                            + "\n\t{0} ".format("CanvasInput")
                            + "requires data: {0}".format(_PLUGIN_REQUIRED_DATA)
                            + "\n\tThe following data is missing:"
                            + "\n\t\u2022 {}".format(",\n\t\u2022 ".join([*req_check])))
        self._data_in = data_in
        self._load_classes_from_data()

    # Causes static type error as it overloads the method in the parent class
    def configure(self, config: dict):          # type:ignore
        self._config = config

    def class_list(self):
        """Getter for required _class_list variable

        :return: list of class labels
        :rtype: list of strings
        """
        return self._class_list

    def _load_classes_from_data(self):
        """Setter for required _class_list variable

        :param value: labels for state-action pair headers
        :type value: list of strings
        """

        self._class_list = list(self._data_in["X"].columns)
        self._class_list = np.squeeze(self._class_list)
        islist = []
        for ii in np.arange(len(self._class_list)):
            islist.append(isinstance(self._class_list[ii], list))
        if not all(islist):
            self._class_list = [list(self._class_list)]

        self.out_data = {}
        self.out_data[0] = {}
        for ii in np.arange(len(self._class_list)):
            self.out_data[ii] = {}
            for k in np.arange(len(self._class_list[ii])):
                self._class_list[ii][k] = self._class_list[ii][k].replace(
                    ' ', '_').lower()
                self.out_data[ii][self._class_list[ii][k]] = []

        for ii in np.arange(len(self.out_data)):
            self.frame.append(tk.Frame(self, bg=self.parent['bg']))
            self.frame[-1].grid(row=0, column=0, sticky="nsew", pady=15)
            # if self._class_list[ii][0].split('_')[1] == 'a':
            if self._class_list[ii][0].split('_')[1] == 'a':
                self.type.append('Rotating')
                self.clock.append(tk.StringVar())
                self.clock[ii].set('clock')
            else:
                self.type.append('Sliding')
                self.clock.append(-1)
            self.notebook.add(
                self.frame[-1],
                text='Object ' + str(ii) + ' - ' + self.type[-1])

            # Create a canvas widget
            self.width, self.height = 600, 600
            self.canvas.append(tk.Canvas(
                self.frame[-1], width=self.width,
                height=self.height, background="white"))
            self.canvas[-1].grid(row=0, column=0, columnspan=4, rowspan=2)
            self.canvas[-1].bind('<Button-1>', self.draw_dot)
            self.canvas[-1].bind("<B1-Motion>", self.on_drag)
            # self.canvas[-1].bind('<Motion>', self.motion)

            # Booleans to identify what the user wants to do
            self.draw.append(tk.StringVar())
            self.draw[ii].set('draw')
            self.state.append(tk.StringVar())
            self.state[ii].set('state')
            # Buttons under the canvas
            self.button_draw = tk.Radiobutton(
                self.frame[-1], text='Draw', fg='white', bg=self.parent['bg'],
                height=3, width=20, var=self.draw[ii],
                selectcolor='black', value='draw').grid(column=4, row=3)
            self.button_drag = tk.Radiobutton(
                self.frame[-1], text='Move', fg='white', bg=self.parent['bg'],
                height=3, width=20, var=self.draw[ii],
                selectcolor='black', value='drag').grid(column=5, row=3)
            self.clock_arc = tk.Radiobutton(
                self.frame[-1], text='Clockwise', fg='white', bg=self.parent['bg'],
                height=3, width=20, var=self.clock[ii],
                selectcolor='black', value='clock').grid(column=6, row=3)
            self.countclock_arc = tk.Radiobutton(
                self.frame[-1], text='Counterclockwise', fg='white', bg=self.parent['bg'],
                height=3, width=20, var=self.clock[ii],
                selectcolor='black', value='countclock').grid(column=7, row=3)
            # self.button_edit = tk.Radiobutton(
            #     self.frame[-1], text = 'Edit', fg = 'white', bg = self.parent['bg'],
            #     height = 3, width = 20, var = self.draw[ii],
            #     selectcolor = 'black', value = 'edit').grid(column = 6,row = 3)
            self.button_save = tk.Button(
                self.frame[-1], text='Save', fg='white', bg=self.parent['bg'],
                height=3, width=20,
                command=self.save_file).grid(column=1, row=3)
            self.button_upload = tk.Button(
                self.frame[-1], text='Upload coordinates', fg='white',
                bg=self.parent['bg'], height=3, width=20,
                command=self.upload_sa).grid(column=0, row=3)
            self.button_reset = tk.Button(
                self.frame[-1], text='Reset', fg='white',
                bg=self.parent['bg'], height=3, width=20,
                command=self.reset).grid(column=2, row=3)
            button_main = tk.Button(
                self.frame[-1], text="Done", fg='white',
                bg=self.parent['bg'], height=3, width=20,
                command=self.check_quit).grid(column=3, row=3)
            style = ttk.Style()
            style.configure(
                "Treeview", background='white', foreground='white',
                rowheight=25, fieldbackground='white',
                font=self.controller.pages_font)
            style.configure("Treeview.Heading",
                            font=self.controller.pages_font)
            style.map('Treeview', background=[('selected', 'grey')])

            tree_frame = tk.Frame(self.frame[-1])
            tree_frame.grid(row=0, column=4, columnspan=3, rowspan=10)

            tree_scrollx = tk.Scrollbar(tree_frame, orient='horizontal')
            tree_scrollx.pack(side=tk.BOTTOM, fill=tk.X)
            tree_scrolly = tk.Scrollbar(tree_frame)
            tree_scrolly.pack(side=tk.RIGHT, fill=tk.Y)

            self.tree.append(ttk.Treeview(
                tree_frame,
                yscrollcommand=tree_scrolly.set,
                xscrollcommand=tree_scrollx.set))
            self.tree[-1].pack()

            tree_scrollx.config(command=self.tree[-1].xview)
            tree_scrolly.config(command=self.tree[-1].yview)

            if self.type[-1] == 'Rotating':
                self.x_ini, self.y_ini = int(self.width/2), int(self.height/2)
                self.r = int(np.min([self.x_ini, self.y_ini])/1.5)
                self.create_circle(self.x_ini, self.y_ini, 4,
                                   fill="#DDD", outline="", width=4)
                self.create_circle(self.x_ini, self.y_ini, self.r,
                                   fill="", outline="#DDD", width=4)

            self.tree[-1]['columns'] = self._class_list[ii]

            # Format columns
            self.tree[-1].column("#0", width=50)
            for n, cl in enumerate(self._class_list[ii]):
                self.tree[-1].column(
                    cl, width=int(
                        self.controller.pages_font.measure(str(cl)))+20,
                    minwidth=50, anchor=tk.CENTER)

            # Headings
            self.tree[-1].heading("#0", text="Sample", anchor=tk.CENTER)
            for cl in self._class_list[ii]:
                self.tree[-1].heading(cl, text=cl, anchor=tk.CENTER)

            # for nn in np.arange(N):
            #     self.tree[-1].insert(
            #                 parent = '', index = 'end', iid = (nn+1)*1000, text = 'Trial '+str(nn),
            #                 values = tuple())

            self.tree[-1].tag_configure('odd', foreground='black',
                                        background='#E8E8E8')
            self.tree[-1].tag_configure('even', foreground='black',
                                        background='#DFDFDF')

            # Define double-click on row action
            self.tree[-1].bind("<Double-1>", self.OnDoubleClick)

    def draw_dot(self, event):

        ii = self.notebook.index(self.notebook.select())
        if self.draw[ii].get() == 'drag':
            self.selected = self.canvas[ii].find_overlapping(
                event.x-10, event.y-10, event.x+10, event.y+10)
            if self.selected:
                if len(self.selected) >= 2:
                    self.canvas[ii].selected = self.selected[-2]
                else:
                    self.canvas[ii].selected = self.selected[-1]
                self.canvas[ii].startxy = (event.x, event.y)
            else:
                self.canvas[ii].selected = None

        if self.draw[ii].get() == 'draw':
            # Draw an oval in the given coordinates
            self.saved = False
            # Angle of the selected point with respect to the circle center
            if self.type[ii] == 'Rotating':
                alpha, x_o, y_o = self.angle_calc(event.x, event.y,
                                                  circxy=True)
                if self.state[ii].get() == 'state':  # Write state coordinates
                    self.canvas[ii].create_oval(
                        x_o-3, y_o-3, x_o+3, y_o+3, fill="black", width=0,
                        tags=("state"+str(ii)+'-'
                              + str(len(self.out_data[ii]['state_a']))))
                    self.out_data[ii]['state_a'].append((
                        -np.rad2deg(alpha)+360) % 360)
                    self.state[ii].set('action')
                    # Update coordinates in corresponding row if exists.
                    if self.tree[ii].selection():
                        n = int(self.tree[ii].selection()[0]) + 1
                        if n % 2 == 0:
                            tag = ('even',)
                        else:
                            tag = ('odd',)
                        self.tree[ii].insert(
                            parent='', index='end', iid=n, text=n+1,
                            values=tuple(self.dict2mat(
                                self.out_data[ii])[n, :].astype(int)),
                            tags=tag)
                        self.tree[ii].selection_set(str(n))
                    else:
                        self.tree[ii].insert(
                            parent='', index='end', iid=0, text=1,
                            values=tuple(self.dict2mat(
                                self.out_data[ii])[0, :].astype(int)),
                            tags=('even',))
                        self.tree[ii].selection_set(str(0))

                elif self.state[ii].get() == 'action':
                    if self.clock[ii].get() == 'clock':
                        start = self.out_data[ii]['state_a'][-1]
                        end = np.rad2deg(-alpha)
                    else:
                        start = self.out_data[ii]['state_a'][-1] - 360
                        end = 360 - np.rad2deg(alpha)
                    self.create_circle_arc(
                        self.x_ini, self.y_ini, self.r, fill="",
                        outline="red", start=start, end=end, width=2,
                        style=tk.ARC, tags=("action"+str(ii)+'-' + str(len(
                            self.out_data[ii]['action_a']))))
                    self.out_data[ii]['action_a'].append((
                        -np.rad2deg(alpha)+360) % 360)
                    self.state[ii].set('state')
                    n = int(self.tree[ii].selection()[0])
                    self.tree[ii].item(
                        self.tree[ii].get_children()[n], text=n+1,
                        values=tuple(self.dict2mat(
                            self.out_data[ii])[n, :].astype(int)))
            else:
                if self.state[ii].get() == 'state':  # Write state coordinates
                    self.canvas[ii].create_oval(
                        event.x-3, event.y-3, event.x+3, event.y+3,
                        fill="black", width=0,
                        tags=("state"+str(ii)+'-' + str(len(
                            self.out_data[ii]['state_x']))))
                    self.out_data[ii]['state_x'].append(event.x)
                    self.out_data[ii]['state_y'].append(event.y)
                    self.state[ii].set('action')
                    # Update coordinates in corresponding row if exists.
                    if self.tree[ii].selection():
                        n = int(self.tree[ii].selection()[0]) + 1
                        if n % 2 == 0:
                            tag = ('even',)
                        else:
                            tag = ('odd',)
                        self.tree[ii].insert(
                            parent='', index='end', iid=n, text=n+1,
                            values=tuple(self.dict2mat(
                                self.out_data[ii])[n, :].astype(int)),
                            tags=tag)
                        self.tree[ii].selection_set(str(n))
                    else:
                        self.tree[ii].insert(
                            parent='', index='end', iid=0, text=1,
                            values=tuple(self.dict2mat(
                                self.out_data[ii])[0, :].astype(int)),
                            tags=('even',))
                        self.tree[ii].selection_set(str(0))

                elif self.state[ii].get() == 'action':
                    self.canvas[ii].create_line(
                        self.out_data[ii]['state_x'][-1],
                        self.out_data[ii]['state_y'][-1], event.x, event.y,
                        fill="red", arrow=tk.LAST,
                        tags=("action"+str(ii)+'-' + str(len(
                            self.out_data[ii]['action_x']))))
                    self.out_data[ii]['action_x'].append(event.x)
                    self.out_data[ii]['action_y'].append(event.y)
                    self.state[ii].set('state')
                    n = int(self.tree[ii].selection()[0])
                    self.tree[ii].item(
                        self.tree[ii].get_children()[n], text=n+1,
                        values=tuple(self.dict2mat(
                            self.out_data[ii])[n, :].astype(int)))

    def on_drag(self, event):

        ii = self.notebook.index(self.notebook.select())
        if self.draw[ii].get() == 'drag' and self.canvas[ii].selected:
            # move the selected item
            n = int(self.canvas[ii].gettags("current")[0].split('-')[1])

            if self.type[ii] == 'Rotating':
                alpha, dx, dy = self.angle_calc(event.x, event.y, circxy=True)
                _, dx_pr, dy_pr = self.angle_calc(
                    self.canvas[ii].startxy[0], self.canvas[ii].startxy[1],
                    circxy=True)
                xa = self.r * np.cos(
                    np.deg2rad(self.out_data[ii]['action_a'][n])) + self.x_ini
                ya = self.r * np.sin(
                    np.deg2rad(self.out_data[ii]['action_a'][n])) + self.y_ini
                if self.canvas[ii].gettags(
                        "current")[0].split('-')[0] == 'state'+str(ii):  # If state, updates both the state placement and the arrow
                    self.canvas[ii].move(
                        self.canvas[ii].selected, dx-dx_pr,
                        dy-dy_pr)
                    self.out_data[ii]['state_a'][n] = (
                        360-np.rad2deg(alpha)) % 360

                    if self.clock[ii].get() == 'clock':
                        start = self.out_data[ii]['action_a'][n]
                        end = np.rad2deg(-alpha)
                    else:
                        start = self.out_data[ii]['action_a'][n] - 360
                        end = 360 - np.rad2deg(alpha)

                    self.canvas[ii].itemconfigure(
                        "action"+str(ii)+'-'+str(n), start=start,
                        extent=end - start)

                elif self.canvas[ii].gettags(
                        "current")[0].split('-')[0] == 'action'+str(ii):  # If action, updates the arrow end of the line position

                    self.out_data[ii]['action_a'][n] = (
                        360-np.rad2deg(alpha)) % 360

                    if self.clock[ii].get() == 'clock':
                        start = self.out_data[ii]['state_a'][n]
                        end = np.rad2deg(-alpha)
                    else:
                        start = self.out_data[ii]['state_a'][n] - 360
                        end = 360 - np.rad2deg(alpha)

                    self.canvas[ii].itemconfigure(
                        "action"+str(ii)+'-'+str(n), start=start,
                        extent=end - start)

            else:
                # calculate distance moved from last position
                dx = event.x - self.canvas[ii].startxy[0]
                dy = event.y - self.canvas[ii].startxy[1]
                if self.canvas[ii].gettags(
                        "current")[0].split('-')[0] == 'state'+str(ii):  # If state, updates both the state placement and the arrow
                    self.canvas[ii].move(self.canvas[ii].selected, dx, dy)
                    self.canvas[ii].coords(
                        "action"+str(ii)+'-'+str(n),
                        (event.x, event.y, self.out_data[ii]['action_x'][n],
                         self.out_data[ii]['action_y'][n]))
                    self.out_data[ii]['state_x'][n] = event.x
                    self.out_data[ii]['state_y'][n] = event.y
                elif self.canvas[ii].gettags(
                        "current")[0].split('-')[0] == 'action'+str(ii):  # If action, updates the arrow end of the line position
                    self.canvas[ii].coords(
                        self.canvas[ii].gettags("current")[0],
                        (self.out_data[ii]['state_x'][n],
                         self.out_data[ii]['state_y'][n], event.x, event.y))
                    self.out_data[ii]['action_x'][n] = event.x
                    self.out_data[ii]['action_y'][n] = event.y
            # update last position
            self.canvas[ii].startxy = (event.x, event.y)
            self.tree[ii].item(self.tree[ii].get_children()[n], text=n+1,
                               values=tuple(self.dict2mat(
                                   self.out_data[ii])[n, :].astype(int)))
            self.tree[ii].selection_set(str(n))

    def checkered(self, line_distance):

        ii = self.notebook.index(self.notebook.select())
        # vertical lines at an interval of "line_distance" pixel
        for x in range(line_distance, self.width, line_distance):
            self.canvas[ii].create_line(x, 0, x, self.height, fill="#476042")
        # horizontal lines at an interval of "line_distance" pixel
        for y in range(line_distance, self.height, line_distance):
            self.canvas[ii].create_line(0, y, self.width, y, fill="#476042")

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
            self.save_path = asksaveasfile(defaultextension='.txt', filetypes=[('Text file', '.txt'),
                                                                               ('CSV file',
                                                                                '.csv'),
                                                                               ('All Files', '*.*')])
        # asksaveasfile return `None` if dialog closed with "cancel".
        if self.save_path is not None:
            # Transform input for output file
            data = {}
            samples = np.max([len(self.out_data[element][
                list(self.out_data[element].keys())[0]])
                for element in self.out_data])
            for ii in self.out_data.keys():
                for c in self.out_data.keys():
                    a, b = c.split('_')
                    aux = self.out_data[c]
                    aux.extend([-1]*(samples - len(self.out_data[c])))
                    data[a+str(ii)+'_'+b] = aux

            filedata = pd.DataFrame(data, columns=data.keys()).to_string()
            self.save_path.seek(0)  # Move to the first row to overwrite it
            self.save_path.write(filedata)
            self.save_path.flush()  # Save without closing
            # typically the above line would do. however this is used to ensure that the file is written
            os.fsync(self.save_path.fileno())
            self.saved = True

    def on_return(self, event):
        ii = self.notebook.index(self.notebook.select())
        val = self.tree[ii].item(self.treerow)['values']
        val = [float(i) for i in val]
        val[int(self.treecol[1:])-1] = float(self.entry.get())
        self.tree[ii].item(self.treerow, values=val)
        self.entry.destroy()
        self.saved = False

        if self.type[ii] == 'Rotating':
            dx, dy = self.coord_calc(np.deg2rad(360 - val[0]))
            dx_pr, dy_pr = self.coord_calc(np.deg2rad(
                360 - self.out_data[ii]['state_a'][self.treerow]))
            self.out_data[ii]['state_a'][self.treerow] = float(val[0])
            self.canvas[ii].move("state"+str(ii)+'-'+str(self.treerow), dx-dx_pr,
                                 dy-dy_pr)

            self.out_data[ii]['action_a'][self.treerow] = float(val[1])
            if self.clock[ii].get() == 'clock':
                start = self.out_data[ii]['state_a'][self.treerow]
                end = self.out_data[ii]['action_a'][self.treerow]
            else:
                start = self.out_data[ii]['state_a'][self.treerow] - 360
                end = self.out_data[ii]['action_a'][self.treerow]

            self.canvas[ii].itemconfigure(
                "action"+str(ii)+'-'+str(self.treerow), start=start,
                extent=end - start)
        else:
            # calculate distance moved from last position
            dx_s = val[0] - self.out_data[ii]['state_x'][self.treerow]
            dy_s = val[1] - self.out_data[ii]['state_y'][self.treerow]

            self.canvas[ii].move("state"+str(ii)+'-' +
                                 str(self.treerow), dx_s, dy_s)

            self.out_data[ii]['state_x'][self.treerow] = val[0]
            self.out_data[ii]['state_y'][self.treerow] = val[1]

            self.canvas[ii].coords(
                "action"+str(ii)+'-'+str(self.treerow),
                (self.out_data[ii]['state_x'][self.treerow],
                 self.out_data[ii]['state_y'][self.treerow], val[2], val[3]))
            self.out_data[ii]['action_x'][self.treerow] = val[2]
            self.out_data[ii]['action_y'][self.treerow] = val[3]

    def OnDoubleClick(self, event):
        """ Executed when a row is double clicked.
        Opens an entry box to edit a cell and updates the canvas and the 
        stored data. """

        ii = self.notebook.index(self.notebook.select())
        self.treerow = int(self.tree[ii].identify_row(event.y))
        self.treecol = self.tree[ii].identify_column(event.x)

        # get column position info
        x, y, width, height = self.tree[ii].bbox(self.treerow, self.treecol)

        # y-axis offset
        pady = height // 2
        # pady = 0

        if hasattr(self, 'entry'):
            self.entry.destroy()

        self.entry = tk.Entry(self.tree[ii], justify='center')

        if int(self.treecol[1:]) > 0:
            self.entry.insert(
                0, self.tree[ii].item(self.treerow)['values'][int(str(self.treecol[1:]))-1])
            # self.entry['selectbackground'] = '#123456'
            self.entry['exportselection'] = False

            self.entry.focus_force()
            self.entry.bind("<Return>", self.on_return)
            self.entry.bind("<Escape>", lambda *ignore: self.entry.destroy())

            self.entry.place(x=x,
                             y=y + pady,
                             anchor=tk.W, width=width)

    def upload_sa(self):

        ii = self.notebook.index(self.notebook.select())
        filename = askopenfilename(initialdir=os.getcwd(),
                                   title='Select a file',
                                   defaultextension='.txt',
                                   filetypes=[('Text file', '.txt'),
                                              ('CSS file', '.css'),
                                              ('All Files', '*.*')])
        if filename is not None:
            data = open(filename, 'r')
            read = False
            self.draw[ii].set('drag')
            for n, point in enumerate(data):
                if read:  # Not elegant at all, just to omit the header.
                    i, sx, sy, ax, ay = point.split()
                    # Draw an oval in the given coordinates
                    self.canvas[ii].create_oval(
                        float(sx)-3, float(sy)-3, float(sx)+3, float(sy)+3,
                        fill="black", width=0,
                        tags=("state-" + str(len(
                            self.out_data[ii]['state_x']))))
                    self.canvas[ii].create_line(
                        float(sx), float(sy), float(ax), float(ay),
                        fill="red", arrow=tk.LAST,
                        tags=("action"+str(ii)+"-" + str(len(
                            self.out_data[ii]['action_x']))))
                    self.out_data[ii]['state_x'].append(sx)
                    self.out_data[ii]['state_y'].append(sy)
                    self.out_data[ii]['action_x'].append(ax)
                    self.out_data[ii]['action_y'].append(ay)
                    self.tree.insert(
                        parent='', index='end',
                        iid=len(self.out_data[ii]['action_x'])-1,
                        text=len(self.out_data[ii]['action_x']),
                        values=tuple(self.dict2mat(
                            self.out_data[ii])
                            [len(self.out_data[ii]
                                 ['action_x'])-1, :].astype(int)))
                    self.tree.selection_set(str(len(
                        self.out_data[ii]['action_x'])-1))
                else:
                    read = True

    def reset(self):

        ii = self.notebook.index(self.notebook.select())
        msg = messagebox.askyesnocancel(
            'Info', 'Are you sure you want to reset the canvas?')
        if msg:
            self.canvas[ii].delete(tk.ALL)  # Reset canvas
            self.state[ii].set('state')
            self.out_data = {}
            for key in self._class_list[ii]:
                self.out_data[key] = []

            for record in self.tree[ii].get_children():  # Reset treeview
                self.tree[ii].delete(record)
            if self.type[ii] == 'Rotating':
                self.create_circle(self.x_ini, self.y_ini, 4,
                                   fill="#DDD", outline="", width=4)
                self.create_circle(self.x_ini, self.y_ini, self.r,
                                   fill="", outline="#DDD", width=4)

    def dict2mat(self, X):

        max_size = 0
        for key in X:
            if len(X[key]) > max_size:
                max_size = len(X[key])

        result = -np.ones((max_size, len(X)))
        for k, key in enumerate(X):
            result[:len(X[key]), k] = X[key]

        return result

    def angle_calc(self, x, y, circxy=False):
        if (x == self.x_ini) & (y < self.y_ini):
            alpha = math.pi/2
        elif (x == self.x_ini) & (y > self.y_ini):
            alpha = 3*math.pi/2
        else:
            alpha = np.arctan((y-self.y_ini)/(x-self.x_ini))
            alpha += ((x-self.x_ini) < 0) * math.pi
            alpha += (alpha < 0) * 2*math.pi
        if circxy:
            cx, cy = self.coord_calc(alpha)
            return alpha, cx, cy
        else:
            return alpha

    def coord_calc(self, alpha):
        cx = self.r * np.cos(alpha) + self.x_ini
        cy = self.r * np.sin(alpha) + self.y_ini
        return cx, cy

    def create_circle(self, x, y, r, **kwargs):

        return self.canvas[self.notebook.index(
            self.notebook.select())].create_oval(x-r, y-r, x+r, y+r, **kwargs)

    def create_circle_arc(self, x, y, r, **kwargs):

        if "start" in kwargs and "end" in kwargs:
            kwargs["extent"] = kwargs["end"] - kwargs["start"]
            # if self.clock == 'countclock':
            #     kwargs["extent"] += (kwargs["extent"] < 0) * 360
            del kwargs["end"]
        return self.canvas[self.notebook.index(
            self.notebook.select())].create_arc(x-r, y-r, x+r, y+r, **kwargs)
