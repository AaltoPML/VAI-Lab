#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@authors: 	Armi Tiihonen, Felipe Oviedo, Shreyaa Raghavan, Zhe Liu
MIT Photovoltaics Laboratory
"""

import os
import pandas as pd
import seaborn as sns
from scipy.integrate import simps
import numpy as np
from vai_lab._plugin_templates import DataProcessingT
from vai_lab._import_helper import rel_to_abs

_PLUGIN_READABLE_NAMES = {"RGBprocessing": "default",
                          "rgbprocessing": "alias",}            # type:ignore
_PLUGIN_MODULE_OPTIONS = {"Type": "Other"}                      # type:ignore
_PLUGIN_REQUIRED_SETTINGS = {}                                  # type:ignore
_PLUGIN_OPTIONAL_SETTINGS = {}                                  # type:ignore
_PLUGIN_REQUIRED_DATA = {}                                      # type:ignore
_PLUGIN_OPTIONAL_DATA = {}                                      # type:ignore

class RGBprocessing(DataProcessingT):
    """
    Class RGB_data points at the moment at average RGB values only
    """

    def __init__(self, config = {}, data_in = [None], ini = False):
        """Initialises parent class.
            Passes `globals` dict of all current variables
        """
        super().__init__(globals())
        if not ini:
            # Model configuration
            self.set_data_in(data_in)
            self.configure(config)
            # Model initialisation    
            try:    
                self.model = RGB_data(**self._config["options"])
            except Exception as exc:
                print('The plugin encountered an error on the parameters of '
                        +str(list(self._PLUGIN_READABLE_NAMES.keys())[list(self._PLUGIN_READABLE_NAMES.values()).index('default')])+': '+str(exc)+'.')
                raise
        else:
            self.model = RGB_data
            
        self.fit_plugin = self.model.preprocess
        self.transform_plugin = self.model.compute_degradation

#Classes and Functions
#Class RGB_data points at the moment at average RGB values only, future version
#will define
#file_name during instantiation
class RGB_data:
    
    def __init__(self, folder, compositions, cutoff = None, is_calibrated = True, is_rgb = True):
        
        if (is_calibrated and is_rgb):
            filenames = ['sample_r_cal.csv', 'sample_g_cal.csv', 'sample_b_cal.csv']
        elif ((not is_calibrated) and is_rgb):
            filenames = ['sample_r.csv', 'sample_g.csv', 'sample_b.csv']
        elif (is_calibrated and (not is_rgb)):
            filenames = ['sample_Ll_cal.csv', 'sample_La_cal.csv', 'sample_Lb_cal.csv']
        else:
            filenames = ['sample_Ll.csv', 'sample_La.csv', 'sample_Lb.csv']
        
        if type(compositions) is str:
            if os.path.isabs(compositions):
                try:
                    compositions = pd.read_csv(compositions).get("Sample")
                except Exception as exc:
                    print('The plugin encountered an error trying to read the provided path to compositions: \"'
                            +compositions+'\"')
                    raise
            else:
                try:
                    compositions = pd.read_csv(rel_to_abs(compositions)).get("Sample")
                except Exception as exc:
                    print('The plugin encountered an error trying to read the provided path to compositions: \"'
                            +compositions+'\"')
                    raise

        os.chdir(rel_to_abs(folder))
        self.compositions = compositions
        compositions = pd.Series(compositions)
        
        self.red = pd.read_csv(filenames[0], header=None)
        self.red = self.red.T
        self.red.columns = compositions
        
        self.green = pd.read_csv(filenames[1], header=None)
        self.green = self.green.T
        self.green.columns = compositions
        
        self.blue = pd.read_csv(filenames[2], header=None)
        self.blue = self.blue.T
        self.blue.columns = compositions
        
        self.time = pd.read_csv('times.csv', header=None)  
        
        if cutoff:
            self.time = self.time[self.time[0] < cutoff]
            self.red = self.red.iloc[:self.time.shape[0],:]
            self.blue = self.blue.iloc[:self.time.shape[0],:]
            self.green = self.green.iloc[:self.time.shape[0],:]
    
    def preprocess(self, normalize = None):
        time_col = pd.DataFrame(np.tile(self.time.values, (self.red.shape[1], 1)))
        red = self.red.melt(var_name='columns')
        green = self.green.melt(var_name='columns')
        blue = self.blue.melt(var_name='columns')
        
        red['time'] = time_col
        green['time'] = time_col
        blue['time'] = time_col
        
        min_color = np.min([red['value'].min(), green['value'].min(), blue['value'].min()])
        max_color = np.max([red['value'].max(), green['value'].max(), blue['value'].max()])

        
        if normalize == 'max':
            
            red['value'] = red['value'] / max_color
            green['value'] = green['value'] / max_color
            blue['value'] = blue['value'] / max_color
        
        elif normalize == 'min_max':
        
            red['value'] = (red['value'] - min_color) / (max_color - min_color)
            green['value'] = (green['value'] - min_color) / (max_color - min_color)
            blue['value'] = (blue['value'] - min_color) / (max_color - min_color)
        
        
        self.red_p = red
        self.blue_p = blue
        self.green_p = green
        
        return red, green, blue, time_col
    
    def plot_samples(self, color_name):
        
        dfm = pd.DataFrame()
        sns.set_style("darkgrid")
        
        if color_name == 'red':
            dfm = self.red_p
            g = sns.FacetGrid(dfm, col='columns', col_wrap=4)
            g = (g.map(sns.lineplot, 'time','value'))
        elif color_name == 'green':
            dfm = self.green_p
            g = sns.FacetGrid(dfm, col='columns', col_wrap=4)
            g = (g.map(sns.lineplot, 'time','value'))           
        elif color_name == 'blue':
            dfm = self.blue_p
            g = sns.FacetGrid(dfm, col='columns', col_wrap=4)
            g = (g.map(sns.lineplot, 'time','value'))
        elif color_name == 'all':
            red_t = self.red_p
            red_t['Color'] = 'Red'
            blue_t = self.blue_p
            blue_t['Color'] = 'Blue'
            green_t = self.green_p
            green_t['Color'] = 'Green'
            dfm = pd.concat([red_t,blue_t,green_t])
            sns.set_palette(palette=sns.xkcd_palette(["pale red", "denim blue", "medium green"]))
            g = sns.FacetGrid(dfm, col='columns', hue='Color', col_wrap=4)
            #Define axis limits here
            g.set(ylim=(0, 140))
            g = (g.map(sns.lineplot, 'time', 'value'))


        
    def compute_degradation(self, method):
        
        merits_r = []
        merits_g = []
        merits_b = []
        
        for key, value in self.compositions.items():
            filtered_r = self.red_p[self.red_p['columns'] == value]
            filtered_g = self.green_p[self.green_p['columns'] == value]
            filtered_b = self.blue_p[self.blue_p['columns'] == value]
            
            #Only using area under curve
            if method == 'area':
                merit_r = simps(filtered_r.value, filtered_r.time)
                merit_g = simps(filtered_g.value, filtered_g.time)
                merit_b = simps(filtered_b.value, filtered_b.time)
            
            #Using differential area between curves, always positive and robust to multiple intersections
            elif method == 'diff_area':
                merit_r = simps( abs(filtered_r.value - np.repeat(filtered_r.value.iloc[0],len(filtered_r.value))),
                                     filtered_r.time)
                merit_g = simps( abs(filtered_g.value - np.repeat(filtered_g.value.iloc[0],len(filtered_g.value))),
                                     filtered_g.time)
                merit_b = simps( abs(filtered_b.value - np.repeat(filtered_b.value.iloc[0],len(filtered_b.value))),
                                     filtered_b.time)
                
            # elif method == 'dtw':
            #     exp_r = np.zeros((len(filtered_r.value), 2))
            #     base_r = np.zeros((len(filtered_r.value), 2))
            #     base_r[:,0] = filtered_r.time
            #     base_r[:,1] = np.repeat(filtered_r.value.iloc[0],len(filtered_r.value))
            #     exp_r[:, 0] = filtered_r.time
            #     exp_r[:, 1] = filtered_r.value
            #     merit_r, rr = similaritymeasures.dtw(exp_r, base_r)
                
            #     exp_g = np.zeros((len(filtered_g.value), 2))
            #     base_g = np.zeros((len(filtered_g.value), 2))
            #     base_g[:,0] = filtered_g.time
            #     base_g[:,1] = np.repeat(filtered_g.value.iloc[0],len(filtered_g.value))
            #     exp_g[:, 0] = filtered_g.time
            #     exp_g[:, 1] = filtered_g.value
            #     merit_g, gr = similaritymeasures.dtw(exp_g, base_g)

            #     exp_b = np.zeros((len(filtered_b.value), 2))
            #     base_b = np.zeros((len(filtered_b.value), 2))
            #     base_b[:,0] = filtered_b.time
            #     base_b[:,1] = np.repeat(filtered_b.value.iloc[0],len(filtered_b.value))
            #     exp_b[:, 0] = filtered_b.time
            #     exp_b[:, 1] = filtered_b.value
            #     merit_b, br = similaritymeasures.dtw(exp_b, base_b)           
            
            #Inverted momentum, scaled by 1/sqrt(x) changing the scaling changes the importance of our sample in time... we 
            #can compute a rate of degradation based in that
            elif method == 'inverted_moment':
                c = 1 #Avoids numerical errors during evaluation
                merit_r = simps(filtered_r.value * (1/np.sqrt(filtered_r.time + c)), filtered_r.time)
                merit_g = simps(filtered_g.value * (1/np.sqrt(filtered_g.time + c)), filtered_g.time)
                merit_b = simps(filtered_b.value * (1/np.sqrt(filtered_b.time + c)), filtered_b.time)
                
                merit_r = simps( abs( (1/np.sqrt(filtered_r.time + c))*(filtered_r.value - np.repeat(filtered_r.value.iloc[0],len(filtered_r.value)))),
                                     filtered_r.time )
                merit_g = simps( abs((1/np.sqrt(filtered_g.time + c))*(filtered_g.value - np.repeat(filtered_g.value.iloc[0],len(filtered_g.value)))),
                                     filtered_g.time )
                merit_b = simps( abs((1/np.sqrt(filtered_b.time + c))*(filtered_b.value - np.repeat(filtered_b.value.iloc[0],len(filtered_b.value)))),
                                     filtered_b.time ) 

            merits_r.append(merit_r)
            merits_g.append(merit_g)
            merits_b.append(merit_b)
            
        degradation_df = pd.DataFrame(
                {'Red': merits_r,
                 'Green': merits_g,
                 'Blue': merits_b,
                 })
    
        degradation_df['Merit'] = degradation_df.Red + degradation_df.Blue + degradation_df.Green
        #degradation_df.index = pd.Series(self.compositions)
        degradation_df.insert(loc=0, column='Sample', value=pd.Series(self.compositions))

            
        return degradation_df