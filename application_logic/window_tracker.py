import time
import pygetwindow as gw
import logging
import json
import os
from datetime import datetime, timedelta


# Set up tracking of active window
class WindowTracker:
    def __init__(self, data_handler):
        self.current_window = None
        self.start_time = None
        try:
            self.data = data_handler.load_data('data.pkl') or {}
        except Exception as e:
            logging.error(f"Error loading data from data.pkl: {e}")
            self.data = {}
        self.data_handler = data_handler
        self.browsers = ["Google Chrome", "Mozilla Firefox", "Microsoft Edge", "Opera"]

    # Simplify the window name. Removes redundant information.
    def simplify_name(self, window_name):
        parts = window_name.split(' - ')
        if len(parts) > 1:
            if any(browser in parts[-1] for browser in self.browsers):
                # It's a browser window, use the part before the last ' - '
                return parts[-2]
            else:
                # It's an application window, use the last part after the last ' - '
                return parts[-1]
        else:
            return window_name

    # Convert seconds to hh:mm:ss format
    @staticmethod
    def seconds_to_hhmmss(seconds):
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        seconds = int(seconds % 60)
        return f"{hours:02}:{minutes:02}:{seconds:02}"

    # Convert hh:mm:ss to seconds
    @staticmethod
    def _hhmmss_to_seconds(hhmmss):
        hours, minutes, seconds = map(int, hhmmss.split(':'))
        return hours * 3600 + minutes * 60 + seconds

    # Uses the getActiveWindow() function from pygetwindow to get the active window
    @staticmethod
    def get_active_window():
        return window.title if (window := gw.getActiveWindow()) else None

    # Update the time spent on the current window
    def update_time_spent(self):
        script_dir = os.path.dirname(__file__)
        assets_dir = os.path.join(script_dir, '../assets')
        data_dir = os.path.join(assets_dir, 'data')
        output_file = os.path.join(data_dir, 'output.json')

        try:
            with open(output_file, 'r') as f:
                old_data = json.load(f)

            if isinstance(old_data, dict):
                self.data.update(old_data)
            else:
                logging.warning(f"Invalid data format in {output_file}. Expected dictionary, got {type(old_data)}")

        except FileNotFoundError:
            logging.warning(f"File {output_file} not found.")

        except json.JSONDecodeError as e:
            logging.error(f"Error decoding JSON from {output_file}: {e}")

        current_time = time.time()
        if self.current_window:
            duration = current_time - self.start_time
            date_str = time.strftime("%Y-%m-%d")
            if date_str not in self.data:
                self.data[date_str] = {}

            window_title = self.current_window
            app_type = "Browser" if any(browser in window_title for browser in self.browsers) else "Application"

            if app_type == "Browser":
                # Extract browser name from window title
                browser_name = next((browser for browser in self.browsers if browser in window_title), None)
                tab_name = self.simplify_name(window_title)

                if browser_name:
                    if browser_name not in self.data[date_str]:
                        self.data[date_str][browser_name] = {
                            "app_type": app_type,
                            "time_spent": "00:00:00",
                            "tabs": {}
                        }

                    total_seconds_browser = self._hhmmss_to_seconds(
                        self.data[date_str][browser_name]["time_spent"]) + duration
                    self.data[date_str][browser_name]["time_spent"] = self.seconds_to_hhmmss(total_seconds_browser)

                    if tab_name not in self.data[date_str][browser_name]["tabs"]:
                        self.data[date_str][browser_name]["tabs"][tab_name] = "00:00:00"

                    tab_seconds = self._hhmmss_to_seconds(
                        self.data[date_str][browser_name]["tabs"][tab_name]) + duration
                    self.data[date_str][browser_name]["tabs"][tab_name] = self.seconds_to_hhmmss(tab_seconds)

                    with open(output_file, 'w') as f:
                        json.dump(self.data, f, indent=4)
                    logging.info(
                        f"Updated time spent on {browser_name} - Tab: {tab_name}: {self.data[date_str][browser_name]['tabs'][tab_name]}")
                else:
                    logging.warning(f"Browser name not recognized for window title: {window_title}")

            else:  # Application
                window_name = self.simplify_name(window_title)

                if window_name not in self.data[date_str]:
                    self.data[date_str][window_name] = {
                        "app_type": app_type,
                        "time_spent": "00:00:00",
                        "tabs": {}
                    }

                total_seconds_app = self._hhmmss_to_seconds(self.data[date_str][window_name]["time_spent"]) + duration
                self.data[date_str][window_name]["time_spent"] = self.seconds_to_hhmmss(total_seconds_app)

                with open(output_file, 'w') as f:
                    json.dump(self.data, f, indent=4)
                logging.info(f"Updated time spent on {window_name}: {self.data[date_str][window_name]['time_spent']}")

        else:
            logging.warning("Current window is None, cannot update time spent.")

    def clean_old_data(self, days_to_keep=30):
        current_date = datetime.now()
        cutoff_date = current_date - timedelta(days=days_to_keep)
        dates_to_delete = [date for date in self.data if datetime.strptime(date, "%Y-%m-%d") < cutoff_date]
        for date in dates_to_delete:
            del self.data[date]
        logging.info(f"Deleted data older than {cutoff_date.strftime('%Y-%m-%d')}")

    def to_json(self):
        return json.dumps(self.data, indent=4)

    def track(self):
        try:
            while True:
                active_window = self.get_active_window()
                if active_window != self.current_window:
                    self.update_time_spent()
                    self.clean_old_data()
                    logging.info(f"Switched to window: {active_window}")
                    self.current_window = active_window
                    self.start_time = time.time()
                time.sleep(1)
        except KeyboardInterrupt:
            self.update_time_spent()
            self.data_handler.save_data(self.data, 'data.pkl')
            logging.info("Application stopped, updated final time spent.")
            print(self.to_json())
