import time
import math
import numpy as np
import pandas as pd
import matplotlib
import matplotlib.animation
import matplotlib.pyplot as plt
import scipy
from matplotlib.figure import Figure
from scipy.signal import filtfilt
import brainflow
from brainflow.board_shim import BoardShim, BrainFlowInputParams, LogLevels, BoardIds
from brainflow.data_filter import DetrendOperations, DataFilter, FilterTypes, AggOperations, WindowFunctions
import scipy.signal as sig
class CytonStream(object):
    def __init__(self):
        #############1 Create variables for holding the stream
        self.display_window = DataFilter.get_nearest_power_of_two(500) # Attribute, DataFilter class contains methods for signal processing
        self.data = [0]*self.display_window #Create an array of a bunch of 0 values of display_window
        #############2 Connect to the Cyton Board through brainflow (This will change depending on your board)
        BoardShim.enable_dev_board_logger () 
        params = BrainFlowInputParams() 
        board_id = BoardIds.MUSE_2_BLED_BOARD 
        self.sample_rate = BoardShim.get_sampling_rate(board_id)
        self.board_channel = BoardShim.get_eeg_channels(board_id)[0]
        params.serial_port = 'COM3' # Port
        board_id = 22 #BoardIds.CYTON_BOARD(0)
        board = BoardShim(board_id, params) # Board Stream Object
        board.prepare_session() # Prepare the session
        board.start_stream() #Create streaming thread 
        self.board = board
        #############3 Create matplotlib plots
        #self.figure = Figure() ???
        self.fig, axes = plt.subplots(2, 1, figsize=(11,7)) #2 or 1?
        prop_cycle = plt.rcParams['axes.prop_cycle'] #CHANGED
        colors = prop_cycle.by_key()['color']
        # Set the Axes Instance
        # Add brainflow waveform and FFT
        self.wave_ax = axes[0] #Location 1
        # Set titles
        self.wave_ax.set_title("Cyton Waveform") #Title
        # Create line objects whose data we update in the animation
        self.lines = [x[0] for x in
                         [ax.plot(self.data, self.data, color=colors[i]) for i,ax in enumerate(axes)]]
        # Start animation
        self.fig.tight_layout() #Creates spaces between titles :)
        self.ani = matplotlib.animation.FuncAnimation(self.fig, self.updateFig,
                                                 interval=5, blit=True) #Animation
        # Create list of objects that get animated
        self.ani_objects = [self.wave_ax]
    ################################################# Animation helpers
    def updateVars(self): #THIS IS WHERE YOU PICK THE FIRST CHANNEL
        ### What's the latest?? # Using the first channel
        all_data = self.board.get_current_board_data(self.display_window)
        self.curData = all_data[self.board_channel, :]
        if (len(self.curData) < self.display_window):
            self.data = self.curData
            return
    ##################### Filtering # USE BRAINFLOW -> GOTTA CHANGE ALL OF THIS 
    def filtering(self, data): #Use Brainflow but HOW???
        # Notch
        b, a = sig.iirnotch(60, 30, fs=self.sample_rate)
        data = sig.filtfilt(b, a, data)
        # Band pass
        passband = [6, 75]
        stopband = [5, 95]
        sos = sig.iirdesign(passband, stopband, 1, 40, fs=self.sample_rate,
                            output='sos')
        data = sig.sosfiltfilt(sos, data)
        return data
    ################################## Animation function
    def updateFig(self, *args):
        now = time.time()
        # Update data from the brainflow
        self.updateVars()
        if (len(self.data) == self.display_window):
            ### Update plots with new data
           self.lines[0].set_data(self.waveX, self.data)
        else: # Set filler waveform data if the buffer hasn't filled yet
            self.lines[0].set_data(list(range(len(self.data))), self.data)
        ## Reset limits of the waveform plot so it looks nice
        self.wave_ax.relim()
        self.wave_ax.autoscale_view(tight=True)
        self.propagateChanges()
        return self.ani_objects
    def propagateChanges(self):
        self.fig.stale = True #'stale' and needs to be re-drawn for the output to match the internal state
        self.fig.canvas.draw() # Redraw the current figure. This is used to update a figure that has been altered, but not automatically re-drawn
        self.fig.canvas.flush_events() # Flush the GUI events for the figure.
global stream
'''
i = 0
while i < 5:
    print("starting loop")
    i += 1
    '''
try:
    stream = CytonStream()
    plt.show()
#except KeyboardInterrupt: # Dont understand incentive behind this???
   # print('\nKeyboard interrupted, ending program')
  # stream.board.release_session()
except Exception as e:
    print("other exception,", e)
    time.sleep(1)