''' 
This file is the sub-main file within the application_timer directory. 
It communicates between all the other files within this directory.
'''

'''
import pygetwindow as gw
import time
from datetime import datetime
import pickle
import pandas as pd

# Create an empty DataFrame to store the data
focus_times_df = pd.DataFrame(columns=['Window', 'Duration'])

def get_active_window():
    try:
        window = gw.getActiveWindow()
        if window is not None:
            return window.title
    except Exception as e:
        print(f"Error getting active window: {e}")
    return None

def save_data():
    with open('focus_timer.pkl', 'wb') as f:
        pickle.dump(focus_times_df, f)

def load_data():
    try:
        with open('focus_timer.pkl','rb') as f:
            return pickle.load(f)
    except FileNotFoundError:
        return pd.DataFrame(columns=['Window', 'Duration'])

def main():
    global focus_times_df
    focus_times_df = load_data()

    previous_window = None
    start_time = None

    try:
        while True:
            current_window = get_active_window()
            
            if current_window!= previous_window: 
                end_time = datetime.now()
                
                if previous_window:
                    duration = (end_time - start_time).total_seconds()
                    new_row = pd.DataFrame({'Window': [previous_window], 'Duration': [duration]})
                    focus_times_df = pd.concat([focus_times_df, new_row], ignore_index=True)
                    print(f"Window '{previous_window}' was in focus for {duration:.2f} seconds.")
                
                previous_window = current_window 
                start_time = end_time 

            elif current_window == previous_window:
                # Check if the window is already in the DataFrame
                if current_window in focus_times_df['Window'].values:
                    # Update the duration for the current window
                    focus_times_df.loc[focus_times_df['Window'] == current_window, 'Duration'] += 1
                else:
                    # Add a new row to the DataFrame with an initial duration of 1 second
                    new_row = pd.DataFrame({'Window': [current_window], 'Duration': [1]})
                    focus_times_df = pd.concat([focus_times_df, new_row], ignore_index=True)

            time.sleep(1)  # Check every second
            if time.time() % 600 == 0:
                save_data()
    except KeyboardInterrupt:
        print("Exiting...")
        save_data()  
        # print the pkl file data
        print(focus_times_df)
        exit(0)

if __name__ == "__main__":
    main()
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