# -*- coding: utf-8 -*-

"""Import all submodules inside this folder and expose them with their respective names

Let's look for a more automatic way of doing this when we have more modules
"""
from ..UserInterfaceClass import UI
from .canvas_input import PageCanvas
from .manual_input import PageManual
from .startpage import StartPage