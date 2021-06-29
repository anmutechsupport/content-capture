# import pickle
import pandas as pd
import numpy as np
import processing

# with open("bapeeg.pkl", "rb") as infile:
#     eeg = pickle.load(infile)

# with open("timestamps.pkl", "rb") as infile:
#     timestamps = pickle.load(infile)

def predict(eeg, timestamps):

    delay = int(((timestamps["startVideo"] - timestamps["startStream"])/1000)*256)
    # print(delay)

    fs = 256
    # order of array [af7, af8, tp9, tp10]
    input_arr = np.array([x["raw"][delay:] for x in eeg[:4]]).T
    # print(input_arr.shape)

    features = processing.PSD(input_arr, fs, filtering=True)

    normalized = processing.descriptive_stats(features)
    # print(normalized.shape)

    model = processing.create_modelFinal()

    predictions = model.predict(normalized)

    return predictions