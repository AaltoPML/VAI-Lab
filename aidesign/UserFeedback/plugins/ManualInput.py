from . import UI
import tkinter as tk
import os
from PIL import Image, ImageTk
from tkinter import messagebox, ttk
from tkinter.filedialog import asksaveasfile, askopenfile, askopenfilename
import numpy as np
import pandas as pd

_PLUGIN_CLASS_NAME = "ManualInput"
_PLUGIN_CLASS_DESCRIPTION = "Method of user feedback for binary or classification data"
_PLUGIN_READABLE_NAMES = {"manual":"default","binary":"alias","classification":"alias"}
_PLUGIN_MODULE_OPTIONS = {"layer_priority": 2,
                            "required_children": None,}
_PLUGIN_REQUIRED_SETTINGS = {"class_list":"list"}
_PLUGIN_OPTIONAL_SETTINGS = {"image_dir":"str"}
class ManualInput(tk.Frame,UI):
    def __init__(self, parent, controller, config:dict):
        self.parent = parent    
        super().__init__(parent, bg = self.parent['bg'])
        self.controller = controller
        self.controller.title('Manual Input')
        
        
        self.dirpath = os.path.dirname(os.path.realpath(__file__))
        self.assets_path = os.path.join(self.dirpath,'resources','Assets')

        self._class_list = None        
        pixels = 500
        path = os.path.join(self.dirpath,'resources','example_radiography_images')
        self.N = len(os.listdir(path))
        
        self.image_list = []
        for f in os.listdir(path):
            self.image_list.append(
                ImageTk.PhotoImage(self.expand2square(
                    Image.open(os.path.join(path, f)), 
                    (0, 0, 0)).resize((pixels, pixels)))) # (0, 0, 0) is the padding colour
        
        # Frames
        frame1 = tk.Frame(self, bg = self.parent['bg'])
        frame4 = tk.Frame(self, bg = self.parent['bg'])
        frame5 = tk.Frame(self, bg = self.parent['bg'])
        frame6 = tk.Frame(self, bg = self.parent['bg'])
        
        # Status bar in the lower part of the window
        self.status = tk.Label(frame6, text='Image 1 of '+str(self.N), bd = 1, 
                          relief = tk.SUNKEN, anchor = tk.E, fg = 'white', 
                          bg = self.parent['bg'])
        self.status.pack(fill = tk.BOTH, expand = True, padx=10, pady=(0,10))
        
        # Inital image
        self.my_label = ResizableImgLabel(frame1, image = self.image_list[0], 
                                 bg = self.parent['bg'])
        self.my_label.pack(fill = tk.BOTH, expand = True, padx=(10,0), pady=(10,0))
        
        # Buttons initialisation
        self.back_img = ImageTk.PhotoImage(Image.open(
            os.path.join(self.assets_path,'back_arrow.png')).resize((150, 50)))
        self.forw_img = ImageTk.PhotoImage(Image.open(
            os.path.join(self.assets_path,'forw_arrow.png')).resize((150, 50)))
        self.button_back = tk.Button(
            frame4, image = self.back_img, bg = self.parent['bg'], 
            state = tk.DISABLED)
        self.button_back.grid(column = 0,row = 19, padx=(10,0), pady=10, sticky="news")
        self.button_save = tk.Button(
            frame4, text = 'Save', fg = 'white', bg = self.parent['bg'], height = 3, 
            width = 20, command = self.save_file)
        self.button_save.grid(column = 1,row = 19, sticky="news", pady=10)
        self.button_forw = tk.Button(
            frame4, image = self.forw_img, bg = self.parent['bg'], 
            command = lambda: self.forward_back(2))
        self.button_forw.grid(column = 2,row = 19, sticky="news", pady=10)

        button_main = tk.Button(
            frame5, text="Done", 
            fg = 'white', bg = self.parent['bg'], height = 3, width = 20, 
            command = self.check_quit).grid(column = 4,row = 19, sticky="news", pady=10)
        self._parse_config(config)
        self.save_path = ''
        self.saved = True
        
        frame1.grid(row = 0, column = 0, sticky="nsew")
        # self.frame3.grid(row = 0, column = 2, sticky="nsew", pady=10, padx=10)
        frame4.grid(row = 1, column = 0, sticky="sew")
        frame5.grid(row = 1, column = 1, sticky="sew")
        frame6.grid(row = 2, column = 0, columnspan =3, sticky="sew")

        frame4.grid_columnconfigure(tuple(range(3)), weight=1)
        self.grid_rowconfigure(0, weight=3)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(tuple(range(3)), weight=1)
        self.grid_columnconfigure(0, weight=2)
        
    def _parse_config(self, config):
        self.config = config
        self.class_list(self.config["plugin"]["options"]["class_list"])

    def class_list(self):
        """Getter for required _class_list variable
        
        :return: list of class labels
        :rtype: list of strings
        """
        return self._class_list

    def class_list(self,value):
        """Setter for required _class_list variable
        
        :param value: class labels for binary classification
        :type value: list of strings
        """
        if isinstance(value[0], list):
            self._class_list = value[0]
        else:
            self._class_list = value
        self.out_data = np.zeros((self.N, len(self._class_list)))
        
        frame2 = tk.Frame(self, bg = self.parent['bg'])
        frame2.grid(row = 0, column = 1, sticky="nsew")
        
        self.button_cl = {}
        self.var = {}
        for i,cl in enumerate(self._class_list):
            self.var[0,i] = tk.IntVar(value=self.out_data[0,i])
            self.button_cl[cl] = tk.Checkbutton(
                frame2, text = cl, fg = 'white', bg = self.parent['bg'], 
                selectcolor = 'black', height = 3, width = 20, 
                variable = self.var[0,i], 
                command=(lambda i=i: self.onPress(0,i)))
            self.button_cl[cl].grid(column = 4,row = i)
        
        #Tree defintion. Output display
        style = ttk.Style()
        style.configure(
            "Treeview", background = 'white', foreground = 'white', 
            rowheight = 25, fieldbackground = 'white', 
            font = self.controller.pages_font)
        style.configure("Treeview.Heading", font = self.controller.pages_font)
        style.map('Treeview', background = [('selected', 'grey')])
        
        tree_frame = tk.Frame(self)
        tree_frame.grid(row = 0, column = 2, sticky="nsew", pady=10, padx=10)
        
        tree_scrollx = tk.Scrollbar(tree_frame, orient = 'horizontal')
        tree_scrollx.pack(side = tk.BOTTOM, fill = tk.X)
        tree_scrolly = tk.Scrollbar(tree_frame)
        tree_scrolly.pack(side = tk.RIGHT, fill = tk.Y)
        
        self.tree = ttk.Treeview(tree_frame, 
                                 yscrollcommand = tree_scrolly.set, 
                                 xscrollcommand = tree_scrollx.set)
        self.tree.pack(fill='both', expand=True)
        
        tree_scrollx.config(command = self.tree.xview)
        tree_scrolly.config(command = self.tree.yview)
        
        self.tree['columns'] = self._class_list
        
        # Format columns
        self.tree.column("#0", width = 50)
        for n, cl in enumerate(self._class_list):
            self.tree.column(
                cl, width = int(self.controller.pages_font.measure(str(cl)))+20, 
                minwidth = 50, anchor = tk.CENTER)
        # Headings
        self.tree.heading("#0", text = "Image", anchor = tk.CENTER)
        for cl in self._class_list:
            self.tree.heading(cl, text = cl, anchor = tk.CENTER)
        self.tree.tag_configure('odd', foreground = 'black', 
                                background='#E8E8E8')
        self.tree.tag_configure('even', foreground = 'black', 
                                background='#DFDFDF')
        # Add data
        for n, sample in enumerate(self.out_data):
            if n%2 == 0:
                self.tree.insert(parent = '', index = 'end', iid = n, text = n+1, 
                                 values = tuple(sample.astype(int)), tags = ('even',))
            else:
                self.tree.insert(parent = '', index = 'end', iid = n, text = n+1, 
                                 values = tuple(sample.astype(int)), tags = ('odd',))
        
        # Select the current row
        self.tree.selection_set(str(int(0)))
        
        # Define double-click on row action
        self.tree.bind("<Double-1>", self.OnDoubleClick)

    def expand2square(self, pil_img, background_color):
        
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
    
    def open_file(self):
        
        self.save_path = askopenfile(mode='r+')
        if self.save_path is not None:
            t = self.save_path.read()
            # textentry.delete('0.0', 'end')
            # textentry.insert('0.0', t)
            # textentry.focus()
            
    def save_file_as(self):
        
        self.save_path = asksaveasfile(mode='w')
        self.save_file()
        
    def save_file(self):
        
        if self.save_path == '':
            self.save_path = asksaveasfile(defaultextension = '.txt', 
                                      filetypes = [('Text file', '.txt'), 
                                                   ('CSV file', '.csv'), 
                                                   ('All Files', '*.*')])
        if self.save_path is not None: # asksaveasfile return `None` if dialog closed with "cancel".
            filedata = pd.DataFrame(
                self.out_data, columns = self._class_list).to_string()
            self.save_path.seek(0) # Move to the first row to overwrite it
            self.save_path.write(filedata)
            self.save_path.flush() # Save without closing
            # typically the above line would do. however this is used to ensure that the file is written
            os.fsync(self.save_path.fileno())
            self.saved = True
            
    def forward_back(self, image_number):
        
        " Forward button to continue to the next image in the folder."
        
        self.tree.selection_set(str(int(image_number-1)))
        # Print the corresponding image
        self.my_label.config(image=self.image_list[image_number-1])
        
        # Update button commands
        self.button_forw.config(image = self.forw_img, bg = self.parent['bg'], 
                            command = lambda: self.forward_back(image_number+1),
                            text = '', state = tk.NORMAL)
        self.button_back.config(image = self.back_img, bg = self.parent['bg'], 
                            command = lambda: self.forward_back(image_number-1),
                            text = '', state = tk.NORMAL)
        if image_number == self.N:
            self.button_forw.config(state = tk.DISABLED)
        if image_number == 1:
            self.button_back.config(state = tk.DISABLED)
        
        # Classes buttons
        # var = {}
        for i,cl in enumerate(self._class_list):
            # print(out_data[image_number-1,i])
            self.var[image_number-1,i] = tk.IntVar(
                value = int(self.out_data[image_number-1,i]))
            # var[i] = tk.IntVar(value = int(self.out_data[image_number-1,i]))
            # I can not make this be selected when going backwards or forward 
            # if it was previously selected.
            self.button_cl[cl].config(text = cl, fg = 'white', bg = self.parent['bg'], 
                selectcolor = 'black', height = 3, width = 20, 
                variable = self.var[image_number-1,i], 
                command=(lambda i=i: self.onPress(image_number-1,i)))

        # Status bar    
        self.status.config(text='Image ' + str(image_number) + ' of '+str(self.N), 
            bd = 1, relief = tk.SUNKEN, anchor = tk.E, fg = 'white', 
            bg = self.parent['bg'])
            
    def onPress(self, n,i):
        
        "Updates the stored values on clicking the checkbutton."
        
        self.out_data[n,i] = not self.out_data[n,i]
        self.tree.item(self.tree.get_children()[n], text = n+1, 
                       values = tuple(self.out_data[n,:].astype(int)))
        self.saved = False
        
    def OnDoubleClick(self, event):
        
        "Moves to the image corresponding to the row clicked on the tree."
        
        item = self.tree.selection()[0]
        self.forward_back(self.tree.item(item,"text"))

class ResizableImgLabel(tk.Label):
    def __init__(self, master, image_path:str='', scale:float=1.0, **kwargs):
        tk.Label.__init__(self, master, **kwargs)
        self.configure(bg=master['bg'])
        self.img   = None if not image_path else Image.open(image_path)
        self.p_img = None
        self.scale = scale
                
        self.bind("<Configure>", self.resizing)
        
    def set_image(self, image_path:str):
        self.img   = Image.open(image_path)
        self.resizing()

    def resizing(self, event=None):
        if self.img:
            iw, ih  = self.img.width, self.img.height
            mw, mh  = self.master.winfo_width(), self.master.winfo_height()
            
            if iw>ih:
                ih = ih*(mw/iw)
                r = mh/ih if (ih/mh) > 1 else 1
                iw, ih = mw*r, ih*r
            else:
                iw = iw*(mh/ih)
                r = mw/iw if (iw/mw) > 1 else 1
                iw, ih = iw*r, mh*r
                
            self.p_img = ImageTk.PhotoImage(self.img.resize((int(iw*self.scale), int(ih*self.scale))))
            self.config(image=self.p_img)