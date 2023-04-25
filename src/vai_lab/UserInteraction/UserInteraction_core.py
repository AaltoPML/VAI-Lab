# -*- coding: utf-8 -*-
from vai_lab.GUI.GUI_core import GUI
class UserInteraction(GUI):
    """UserFeedback core class directly uses GUI_core.py"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
