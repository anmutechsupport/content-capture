import pickle
import pandas as pd
import numpy as np

with open("bapeeg.pkl", "rb") as infile:
    eeg = pickle.load(infile)

# order of array [af7, af8, tp9, tp10]
print(eeg[0]["raw"])