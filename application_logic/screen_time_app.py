from window_tracker import WindowTracker
from data_handler import DataHandler
import logging
from cryptography.fernet import Fernet

class ScreenTimeApp:
    def __init__(self):
        # Initialize DataHandler with a generated key
        self.data_handler = DataHandler(Fernet.generate_key())
        
        # Pass data_handler to WindowTracker during initialization
        self.tracker = WindowTracker(self.data_handler)

    def run(self):
        try:
            self.tracker.track()
        except KeyboardInterrupt:
            self.tracker.update_time_spent()
            self.data_handler.save_data(self.tracker.data)

    def read_data(self, filename):
        return self.data_handler.load_data(filename)

if __name__ == "__main__":
    import logger
    app = ScreenTimeApp()
    app.run()
