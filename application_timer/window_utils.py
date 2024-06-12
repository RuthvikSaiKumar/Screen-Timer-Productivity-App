'''
This file monitors the active window and logs the amount of time spent on each window.
Has the ability to check each tab within the browers. 
'''
'''
import data_manager
import data_model
import window_utils

class WindowLibrary:
    def __init__(self, data_file):
        self.data_manager = data_manager.DataManager(data_file)
        self.data_model = data_model.DataModel(self.data_manager.load_data())
        self.window_utils = window_utils.WindowUtils()

    def get_data(self):
        return self.data_model.get_data()

    def process_window_events(self):
        self.window_utils.process_events()

'''

import pygetwindow as gw

class WindowUtils:
    def __init__(self):
        self.window = gw.getActiveWindow()

    def process_events(self):
        # Process window events using getwindows library
        pass