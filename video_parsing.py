import cv2
import tempfile

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

    requestedFrames = []
    for frameInd in timestamps:

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
                if len(numFrames) == 25*20:
                    # print("haha")
                    requestedFrames.append(numFrames)
                    break 

    cap.release()

    namedtemp = tempfile.NamedTemporaryFile(delete=False, suffix='.avi')
    namedtemp.seek(0)

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
