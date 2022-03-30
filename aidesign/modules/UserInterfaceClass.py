from abc import ABC, abstractmethod

"""Defines the parent class for all potential methods of user interface for the framework

Todo: declare what is commonly needed for this module and add below (WIP)
"""

class UI(ABC):
    @property
    def class_list(self):
        pass
        # """Set the class list"""
        
    @class_list.setter
    @abstractmethod
    def class_list(self,value):
        pass
    

    @abstractmethod
    def save_file(self):
        pass

    @abstractmethod
    def save_file_as(self):
        pass

    @abstractmethod
    def on_press(self):
        pass
