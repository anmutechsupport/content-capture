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


# """"""
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

# from threading import Thread
# import cv2
# import time

# class VideoWriterWidget(object):

#     def __init__(self, video_file_name, timestamps, src=0):
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

