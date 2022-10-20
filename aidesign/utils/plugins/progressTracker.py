# Import the required libraries
import tkinter as tk
from PIL import ImageTk
import os
import numpy as np
import pandas as pd
import time

from aidesign.Data.xml_handler import XML_handler
from aidesign.utils.plugin_helpers import PluginSpecs

_PLUGIN_READABLE_NAMES = {"progress_tracker":"default","progressTracker":"alias","progress tracker":"alias"}
_PLUGIN_MODULE_OPTIONS = {"layer_priority": 2,
                            "required_children": None}
_PLUGIN_REQUIRED_SETTINGS = {"id_done"}
_PLUGIN_OPTIONAL_SETTINGS = {}

class progressTracker(tk.Frame):
    """Canvas for the visualisation of the pipeline state."""
    
    def __init__(self, parent, controller, config:dict):
        
        """ Here we define the frame displayed for the plugin specification."""
        
        super().__init__(parent, bg = parent['bg'])
        self.bg = parent['bg']
        self.controller = controller
        self.s = XML_handler()
        
        self.controller.title('Progress Tracker')
        
        script_dir = os.path.dirname(__file__)
        self.tk.call('wm','iconphoto', self.controller._w, ImageTk.PhotoImage(
            file = os.path.join(os.path.join(
                script_dir, 
                'resources', 
                'Assets', 
                'AIDIcon.ico'))))
        self.grid_rowconfigure(tuple(range(2)), weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        frame1 = tk.Frame(self, bg = self.bg)
        self.frame2 = tk.Frame(self, bg = self.bg)
        frame3 = tk.Frame(self, bg = self.bg)
        self.frame4 = tk.Frame(self, bg = self.bg)
        
        # Create canvas
        self.width, self.height = 600, 600
        self.canvas = tk.Canvas(frame1, width=self.width, 
            height=self.height, background="white")
        self.canvas.pack(fill = tk.BOTH, expand = True, padx=(10,0), pady=10)
        
        self.w, self.h = 100, 50
        self.cr = 4
        """
        TODO: Implement clicking on canvas actions
        """
        self.canvas.bind('<Button-1>', self.on_click)
        self.dataType = {}
        
        self.upload()

        sec = 5
        self.click = False
        self.my_label = tk.Label(self.frame2, 
                    text = 
                    'This window will get\nclosed after '+str(sec)+' seconds\nunless you click on the canvas.',
                    pady= 10,
                    font = self.controller.title_font,
                    bg = self.bg,
                    fg = 'white',
                    anchor = tk.CENTER)
        self.my_label.grid(column = 0,
                            row = 0, columnspan = 2, padx=10)
        tk.Button(
            self.frame4, text = 'Next step', fg = 'white', bg = parent['bg'], 
            height = 3, width = 15, font = self.controller.pages_font, 
            command = self.check_quit).grid(column = 1, row = 26, sticky="news", pady=(0,10))
        tk.Button(
            self.frame4, text = 'Stop pipeline', fg = 'white', bg = parent['bg'], 
            height = 3, width = 15, font = self.controller.pages_font, 
            command = self.terminate).grid(column = 0, row = 26, sticky="news", pady=(0,10))
        
        self.controller._append_to_output('close', False)
        self.save_path = ''
        self.saved = True
        frame1.grid(column=0, row=0, sticky="nsew")
        self.frame2.grid(column=1, row=0, sticky="new")
        frame3.grid(column=0, row=1, sticky="swe")
        self.frame4.grid(column=1, row=1, sticky="sew")
        
        frame3.grid_columnconfigure(tuple(range(2)), weight=1)
        self.frame4.grid_columnconfigure(tuple(range(2)), weight=1)

        self.controller.after(sec*1000,lambda:self.check_click())

    def class_list(self,value):
        """ Temporary fix """
        return value

    def on_click(self, event):
        """ Passes the mouse click coordinates to the select function."""
        self.click = True
        self.select(event.x, event.y)
    
    def check_click(self):
        """ If not clicked on canvas, closes the window."""
        if not self.click:
            self.check_quit()

    def terminate(self):
        """ Terminates window and pipeline. """
        self.controller._append_to_output('close', True)
        self.check_quit()
        
    def select(self, x: float, y:float):
        """ 
        Selects the module at the mouse location and updates the associated 
        plugins as well as the colours. 
        Blue means no plugin has been specified,
        Orange means the module is selected.
        Green means the plugin for this module is already set. 
        :param x: float type of module x coordinate
        :param y: float type of module y coordinate
        """
        self.selected = self.canvas.find_overlapping(
            x-5, y-5, x+5, y+5)
        if self.selected:
            if len(self.selected) > 2:
                self.canvas.selected = self.selected[-2]
            else:
                self.canvas.selected = self.selected[-1]
            if len(self.canvas.gettags(self.canvas.selected)) > 0:
                if not (len(self.canvas.gettags(self.canvas.selected)[0].split('-')) > 1) and\
                    not (self.canvas.gettags(self.canvas.selected)[0].split('-')[0] == 'loop'):
                    self.m = int(self.canvas.gettags(self.canvas.selected)[0][1:])
                if self.m > 1:
                    self.optionsWindow()

    def module_out(self, name):
        """ Updates the output DataFrame.
        
        :param name: name of the model
        :type name: str
        """
        name_list = list(self.out_data.columns)
        m_num = [n for n in name_list if (n.split('-')[0] == name)]
        if len(m_num) > 0:
            name_list.append(name + '-' + str(len(m_num)))
        else:
            name_list.append(name)
        self.canvas.itemconfig('t'+str(self.modules), text = name_list[-1])
        values = self.out_data.values
        values = np.vstack((
                    np.hstack((values, np.zeros((values.shape[0],1)))),
                    np.zeros((1, values.shape[0]+1))))
        self.out_data = pd.DataFrame(values, 
                                     columns = name_list, 
                                     index = name_list)
        self.module_names.append(name_list[-1])

    def pretty_status(self,status: dict):
        status_str = ''
        for key in status.keys():
            status_str += str(key) +': '+str(status[key])+'\n'
        return status_str

    def add_module(self,boxName: str,x: float,y:float,ini = False,out = False):
        """ Creates a rectangular module with the corresponding text inside.
        
        :param boxName: name of the model
        :type boxName: str
        :param x: float type of module x coordinate
        :param y: float type of module y coordinate
        :param ini: bool type of whether the module corresponds to initialiser.
        :param out: bool type of whether the module corresponds to output.
        """
        if not ini and not out:
            tag = ('o'+str(self.modules),)
        else: #Make initialisation and output unmoveable
            tag = ('n0',)
        text_w = self.controller.pages_font.measure(boxName+'-00') + 10
        # Check module status
        if 'start' in self.controller.status[boxName]:
            if 'finish' in self.controller.status[boxName]:
                colour = '#46da63'
            else:
                colour = '#dbaa21'
        else:
            colour = self.bg
        
        self.canvas.create_rectangle(
            x - text_w/2 , 
            y - self.h/2, 
            x + text_w/2, 
            y + self.h/2, 
            tags = tag + ('p'+str(self.modules),), 
            fill = colour, 
            width = 3,
            # activefill = '#dbaa21'
            )
        
        self.canvas.create_text(
            x, 
            y, 
            font = self.controller.pages_font, 
            text = boxName, 
            tags = tag + ('t'+str(self.modules),), 
            fill = '#d0d4d9', 
            justify = tk.CENTER)
        
        CanvasTooltip(self.canvas, self.canvas.find_withtag('p'+str(self.modules))[0], 
                           text = 'Model progress status:\n'+self.pretty_status(self.controller.status[boxName])) # Link box
        CanvasTooltip(self.canvas, self.canvas.find_withtag('t'+str(self.modules))[0], 
                           text = 'Model progress status:\n'+self.pretty_status(self.controller.status[boxName])) # Link text
        
        if not out:
            self.canvas.create_oval(
                x - self.cr, 
                y + self.h/2 - self.cr, 
                x + self.cr, 
                y + self.h/2 + self.cr, 
                width = 2, 
                fill = 'black', 
                tags = tag + ('d'+str(self.modules),))
            
        if not ini:
            self.canvas.create_oval(
                x - self.cr, 
                y - self.h/2 - self.cr, 
                x + self.cr, 
                y - self.h/2 + self.cr, 
                width = 2, 
                fill = 'black', 
                tags = tag + ('u'+str(self.modules),))
        
        if not out and not ini:
            self.canvas.create_oval(
                x - text_w/2 - self.cr, 
                y - self.cr, 
                x - text_w/2 + self.cr, 
                y + self.cr, 
                width = 2, 
                fill = 'black', 
                tags = tag + ('l'+str(self.modules),))
        
            self.canvas.create_oval(
                x + text_w/2 - self.cr, 
                y - self.cr, 
                x + text_w/2 + self.cr, 
                y + self.cr, 
                width = 2, 
                fill = 'black', 
                tags = tag + ('r'+str(self.modules),))
            
        self.canvas.startxy.append((x, y))
        self.connections[self.modules] = {}
        self.module_out(boxName)
        self.module_list.append(boxName)
        self.modules += 1
        
    def optionsWindow(self):
        """ Function to create a new window displaying the available options 
        of the selected plugin."""
        
        self.module = np.array(self.module_list)[self.m == np.array(self.id_mod)][0]
        self.plugin = self.s.loaded_modules[self.module]['plugin']['plugin_name']
        module_type = self.s.loaded_modules[self.module]['module_type']
        ps = PluginSpecs()
        self.opt_settings = ps.optional_settings[module_type][self.plugin]
        self.req_settings = ps.required_settings[module_type][self.plugin]
        if (len(self.opt_settings) != 0) or (len(self.req_settings) != 0):
            if hasattr(self, 'newWindow') and (self.newWindow!= None):
                self.newWindow.destroy()
            self.newWindow = tk.Toplevel(self.controller)
            # Window options
            self.newWindow.title(self.plugin+' plugin options')
            script_dir = os.path.dirname(__file__)
            self.tk.call('wm','iconphoto', self.newWindow, ImageTk.PhotoImage(
                file = os.path.join(os.path.join(
                    script_dir, 
                    'resources', 
                    'Assets', 
                    'AIDIcon.ico'))))
            self.newWindow.geometry("350x400")

            frame1 = tk.Frame(self.newWindow)
            frame4 = tk.Frame(self.newWindow)
            
            # Print settings
            tk.Label(frame1,
                  text ="Please indicate your desired options for the "+self.plugin+" plugin.", anchor = tk.N, justify=tk.LEFT).pack(expand = True)
            self.entry = []
            # Required
            r = 1
            if len(self.req_settings) > 0:
                frame2 = tk.Frame(self.newWindow)
                tk.Label(frame2,
                      text ="Required settings:", anchor = tk.W, justify=tk.LEFT).grid(row=0,column=0 , columnspan=2)
                self.displaySettings(frame2, self.req_settings)
                frame2.grid(column=0, row=r, sticky="nswe")
                r += 1
            # Optional
            if len(self.opt_settings) > 0:
                frame3 = tk.Frame(self.newWindow)
                tk.Label(frame3,
                      text ="Optional settings:", anchor = tk.W, justify=tk.LEFT).grid(row=0,column=0, columnspan=2)
                self.displaySettings(frame3, self.opt_settings)
                frame3.grid(column=0, row=r, sticky="nswe")
                r += 1
            if len(self.entry) > 0:
                self.entry[0].focus()
            self.finishButton = tk.Button(
                frame4, text = 'Finish', command = self.removewindow)
            self.finishButton.grid(column = 1, row = r+1, sticky="es", pady=(0,10), padx=(0,10))
            self.finishButton.bind("<Return>", lambda event: self.removewindow())
            self.newWindow.protocol('WM_DELETE_WINDOW', self.removewindow)

            frame1.grid(column=0, row=0, sticky="new")
            frame4.grid(column=0, row=r, sticky="se")
            self.newWindow.grid_rowconfigure(0, weight=1)
            self.newWindow.grid_rowconfigure(tuple(range(r+1)), weight=2)
            self.newWindow.grid_columnconfigure(0, weight=1)

    def displaySettings(self, frame, settings):
        """ Adds an entry for each input setting. Displays it in the specified row.
        :param frame: tkinter frame type of frame
        :param settings: dict type of plugin setting options
        """
        r = 1
        options = self.s.loaded_modules[self.module]['plugin']['options']
        for arg, val in settings.items():
            tk.Label(frame,
              text = arg).grid(row=r,column=0)
            if arg == 'Data':
                if self.m not in self.dataType:
                    self.dataType[self.m] = tk.StringVar()
                    self.dataType[self.m].set('X')
                tk.Radiobutton(frame, text = 'Input (X)', fg = 'black', 
                               var = self.dataType[self.m], value = 'X'
                               ).grid(row=r, column=1)
                if len(self.s._get_all_elements_with_tag("Y")) > 0 or \
                    len(self.s._get_all_elements_with_tag("Y_test")) > 0:
                    tk.Radiobutton(frame, text = 'Output (Y)', fg = 'black', 
                                   var = self.dataType[self.m], value = 'Y'
                                   ).grid(row=r, column=2)
            else:
                self.entry.append(tk.Entry(frame))
                value = options[arg] if arg in options else 'default'
                self.entry[-1].insert(0, str(value))
                self.entry[-1].grid(row=r, column=1)
                self.entry[-1].bind("<Return>", lambda event, a = len(self.entry): self.on_return_entry(a))
            r += 1
        frame.grid_rowconfigure(tuple(range(r)), weight=1)
        frame.grid_columnconfigure(tuple(range(2)), weight=1)

    def removewindow(self):
        """ Stores settings options and closes window """
        self.req_settings.pop("Data", None)
        req_keys = list(self.req_settings.keys())
        opt_keys = list(self.opt_settings.keys())
        for e,ent in enumerate(self.entry):
            if e < len(self.req_settings):
                if len(ent.get()) == 0 or ent.get() == 'default':
                    self.req_settings.pop(req_keys[e], None)
                else:
                    self.req_settings[req_keys[e]] = ent.get()
            else:
                if len(ent.get()) == 0 or ent.get() == 'default':
                    self.opt_settings.pop(opt_keys[e-len(req_keys)], None)
                else:
                    self.opt_settings[opt_keys[e-len(req_keys)]] = ent.get()
        if self.m in self.dataType:
            self.req_settings['Data'] = self.dataType[self.m].get()
        self.newWindow.destroy()
        self.newWindow = None
        self.s.update_plugin_options(self.module,
                                       {**self.req_settings, **self.opt_settings},
                                       True)
        self.focus()

    def on_return_entry(self, r):
        """ Changes focus to the next available entry. When no more, focuses 
        on the finish button.
        : param r: int type of entry id.
        """
        if r < len(self.entry):
            self.entry[r].focus()
        else:
            self.finishButton.focus()

    def upload(self):
        """ Opens the XML file that was previously uploaded and places the 
        modules, loops and connections in the canvas."""
        
        filename = self.controller.output["xml_filename"]
        
        self.reset()

        self.s = XML_handler()
        self.s.load_XML(filename)
        # self.s._print_pretty(self.s.loaded_modules)
        modules = self.s.loaded_modules
        modout = modules['Output']
        del modules['Initialiser'], modules['Output'] # They are generated when resetting
        self.disp_mod = ['Initialiser', 'Output']
        self.id_mod = [0, 1]
        
        # Place the modules
        self.place_modules(modules)
        connect = list(modout['coordinates'][2].keys())
        for p, parent in enumerate(modout['parents']):
                parent_id = self.id_mod[np.where(np.array(self.disp_mod) == parent)[0][0]]
                out, ins = modout['coordinates'][2][connect[p]].split('-')
                xout, yout, _ , _ = self.canvas.coords(out[0]+str(parent_id))
                xins, yins, _, _ =self.canvas.coords(ins[0]+str(1))
                self.canvas.create_line(
                            xout + self.cr, 
                            yout + self.cr, 
                            xins + self.cr, 
                            yins + self.cr,
                            fill = "red", 
                            arrow = tk.LAST, 
                            tags = ('o'+str(parent_id), 
                                  'o'+str(1), modout['coordinates'][2][connect[p]]))
                self.out_data.iloc[int(parent_id)][1] = 1
                self.connections[1][
                    int(parent_id)] = out[0]+str(parent_id) + '-' + ins[0]+str(1)
        self.m = self.id_mod[2]
        x0, y0, x1, y1 = self.canvas.coords('p'+str(self.m))
        # self.select(x0, y0)

    def place_modules(self,modules: dict):
        """Places the modules in the dictionary in the canvas.
        :param modules: dict type of modules in the pipeline.
        """
        
        for key in [key for key, val in modules.items() if type(val) == dict]:
            if modules[key]['class'] == 'loop':
                # Extracts numbers from string
                l = int(''.join(map(str, list(filter(str.isdigit, modules[key]['name'])))))
                x0, y0, x1, y1 = modules[key]['coordinates']
                self.canvas.create_rectangle(x0, y0, 
                                             x1, y1, 
                                             outline = '#4ff07a',
                                             tag = 'loop-'+str(l))
                text_w = self.controller.pages_font.measure(modules[key]['type']) + 20
                self.canvas.create_text(
                    x0 + text_w/2, 
                    y0 + 20, 
                    font = self.controller.pages_font, 
                    text = modules[key]['type'], 
                    tags = ('loop-'+str(l), 'type'+'-'+str(l)), 
                    justify = tk.CENTER)
                text_w = self.controller.pages_font.measure(modules[key]['condition']) + 20
                self.canvas.create_text(
                    x1 - text_w/2, 
                    y0 + 20, 
                    font = self.controller.pages_font, 
                    text = modules[key]['condition'], 
                    tags = ('loop-'+str(l), 'condition'+'-'+str(l)), 
                    justify = tk.CENTER)
                self.loops.append({'type': modules[key]['type'],
                                   'condition': modules[key]['condition'],
                                   'mod': [], 
                                   'coord': (x0, y0, 
                                             x1, y1)})
                self.place_modules(modules[key])
            else:
                # Display module
                self.add_module(key,
                                modules[key]['coordinates'][0][0],
                                modules[key]['coordinates'][0][1])
                # self.module_list[-1] = modules[key]['module_type']
                self.id_mod.append(modules[key]['coordinates'][1])
                connect = list(modules[key]['coordinates'][2].keys())
                
                # Connect modules
                for p, parent in enumerate(modules[key]['parents']):
                    if not (parent[:4] == 'loop'):
                        parent_id = self.id_mod[np.where(np.array(self.disp_mod) == parent)[0][0]]
                        out, ins = modules[key]['coordinates'][2][connect[p]].split('-')
                        xout, yout, _ , _ = self.canvas.coords(out[0]+str(parent_id))
                        xins, yins, _, _ =self.canvas.coords(ins[0]+str(self.id_mod[-1]))
                        self.canvas.create_line(
                                    xout + self.cr, 
                                    yout + self.cr, 
                                    xins + self.cr, 
                                    yins + self.cr,
                                    fill = "red", 
                                    arrow = tk.LAST, 
                                    tags = ('o'+str(parent_id), 
                                          'o'+str(self.id_mod[-1]), modules[key]['coordinates'][2][connect[p]]))
                        self.out_data.iloc[int(parent_id)][int(self.id_mod[-1])] = 1
                        self.connections[int(self.id_mod[-1])][
                            int(parent_id)] = out[0]+str(parent_id) + '-' + ins[0]+str(self.id_mod[-1])
                    else:
                        self.loops[-1]['mod'].append(key)
                self.disp_mod.append(key)

    def reset(self):
        """ Resets the canvas and the stored information."""
        self.canvas.delete(tk.ALL) # Reset canvas
        
        if hasattr(self, 'newWindow') and (self.newWindow!= None):
            self.newWindow.destroy()
        
        self.canvas.startxy = []
        self.out_data = pd.DataFrame()
        self.connections = {}
        self.modules = 0
        self.module_list = []
        self.module_names = []
        
        self.add_module('Initialiser', self.width/2, self.h, ini = True)
        self.add_module('Output', self.width/2, self.height - self.h, out = True)
    
        self.draw = False
        self.loops = []
        self.drawLoop = False
        self.l = 0
        self.id_done = [0,1]
        self.plugin = {}

    def check_quit(self):
        self.controller.destroy()
        
class CanvasTooltip:
    '''
    It creates a tooltip for a given canvas tag or id as the mouse is
    above it.

    This class has been derived from the original Tooltip class I updated
    and posted back to StackOverflow at the following link:

    https://stackoverflow.com/questions/3221956/
           what-is-the-simplest-way-to-make-tooltips-in-tkinter/
           41079350#41079350

    Alberto Vassena on 2016.12.10.
    '''

    def __init__(self, canvas, tag_or_id,
                 *,
                 bg='#FFFFEA',
                 pad=(5, 3, 5, 3),
                 text='canvas info',
                 waittime=100,
                 wraplength=250):
        self.waittime = waittime  # in miliseconds, originally 500
        self.wraplength = wraplength  # in pixels, originally 180
        self.canvas = canvas
        self.text = text
        self.canvas.tag_bind(tag_or_id, "<Enter>", self.onEnter)
        self.canvas.tag_bind(tag_or_id, "<Leave>", self.onLeave)
        self.canvas.tag_bind(tag_or_id, "<ButtonPress>", self.onLeave)
        self.bg = bg
        self.pad = pad
        self.id = None
        self.tw = None

    def onEnter(self, event=None):
        self.schedule()

    def onLeave(self, event=None):
        self.unschedule()
        self.hide()

    def schedule(self):
        self.unschedule()
        self.id = self.canvas.after(self.waittime, self.show)

    def unschedule(self):
        id_ = self.id
        self.id = None
        if id_:
            self.canvas.after_cancel(id_)

    def show(self, event=None):
        def tip_pos_calculator(canvas, label,
                               *,
                               tip_delta=(10, 5), pad=(5, 3, 5, 3)):

            c = canvas

            s_width, s_height = c.winfo_screenwidth(), c.winfo_screenheight()

            width, height = (pad[0] + label.winfo_reqwidth() + pad[2],
                             pad[1] + label.winfo_reqheight() + pad[3])

            mouse_x, mouse_y = c.winfo_pointerxy()

            x1, y1 = mouse_x + tip_delta[0], mouse_y + tip_delta[1]
            x2, y2 = x1 + width, y1 + height

            x_delta = x2 - s_width
            if x_delta < 0:
                x_delta = 0
            y_delta = y2 - s_height
            if y_delta < 0:
                y_delta = 0

            offscreen = (x_delta, y_delta) != (0, 0)

            if offscreen:

                if x_delta:
                    x1 = mouse_x - tip_delta[0] - width

                if y_delta:
                    y1 = mouse_y - tip_delta[1] - height

            offscreen_again = y1 < 0  # out on the top

            if offscreen_again:
                # No further checks will be done.

                # TIP:
                # A further mod might automagically augment the
                # wraplength when the tooltip is too high to be
                # kept inside the screen.
                y1 = 0

            return x1, y1

        bg = self.bg
        pad = self.pad
        canvas = self.canvas

        # creates a toplevel window
        self.tw = tk.Toplevel(canvas.master)

        # Leaves only the label and removes the app window
        self.tw.wm_overrideredirect(True)

        win = tk.Frame(self.tw,
                       background=bg,
                       borderwidth=0)
        label = tk.Label(win,
                          text=self.text,
                          justify=tk.LEFT,
                          background=bg,
                          relief=tk.SOLID,
                          borderwidth=0,
                          wraplength=self.wraplength)

        label.grid(padx=(pad[0], pad[2]),
                   pady=(pad[1], pad[3]),
                   sticky=tk.NSEW)
        win.grid()

        x, y = tip_pos_calculator(canvas, label)

        self.tw.wm_geometry("+%d+%d" % (x, y))

    def hide(self):
        if self.tw:
            self.tw.destroy()
        self.tw = None

if __name__ == "__main__":
    app = progressTracker()
    app.mainloop()
