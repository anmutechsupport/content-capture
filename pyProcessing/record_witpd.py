"""
Record from a Stream
This example shows how to record data from an existing Muse LSL stream
"""
from muselsl import record
from muselsl.stream import find_muse
import time
"""
Starting a Stream
This example shows how to search for available Muses and
create a new stream
"""
import pandas as pd
import os
import pyautogui
from muselsl import *

if __name__ == "__main__":
  
    while True:
        length = input('how long is the video') #20
        name = input("what is the file name")
        subject = input("what subject")
        fileN = os.path.join(os.getcwd(), "%s%s.csv" % (name, subject))
        break
    tic = time.perf_counter()
    while True:

        if time.perf_counter() - tic > 10:
            # Note: an existing Muse LSL stream is required
            pyautogui.press('space')
            record(int(length), filename = fileN, dejitter=True)
 
            # Note: Recording is synchronous, so code here will not execute until the stream has been closed
            print('Recording has ended')
            break
        else:
            print(time.perf_counter() - tic)

    # fileN =  "testest1"
    samplerate = 256
    skip = 4

    df = pd.read_csv(fileN)
    df = df.drop(labels=range(samplerate*skip), axis=0)

    file_len = len(df)
    Type_new = pd.Series([])

    interval_len = int(input("how long are the intervals"))

    for interval in range(int(file_len/(interval_len*samplerate))): #looping over the # of intervals in the dataset
        interest = input(("between {} to {} seconds, how much were  you interested on a scale from 1-5?").format(interval*interval_len+skip, interval*interval_len+interval_len+skip)) #asks for interest between an interval
        for row in range(interval*interval_len*samplerate, interval*interval_len*samplerate+interval_len*samplerate): #loops over each row in that interval
            # print(row)
            Type_new[row] = interest

    
    # print(Type_new.shape)

    df.insert(5, "Interest", Type_new)
    df.to_csv(("{}processed.csv").format(fileN), index=False)
    
