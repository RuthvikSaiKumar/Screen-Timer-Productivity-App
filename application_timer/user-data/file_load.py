'''
This file is just for checking if the data is stored correctly 
'''

import pickle

with open('window_screentime_cache.pkl', "rb") as f:
    ok = pickle.load(f) 

print(ok)