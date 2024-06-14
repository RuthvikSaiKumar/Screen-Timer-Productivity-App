'''
This file makes a Dataframe of the user's screen time for one log in session.
'''

import pandas as pd

class DataModel:
    def __init__(self, data):
        self.data = data

    def create_dataframe(self):
        df = pd.DataFrame(self.data)
        return df

    def get_data(self):
        return self.data