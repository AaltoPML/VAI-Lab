# -*- coding: utf-8 -*-
from aidesign.GUI.GUI_core import GUI
class UserFeedback(GUI):
    """UserFeedback core class directly uses GUI_core.py"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)