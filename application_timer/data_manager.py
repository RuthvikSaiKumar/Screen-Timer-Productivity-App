'''
This file is responsible for saving and loading data from the application.
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