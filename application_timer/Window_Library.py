import pygetwindow as gw
import time
from datetime import datetime

# Dictionary to keep track of focused windows and their active time
focus_times = {}


def get_active_window():
    try:
        window = gw.getActiveWindow()
        if window is not None:
            return window.title
    except Exception as e:
        print(f"Error getting active window: {e}")
    return None


def main():
    previous_window = None
    start_time = None

    while True:
        current_window = get_active_window()

        if current_window != previous_window:
            end_time = datetime.now()

            if previous_window:
                duration = (end_time - start_time).total_seconds()
                if previous_window in focus_times:
                    focus_times[previous_window] += duration
                else:
                    focus_times[previous_window] = duration
                print(f"Window '{previous_window}' was in focus for {duration:.2f} seconds.")

            previous_window = current_window
            start_time = end_time

        time.sleep(1)  # Check every second


if __name__ == "__main__":
    main()
