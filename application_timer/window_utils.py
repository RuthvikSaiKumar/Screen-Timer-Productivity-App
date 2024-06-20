"""
This file monitors the active window and logs the amount of time spent on each window.
Has the ability to check each tab within the browsers.  And It saves this data to a session dictionary or a
cache file
"""

import contextlib
import pygetwindow as gw
import time
from datetime import date
import datetime
import pickle
import psutil
import pandas as pd
import json
from cryptography.fernet import Fernet
import os

class WindowUtils:

    def __init__(self):
        self.previous_window = None
        self.window_title = None
        self.today = date.today()
        self.start_time = 0
        self.window_screentime = {}
        self.end_time = 0
        self.save_path = 'window_screentime_cache.pkl'
        self.last_save_time = time.time()
        self.key = None

        # Load the encryption key from the file
        if os.path.exists('KEY'):
            with open('KEY', 'rb') as k:
                self.key = k.read()
        else:
            self.key = Fernet.generate_key()
            with open('KEY', 'wb') as k:
                k.write(self.key)

    def refresh_data(self):
        self.window_screentime = {}

    def save_data(self, interrupt=False):
        # Save the data in a temp file for the session every 2min.
        current_time = time.time()
        if current_time - self.last_save_time >= 120 or interrupt:
            self.encrypt_and_save_data()
            self.window_screentime = {}
            self.last_save_time = current_time

    def encrypt_and_save_data(self):
        encrypted_data = self.encrypt_dict(self.window_screentime)
        with open(self.save_path, "wb") as f:
            f.write(encrypted_data)

    def encrypt_dict(self, data):
        json_data = json.dumps(data)
        encrypted_text = Fernet(self.key).encrypt(json_data.encode())
        return encrypted_text

    def decrypt_and_load_data(self):
        with open(self.save_path, "rb") as f:
            encrypted_data = f.read()
        decrypted_data = Fernet(self.key).decrypt(encrypted_data)
        decrypted_str = decrypted_data.decode()
        self.window_screentime = json.loads(decrypted_str)

    def data_parse(self):
        return self.window_screentime

    def process_data(self):
        model = WindowsModel(self.window_screentime)
        model.process_data()

    def window_grab(self):
        # This loop should run infinitely unless interrupted via keyboard
        while True:
            # This try and except blocks help in detecting the focused windows and their times whilst
            # handling the exceptions to keyboard interruption
            try:
                window = gw.getActiveWindow()
                if self.previous_window!= window:
                    if self.previous_window is not None:
                        self.end_time = time.time()
                        window_time = self.end_time - self.start_time
                        h, m, s = int(window_time // 3600), int(window_time % 3600) // 60, int(window_time % 60)
                        print("Time spent on ", self.previous_window.title, " is: ", f"{h:02}:{m:02}:{s:02}")
                        self.window_screentime.setdefault(str(self.today), {})[self.previous_window.title] = {
                            "time_spent": window_time,
                            "tabs": {}
                        }
                        self.save_data()

                    self.previous_window = window
                    self.start_time = time.time()

                time.sleep(1)

            except KeyboardInterrupt:
                if self.previous_window is not None:
                    self.end_time = time.time()
                    window_time = self.end_time - self.start_time
                    h, m, s = int(window_time // 3600), int(window_time % 3600) // 60, int(window_time % 60)
                    print("Time spent on ", self.previous_window.title, " is: ", f"{h:02}:{m:02}:{s:02}")
                    self.window_screentime.setdefault(str(self.today), {})[self.previous_window.title] = {
                        "time_spent": window_time,
                        "tabs": {}
                    }
                    print(self.window_screentime)
                self.save_data(interrupt=True)
                break


class WindowsModel:
    def __init__(self, data_dict):
        self.data_dict = data_dict

    def process_data(self):
        df = pd.DataFrame(self.data_dict)
        current_datetime = datetime.datetime.now()
        self.file_name = f"window_screentime_{current_datetime.strftime('%Y-%m-%d_%H-%M-%S')}.pkl"
        folder_path = 'user-data'
        file_path = os.path.join(folder_path, self.file_name)
        df.to_pickle(file_path)
       