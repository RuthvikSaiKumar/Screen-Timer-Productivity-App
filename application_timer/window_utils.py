'''
This file monitors the active window and logs the amount of time spent on each window.
Has the ability to check each tab within the browers. 
'''
import pygetwindow as gw
import time
from datetime import date
import pickle

# This class is supposed to give the main file, the data on current window. 
class WindowUtils():

    def __init__(self):
        self.previous_window = None
        self.window_title = None
        self.today = date.today()
        self.start_time = 0
        self.window_screentime = {}
        self.end_time = 0

    # This method will enable us to call this function and make a save of data for each session and renew the dict.
    def refresh_data(self):
        self.window_screentime = {}

    def save_data(self):
        # Save the data in a temp file for the session every 2min.
        print()

    def data_parse(self):
        # Send the data to data_model.py for it to make a Dataframe. 
        print()

    def window_grab(self):
        # This loop should run infinitely unless inturrepted via keyboard
        while True:
            try:
                window = gw.getActiveWindow()
                if self.previous_window!=window:
                    if self.previous_window is not None:
                        self.end_time = time.time()
                        window_time = self.end_time - self.start_time
                        # h, m, s = int(window_time // 3600), int(window_time % 3600) // 60, int(window_time % 60)
                        # print("Time spent on ", self.previous_window.title, " is: ", f"{h:02}:{m:02}:{s:02}")
                        window_time_hhmmss = time.strftime("%H:%M:%S", time.gmtime(window_time))
                        self.window_screentime[self.previous_window.title] = {
                            "apptype": "browser",  # or "application"
                            "time_spent": {
                                "hours": int(window_time_hhmmss.split(":")[0]),
                                "minutes": int(window_time_hhmmss.split(":")[1]),
                                "seconds": int(window_time_hhmmss.split(":")[2]),
                                }
                        }
                    elif (self.previous_window) is None or self.previous_window == ' ':
                        pass
                    self.previous_window = window
                    self.start_time = time.time()

                # self.window_time += 1
                time.sleep(1)
            except KeyboardInterrupt:
                if self.previous_window is not None:
                    self.end_time = time.time()
                    window_time = self.end_time - self.start_time
                    # print("Time spent on ", self.previous_window.title, " is: ", window_time)
                    # h, m, s = int(window_time // 3600), int(window_time % 3600) // 60, int(window_time % 60)
                    # print("Time spent on ", self.previous_window.title, " is: ", f"{h:02}:{m:02}:{s:02}")
                    window_time_hhmmss = time.strftime("%H:%M:%S", time.gmtime(window_time))
                    self.window_screentime[self.previous_window.title] = {
                        "apptype": "browser",  # or "application"
                        "time_spent": {
                            "hours": int(window_time_hhmmss.split(":")[0]),
                            "minutes": int(window_time_hhmmss.split(":")[1]),
                            "seconds": int(window_time_hhmmss.split(":")[2]),
                            }
                    }
                    print(self.window_screentime)
                break

