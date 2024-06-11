#import pandas as pd
import pickle 

try:
    with open('focus_timer.pkl','rb') as f:
        print(pickle.load(f))
except FileNotFoundError:
    print("Empty")