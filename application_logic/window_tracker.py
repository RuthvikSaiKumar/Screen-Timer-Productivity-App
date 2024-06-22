'''
This module contains the WindowTracker class that is responsible for tracking the active window and the time spent on it.
'''

import time
import pygetwindow as gw
import logging
from datetime import datetime, timedelta

# Set up tracking of active window
class WindowTracker:
    def __init__(self):
        self.current_window = None
        self.start_time = None
        self.data = {}

    # Simplify the window name. Removes redundant information.
    @staticmethod
    def simplify_name(window_name):
        if ' - ' in window_name:
            window_name = window_name.split(' - ')[-1]
        return window_name

    # Convert seconds to hh:mm:ss format
    @staticmethod
    def seconds_to_hhmmss(seconds):
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        seconds = int(seconds % 60)
        return f"{hours:02}:{minutes:02}:{seconds:02}"

    # Uses the getActiveWindow() function from pygetwindow to get the active window
    def get_active_window(self):
        window = gw.getActiveWindow()
        if window:
            return self.simplify_name(window.title)
        return None
    
    # Update the time spent on the current window
    def update_time_spent(self):
        current_time = time.time()
        if self.current_window:
            duration = current_time - self.start_time
            date_str = time.strftime("%Y-%m-%d")
            if date_str not in self.data:
                self.data[date_str] = {}
            if self.current_window not in self.data[date_str]:
                self.data[date_str][self.current_window] = {
                    "app_type": "Application",
                    "time_spent": "00:00:00",
                    "tabs": {}
                }
            total_seconds = self._hhmmss_to_seconds(self.data[date_str][self.current_window]["time_spent"]) + duration
            self.data[date_str][self.current_window]["time_spent"] = self.seconds_to_hhmmss(total_seconds)
            logging.info(f"Updated time spent on {self.current_window}: {self.data[date_str][self.current_window]['time_spent']}")

    @staticmethod
    def _hhmmss_to_seconds(hhmmss):
        hours, minutes, seconds = map(int, hhmmss.split(':'))
        return hours * 3600 + minutes * 60 + seconds

    def track(self):
        while True:
            active_window = self.get_active_window()
            if active_window != self.current_window:
                self.update_time_spent()
                logging.info(f"Switched to window: {active_window}")
                self.current_window = active_window
                self.start_time = time.time()
            time.sleep(1)
                
    
    def clean_old_data(self, days_to_keep=30): # Alter the days_to_keep parameter to change the number of days to keep data for
        current_date = datetime.now()
        cutoff_date = current_date - timedelta(days=days_to_keep)
        dates_to_delete = [date for date in self.data if datetime.strptime(date, "%Y-%m-%d") < cutoff_date]
        for date in dates_to_delete:
            del self.data[date]
        logging.info(f"Deleted data older than {cutoff_date.strftime('%Y-%m-%d')}")

    def track(self):
        while True:
            active_window = self.get_active_window()
            if active_window != self.current_window:
                self.update_time_spent()
                self.clean_old_data()  # Clean old data during tracking
                logging.info(f"Switched to window: {active_window}")
                self.current_window = active_window
                self.start_time = time.time()
            time.sleep(1)
