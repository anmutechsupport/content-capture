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
import csv
import tempfile
import os
import pyautogui
from muselsl import *

if __name__ == "__main__":
    
    samplerate = 256
    # while True:
    #     length = input('how long is the video') #20
    #     name = input("what is the file name")
    #     subject = input("what subject")
    #     fileN = os.path.join(os.getcwd(), "%s%s.csv" % (name, subject))
    #     break
    
    # tic = time.perf_counter()
    # while True:

    #     if time.perf_counter() - tic > 5:
            
    #         # Note: an existing Muse LSL stream is required
    #         pyautogui.press('space')
    #         record(int(length), filename = fileN, dejitter=True)

    #         # Note: Recording is synchronous, so code here will not execute until the stream has been closed
    #         print('Recording has ended')
    #         break

    temp_file = tempfile.NamedTemporaryFile(delete=False)
    fileName = 'wowe1.csv'

    with open(fileName, "r") as csvfile, temp_file:
        reader = csv.DictReader(csvfile)
        # fieldnames = ['timestamps', 'TP9', 'AF7', 'TP10', 'Interest']
        big_list = [row for row in reader]

        colnames, len_file = list(big_list[0].keys()), len(big_list)+1
        colnames.append("Interest")
        print(colnames)
 
        writer = csv.DictWriter(temp_file, fieldnames=colnames)
        # writer.writeheader()

        interval_len = int(input("how long are the intervals"))

        for interval in range(int(len_file/(interval_len*samplerate))):
            interest = input(("between {} to {} seconds, how much were interested on a scale from 1-5?").format(interval*interval_len, interval*interval_len+interval_len))
            for row in big_list[]
 
        # for row in reader:
        #     print(row)