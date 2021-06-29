from threading import local
import cv2
import tempfile
import numpy as np
from PIL import Image
import os

def parse_video(fileV, timestamps=[500, 2000, 4000]):

    myFrameNumber = timestamps
    cap = cv2.VideoCapture(fileV.name) #fig this shi out 

    fps = cap.get(cv2.CAP_PROP_FPS)
    width  = cap.get(cv2.CAP_PROP_FRAME_WIDTH)   # float
    height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)  # float

    # get total number of frames
    totalFrames = cap.get(cv2.CAP_PROP_FRAME_COUNT)

    requestedFrames = []
    for frameInd in myFrameNumber:

    # check for valid frame number
        if frameInd >= 0 & frameInd <= totalFrames:
            # set frame position
            cap.set(cv2.CAP_PROP_POS_FRAMES,frameInd)

        # requestedFrames = []
        numFrames = []
        while cap.isOpened():
            ret, frame = cap.read()
            if ret:
                numFrames.append(frame)

                # cv2.imshow("frame", frame)
                # if cv2.waitKey(25) == ord('q'):
                #     break
                if len(numFrames) == 25*10:
                    # print("haha")
                    requestedFrames.append(numFrames)
                    break 

    cap.release()

    namedtemp = tempfile.NamedTemporaryFile(delete=False)

    out = cv2.VideoWriter(namedtemp.name, cv2.VideoWriter_fourcc(*'DIVX'), fps, (int(width), int(height)))
    for segment in requestedFrames:
        for x in segment:
            # writing to a image array
            # print(x.shape)
            out.write(x)
    out.release()

    cv2.destroyAllWindows()

    return namedtemp


""""""

# myFrameNumber = [500, 2000, 4000]
# cap = cv2.VideoCapture("test.mp4")

# fps = cap.get(cv2.CAP_PROP_FPS)
# width  = cap.get(cv2.CAP_PROP_FRAME_WIDTH)   # float
# height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)  # float

# # get total number of frames
# totalFrames = cap.get(cv2.CAP_PROP_FRAME_COUNT)

# requestedFrames = []
# for frameInd in myFrameNumber:

# # check for valid frame number
#     if frameInd >= 0 & frameInd <= totalFrames:
#         # set frame position
#         cap.set(cv2.CAP_PROP_POS_FRAMES,frameInd)

#     # requestedFrames = []
#     numFrames = []
#     while cap.isOpened():
#         ret, frame = cap.read()
#         if ret:
#             numFrames.append(frame)

#             # cv2.imshow("frame", frame)
#             # if cv2.waitKey(25) == ord('q'):
#             #     break
#             if len(numFrames) == 25*10:
#                 # print("haha")
#                 requestedFrames.append(numFrames)
#                 break 

# cap.release()

# out = cv2.VideoWriter('video.avi',cv2.VideoWriter_fourcc(*'DIVX'), fps, (int(width), int(height)))
# for segment in requestedFrames:
#     for x in segment:
#         # writing to a image array
#         # print(x.shape)
#         out.write(x)

# # print(out)
# out.release()

# cv2.destroyAllWindows()
