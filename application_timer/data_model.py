'''
This file makes a Dataframe of the user's screen time for one log in session.
'''

# import pandas as pd
# import datetime
# from window_utils import WindowUtils

# class WindowsModel:
#     def __init__(self):
#         self.window_utils = WindowUtils()

#     def process_data(self):
#         data = self.window_utils.data_traverse()
#         df = pd.DataFrame(data)
#         current_datetime = datetime.datetime.now()
#         filename = f"windows_screentime_{current_datetime.strftime('%Y-%m-%d_%H-%M-%S')}.pkl"
#         df.to_pickle(filename)
#         print(f"Data saved to {filename}")

# model = WindowsModel
# WindowsModel.process_data()