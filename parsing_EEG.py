import pickle
import pandas as pd
import numpy as np
import processing

with open("bapeeg.pkl", "rb") as infile:
    eeg = pickle.load(infile)

fs = 256
# order of array [af7, af8, tp9, tp10]
input_arr = np.array([x["raw"] for x in eeg[:4]]).T
# print(input_arr.shape)

features = processing.PSD(input_arr, fs, filtering=True)

normalized = processing.descriptive_stats(features)
print(normalized.shape)

model = processing.create_modelFinal()

predictions = model.predict(normalized)
print(predictions)