from window_tracker import WindowTracker
from data_handler import DataHandler
import logging
from cryptography.fernet import Fernet

class ScreenTimeApp:
    def __init__(self):
        self.tracker = WindowTracker()
        self.data_handler = DataHandler(Fernet.generate_key())

    def run(self):
        try:
            self.tracker.track()
        except KeyboardInterrupt:
            self.tracker.update_time_spent()
            self.data_handler.save_data(self.tracker.data, 'data.pkl')

    def read_data(self, filename):
        return self.data_handler.load_data(filename)

if __name__ == "__main__":
    import logger
    app = ScreenTimeApp()
    app.run()
