import cv2
import tempfile
import numpy as np

# video = cv2.VideoCapture('test.mp4')

# if (video.isOpened()== False):
#   print("Error opening video stream or file")

# num_frames = []
# while video.isOpened():
#     ret, frame = video.read()
#     if ret:
#         num_frames.append('go')
#     # For testing purpose
#         # num_frames.append(frame)
#         # cv2.imshow("frame", frame)
#         # if cv2.waitKey(25) == ord('q'):
#         #     print("nice")
#         #     break
#     ##############################
#         temp_file = tempfile.TemporaryFile()
#         np.save(temp_file, frame)
#         temp_file.seek(0)
#         # upload_to_some_where(temp_file.read())
#         temp_file.close()
#     else:
#         break

# print(len(num_frames))

# video.release()
# cv2.destroyAllWindows()

""""""

myFrameNumber = [250, 2000, 4000]
cap = cv2.VideoCapture("test.mp4")

# get total number of frames
totalFrames = cap.get(cv2.CAP_PROP_FRAME_COUNT)

for frame in myFrameNumber:

    # check for valid frame number
    if myFrameNumber >= 0 & myFrameNumber <= totalFrames:
        # set frame position
        cap.set(cv2.CAP_PROP_POS_FRAMES,myFrameNumber)

    while True:
        ret, frame = cap.read()
        if ret:   
            cv2.imshow("Video", frame)
            if cv2.waitKey(20) & 0xFF == ord('q'):
                break

cv2.destroyAllWindows()
