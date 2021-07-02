import cv2
import tempfile
from random import random

def parse_video(fileV, features=[500, 2000, 4000]):

    fileV.seek(0)
    cap = cv2.VideoCapture(fileV.name) #fig this shi out 

    fps = cap.get(cv2.CAP_PROP_FPS)
    width  = cap.get(cv2.CAP_PROP_FRAME_WIDTH)   # float
    height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)  # float

    if features is parse_video.__defaults__[0]:
        print('default')
        timestamps = features
    else:
        timestamps = []
        for ind, lab in enumerate(features):
            if lab == 1:
                timestamps.append(int(ind*20*fps))
        print('passed in the call')

    # get total number of frames
    totalFrames = cap.get(cv2.CAP_PROP_FRAME_COUNT)

    suffix = ".mp4"
    prefix = ("johnny{}").format(round(random()*1000000))
    namedtemp = tempfile.NamedTemporaryFile(delete=False, prefix=prefix, suffix=suffix)
    namedtemp.seek(0)

    fourcc = cv2.VideoWriter_fourcc(*'avc1')
    out = cv2.VideoWriter(namedtemp.name, fourcc, fps, (int(width), int(height)))

    for frameInd in timestamps:

    # check for valid frame number
        if frameInd >= 0 & frameInd <= totalFrames:
            # set frame position
            cap.set(cv2.CAP_PROP_POS_FRAMES,frameInd)

        i = 0
        while cap.isOpened():
            ret, frame = cap.read()
            if ret:
                # print(i)
                i += 1
                out.write(frame)

                # cv2.imshow("frame", frame)
                # if cv2.waitKey(25) == ord('q'):
                #     break
                if i == int(fps*20):
                    break 

    cap.release()
    out.release()
    cv2.destroyAllWindows()

    return namedtemp


""""""
# fileV = "test.mp4"

# cap = cv2.VideoCapture(fileV) #fig this shi out 

# fps = cap.get(cv2.CAP_PROP_FPS)
# width  = cap.get(cv2.CAP_PROP_FRAME_WIDTH)   # float
# height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)  # float

# timestamps = [500, 2000, 4000]

# # get total number of frames
# totalFrames = cap.get(cv2.CAP_PROP_FRAME_COUNT)

# suffix = ".mp4"
# prefix = ("johnny{}").format(round(random()*1000000))
# namedtemp = tempfile.NamedTemporaryFile(delete=False, prefix=prefix, suffix=suffix)
# namedtemp.seek(0)

# fourcc = cv2.VideoWriter_fourcc(*'avc1')
# out = cv2.VideoWriter(namedtemp.name, fourcc, fps, (int(width), int(height)))

# for frameInd in timestamps:

# # check for valid frame number
#     if frameInd >= 0 & frameInd <= totalFrames:
#         # set frame position
#         cap.set(cv2.CAP_PROP_POS_FRAMES,frameInd)

#     i = 0
#     while cap.isOpened():
#         ret, frame = cap.read()
#         if ret:

#             i += 1
#             out.write(frame)

#             # cv2.imshow("frame", frame)
#             # if cv2.waitKey(25) == ord('q'):
#             #     break
#             if i == 25*20:
#                 break 

# cap.release()
# out.release()
# cv2.destroyAllWindows()

# print(namedtemp.name)

''''''

# from threading import Thread
# import cv2
# import time

# class VideoWriterWidget(object):

#     def __init__(self, video_file_name, timestamps=[500, 2000, 4000], src=0):
#         # Create a VideoCapture object
#         self.timestamps = timestamps
#         self.frame_name = str(src)
#         self.video_file_name = video_file_name
#         self.capture = cv2.VideoCapture(src)

#         # Default resolutions of the frame are obtained (system dependent)
#         self.fps = int(self.capture.get(cv2.CAP_PROP_FPS))
#         self.frame_width = int(self.capture.get(cv2.CAP_PROP_FRAME_WIDTH))
#         self.frame_height = int(self.capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
#         self.totalFrames = self.capture.get(cv2.CAP_PROP_FRAME_COUNT)

#         # Set up codec and output video settings
#         self.codec = cv2.VideoWriter_fourcc(*'avc1')
#         self.output_video = cv2.VideoWriter(self.video_file_name, self.codec, self.fps, (self.frame_width, self.frame_height))

#         # Start the thread to read frames from the video stream
#         self.thread = Thread(target=self.update, args=())
#         self.thread.daemon = True
#         self.thread.start()

#         # Start another thread to show/save frames
#         self.start_recording()
#         print('initialized {}'.format(self.video_file_name))

#     def update(self):
#         # Read the next frame from the stream in a different thread
#         while True:
#             if self.capture.isOpened():
#                 (self.status, self.frame) = self.capture.read()

#         # for frameInd in self.timestamps:

#         # # check for valid frame number
#         #     if frameInd >= 0 & frameInd <= self.totalFrames:
#         #         # set frame position
#         #         self.capture.set(cv2.CAP_PROP_POS_FRAMES,frameInd)

#         #     i = 0
#         #     while self.capture.isOpened():
#         #         (self.status, self.frame) = self.capture.read()

#         #         i += 1
#         #         if i == 25*20:
#         #             break 

#     def save_frame(self):
#         # Save obtained frame into video output file
#         self.output_video.write(self.frame)

#     def start_recording(self):
#         # Create another thread to save frames
#         def start_recording_thread():
#             while True:
#                 try:
#                     self.save_frame()
#                 except AttributeError:
#                     pass
#         self.recording_thread = Thread(target=start_recording_thread, args=())
#         self.recording_thread.daemon = True
#         self.recording_thread.start()

# if __name__ == '__main__':

#     fileV = "test.mp4"
#     suffix = ".mp4"
#     prefix = ("johnny{}").format(round(random()*1000000))
#     namedtemp = tempfile.NamedTemporaryFile(delete=False, prefix=prefix, suffix=suffix)
#     namedtemp.seek(0)

#     video_writer_widget1 = VideoWriterWidget(video_file_name=namedtemp.name, timestamps=[200, 2000, 3000], src=fileV)

#     # Since each video player is in its own thread, we need to keep the main thread alive.
#     # Keep spinning using time.sleep() so the background threads keep running
#     # Threads are set to daemon=True so they will automatically die 
#     # when the main thread dies
#     while True:
#         time.sleep(5)

''''''

# from threading import Thread
# import cv2
# import time
# from queue import Queue

# class VideoWriterWidget(object):
#     def __init__(self, video_file_name, src=0, queueSize=6000):
#         # Create a VideoCapture object
#         self.frame_name = str(src)
#         self.video_file_name = video_file_name
#         self.capture = cv2.VideoCapture(src)
#         self.frames = []

#         # Default resolutions of the frame are obtained (system dependent)
#         self.frame_width = int(self.capture.get(cv2.CAP_PROP_FRAME_WIDTH))
#         self.frame_height = int(self.capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
#         self.fps = self.capture.get(cv2.CAP_PROP_FPS)

#         # Set up codec and output video settings
#         self.codec = cv2.VideoWriter_fourcc(*'avc1')
#         self.output_video = cv2.VideoWriter(self.video_file_name, self.codec, self.fps, (self.frame_width, self.frame_height))

#         # Start the thread to read frames from the video stream
#         self.Q = Queue(maxsize=queueSize)

#     def start(self):
#         self.thread = Thread(target=self.update, args=())
#         self.thread.daemon = True
#         self.thread.start()

#         # Start another thread to show/save frames
#         self.start_recording()
#         return self

#     def update(self):
#         # Read the next frame from the stream in a different thread
#         while True:
#             if self.capture.isOpened():
#                  if not self.Q.full():
#                     (status, frame) = self.capture.read()
#                     self.Q.put((frame, status))
#                 # self.frames.append(self.frame)

#     def check_frame(self):
#         # Display frames in main program
#         # print(self.status)
#         print(self.Q.get()[1])
#         if self.Q.get()[1] == False:
#             self.capture.release()
#             self.output_video.release()
#             cv2.destroyAllWindows()
#             # print(len(self.frames))
#             print('initialized {}'.format(self.video_file_name))
#             exit(1)

#     def save_frame(self):
#         # Save obtained frame into video output file
#         self.output_video.write(self.Q.get()[0])

#     def start_recording(self):
#         # Create another thread to show/save frames
#         def start_recording_thread():
#             while True:
#                 try:
#                     self.check_frame()
#                     self.save_frame()
#                 except AttributeError:
#                     pass
#         self.recording_thread = Thread(target=start_recording_thread, args=())
#         self.recording_thread.daemon = False
#         self.recording_thread.start()

# if __name__ == '__main__':

#     suffix = ".mp4"
#     prefix = ("johnny{}").format(round(random()*1000000))
#     namedtemp = tempfile.NamedTemporaryFile(delete=False, prefix=prefix, suffix=suffix)
#     namedtemp.seek(0)
#     src1 = 'test.mp4'
#     video_writer_widget1 = VideoWriterWidget(namedtemp.name, src1).start()

    # Since each video player is in its own thread, we need to keep the main thread alive.
    # Keep spinning using time.sleep() so the background threads keep running
    # Threads are set to daemon=True so they will automatically die 
    # when the main thread dies
    # while True:
    #     time.sleep(5)

''''''

# from threading import Thread
# import time
# import cv2
# from queue import Queue

# class FileVideoStream:
    
#     def __init__(self, source, timestamps=[500, 2000, 4000], queueSize=128):
# 		# initialize the file video stream along with the boolean
# 		# used to indicate if the thread should be stopped or not
#         self.stream = cv2.VideoCapture(source)
#         self.stopped = False
#         self.timestamps = timestamps

#         self.fps = self.stream.get(cv2.CAP_PROP_FPS)
#         self.width  = self.stream.get(cv2.CAP_PROP_FRAME_WIDTH)   # float
#         self.height = self.stream.get(cv2.CAP_PROP_FRAME_HEIGHT)  # float
#         # initialize the queue used to store frames read from
#         # the video file
#         self.Q = Queue(maxsize=queueSize)
        
#     def start(self):
# 		# start a thread to read frames from the file video stream
#         t = Thread(target=self.update, args=())
#         t.daemon = True
#         t.start()  
#         return self

#     def update(self):
#         # keep looping infinitely
#         for stamp in self.timestamps:

#             i = 0
#             self.stream.set(cv2.CAP_PROP_POS_FRAMES,stamp)

#             while True:
#                 # if the thread indicator variable is set, stop the
#                 # thread
#                 if self.stopped:
#                     return
#                 # otherwise, ensure the queue has room in it
#                 if not self.Q.full():
#                     # read the next frame from the file
#                     (grabbed, frame) = self.stream.read()
#                     # if the `grabbed` boolean is `False`, then we have
#                     # reached the end of the video file
#                     if not grabbed:
#                         self.stop()
#                         return

#                     if i == int(self.fps*20):
#                         break
                    
#                     # add the frame to the queue
#                     i += 1
#                     self.Q.put(frame)

#     def read(self):
#         # return next frame in the queue
#         return self.Q.get()

#     def more(self):
#         # return True if there are still frames in the queue
#         return self.Q.qsize() > 0

#     def stop(self):
#         # indicate that the thread should be stopped
#         self.stopped = True


# # start the file video stream thread and allow the buffer to
# # start to fill
# print("[INFO] starting video file thread...")
# fvs = FileVideoStream(source='test.mp4').start()
# time.sleep(1.0)

# # loop over frames from the video file stream

# fourcc = cv2.VideoWriter_fourcc(*'avc1')
# out = cv2.VideoWriter('test1.mp4', fourcc, fvs.fps, (int(fvs.width), int(fvs.height)))

# while fvs.more():

#     frame = fvs.read()
#     out.write(frame)

# 	# cv2.imshow("Frame", frame)
# 	# cv2.waitKey(1)


# # do a bit of cleanup
# out.release()
# cv2.destroyAllWindows()
# fvs.stop()