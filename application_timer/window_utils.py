'''
This file monitors the active window and logs the amount of time spent on each window.
Has the ability to check each tab within the browers. 
'''
import pygetwindow as gw
import time
from datetime import date
import pickle
import psutil
# from user_agents import parse

# This class is supposed to give the main file, the data on current window. 
class WindowUtils():

    def __init__(self):
        self.previous_window = None
        self.window_title = None
        self.today = date.today()
        self.start_time = 0
        self.window_screentime = {}
        self.end_time = 0
        self.save_path = 'window_screentime_cache.pkl'
        self.last_save_time = time.time()
        # self.browser = user_agent.browser.family
        self.browser_list = ["Chrome", "Firefox", "Edge", "Safari", "Opera", "Internet Explorer", "Vivaldi", "Brave", "Torch", "Yandex Browser", "Maxthon", "Coc Coc", "Comodo Dragon", "Epic Privacy Browser", "Waterfox", "Pale Moon", "SeaMonkey", "Tor Browser", "Brave Privacy Browser", "K-Meleon"]

    # This method will enable us to call this function and make a save of data for each session and renew the dict.
    def refresh_data(self):
        self.window_screentime = {}

    def save_data(self, interrupt= False):
        # Save the data in a temp file for the session every 2min.
        current_time = time.time()
        if current_time -  self.last_save_time >= 120 or interrupt:
            with open(self.save_path, "wb") as f:
                pickle.dump(self.window_screentime, f)
            self.window_screentime = {}                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        
            self.last_save_time = current_time

    def data_parse(self):
        # Send the data to data_model.py for it to make a Dataframe. 
        print()

    def get_app_type(self, window):
        try:
            for process in psutil.process_iter(['pid', 'name']):
                try:
                    if process.info['name'].lower() in [i.lower() + '.exe' for i in self.browser_list]:
                        if window.title in process.as_dict()['cmdline']:
                            return "browser"
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    pass
        except KeyboardInterrupt:
            pass
        return "application"

    def window_grab(self):
        # This loop should run infinitely unless inturrepted via keyboard
        while True:
            # This try and except blocks help in detecting the focused windows and their times whilst 
            # handling the exceptions of keyboard intruption 
            try:
                window = gw.getActiveWindow()
                if self.previous_window!=window:
                    if self.previous_window is not None:
                        # print(self.browser)
                        self.end_time = time.time()
                        window_time = self.end_time - self.start_time
                        h, m, s = int(window_time // 3600), int(window_time % 3600) // 60, int(window_time % 60)
                        print("Time spent on ", self.previous_window.title, " is: ", f"{h:02}:{m:02}:{s:02}")
                        window_time_hhmmss = time.strftime("%H:%M:%S", time.gmtime(window_time))
                        # browser_found = False
                        # This loop checks if the active window is a browser or an application
                        # for i in self.browser_list:
                        #     if not browser_found:
                        #         for j in self.previous_window.title.split() :
                        #             if i.lower() == j.lower():
                        #                 app_type = "browser"
                        #                 browser_found = True
                        #                 break
                        #         if browser_found:
                        #             break
                        # if not browser_found:
                        #     app_type = "application"
                        app_type = self.get_app_type(self.previous_window)
                        self.window_screentime[self.previous_window.title] = {
                            "apptype": app_type,  # or "application"
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
                self.save_data()
                time.sleep(1)

            except KeyboardInterrupt:
                if self.previous_window is not None:
                    self.end_time = time.time()
                    window_time = self.end_time - self.start_time
                    # print("Time spent on ", self.previous_window.title, " is: ", window_time)
                    h, m, s = int(window_time // 3600), int(window_time % 3600) // 60, int(window_time % 60)
                    print("Time spent on ", self.previous_window.title, " is: ", f"{h:02}:{m:02}:{s:02}")
                    window_time_hhmmss = time.strftime("%H:%M:%S", time.gmtime(window_time))
                    app_type = self.get_app_type(self.previous_window)
                    self.window_screentime[self.previous_window.title] = {
                        "apptype": app_type,  # or "application"
                        "time_spent": {
                            "hours": int(window_time_hhmmss.split(":")[0]),
                            "minutes": int(window_time_hhmmss.split(":")[1]),
                            "seconds": int(window_time_hhmmss.split(":")[2]),
                            }
                    }
                    print(self.window_screentime)
                self.save_data(interrupt = True)
                break

# TODO : Implement a way to avoid loss of data from certain applications due to the limits of pygetwindow