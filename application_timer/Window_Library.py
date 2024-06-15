''' 
This file is the sub-main file within the application_timer directory. 
It communicates between all the other files within this directory.
'''

import window_utils
import time

# This library is supposed to get the the active window of the system.
class WindowLibrary():
    def __init__(self):
        window_utils_instance = window_utils.WindowUtils()
        window_utils_instance.window_grab()
        # window_utils_instance.day_data()

WindowLibrary()