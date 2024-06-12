'''
This file is responsible for saving and loading data from the application.
'''

'''
import pandas as pd
import pickle
import datetime
import os
import glob

class Datalogger:
    def __init__(self):
        self.focus_times_df = pd.DataFrame(columns=['Window', 'Duration'])
        self.previous_window = None
        self.start_time = None
    
    def get_active_window(self):
        try:
            window = gw.getActiveWindow()
            if window is not None:
                return window.title
        except Exception as e:
            print(f"Error getting active window: {e}")
        return None
    
    def save_data(self):
        # This function generates a unique pickel file name based on the current date and time
        file_name = f'focus_timer_{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.pkl'
        with open(file_name, 'wb') as f:
            pickle.dump(self.focus_times_df, f)
        
    def load_data(self):
        try:
            # Open the most recent pickle file
            files = glob.glob('focus_timer_*.pkl')
            if files:
                latest_file = max(files, key=os.path.getctime)
                with open(latest_file,'rb') as f:
                    return pickle.load(f)
        except FileNotFoundError:
            return pd.DataFrame(columns=['Window', 'Duration'])
            '''

import pickle

class DataManager:
    def __init__(self, data_file):
        self.data_file = data_file

    def load_data(self):
        with open(self.data_file, 'rb') as f:
            data = pickle.load(f)
        return data

    def save_data(self, data):
        with open(self.data_file, 'wb') as f:
            pickle.dump(data, f)