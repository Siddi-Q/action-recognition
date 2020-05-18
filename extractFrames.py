import cv2
import pathlib

"""
Documentation:
- cv2
    1. get(), read(), release(), set(), VideoCapture()
        - https://docs.opencv.org/master/d8/dfe/classcv_1_1VideoCapture.html
    2. imwrite()
        - https://docs.opencv.org/master/d4/da8/group__imgcodecs.html#gabbc7ef1aa2edfaa87772f1202d67e0ce
    3. VideoCapture properties
        - https://docs.opencv.org/master/d4/d15/group__videoio__flags__base.html#gaeb8dd9c89c10a5c63c139bf7c4f5704d
- pathlib
    1. Path(), /
        - https://docs.python.org/3/library/pathlib.html
"""

"""
Function Name: extractFrames
Number of parameters: 5
List of parameters:
    1. videoFilePath   | string | Path to a video.
    2. videoFileName   | string | Name of a video.
    3. destinationPath | string | Path to save the frames.
    4. maxNumOfFrames  | int    | Maximum number of frames to be extracted.
    5. extractRate     | int    | The frequency at which frames are to be extracted. (E.g. 3 => Extract every THIRD frame)
Pre-condition:
    1. 'videoFilePath' exists and points to a video file.
    2. 'destinationPath' exits.
    3. 'extractRate' is a non-negative integer.
Post-condition:
    1. Extract 'maxNumOfFrames' frames from 'videoFilePath' and save them into 'destinationPath'.
    2. Nothing is returned.
"""
def extractFrames(videoFilePath, videoFileName, destinationPath, maxNumOfFrames, extractRate):
    # Open a video file for video capturing
    vidCap        = cv2.VideoCapture(videoFilePath)
    # Get the number of frames in a video file
    numOfFrames   = int(vidCap.get(cv2.CAP_PROP_FRAME_COUNT))

    midFrameIndex    = numOfFrames // 2
    deviationFromMid = (maxNumOfFrames * extractRate) // 2
    
    startFrameIndex = max(0, midFrameIndex - deviationFromMid)
    endFrameIndex   = min(midFrameIndex + deviationFromMid, numOfFrames - 1)

    # Number of frames that have been captured so far
    capturedFrameNumber = 0
    # Frame index that we want to go to
    frameIndex          = startFrameIndex

    padding = '%04d'
    while(frameIndex <= endFrameIndex and capturedFrameNumber < maxNumOfFrames):
        # Set the (0-based) index of the frame that is going to be captured
        vidCap.set(cv2.CAP_PROP_POS_FRAMES, frameIndex)
        # Grab and return the next video frame, or return False if no frame was grabbed
        retVal, frame = vidCap.read()

        # Check to see if a frame was successfully grabbed
        if retVal:
            # Create the file path that will be used to save the frame
            filePath = str(pathlib.Path(destinationPath)/f'{videoFileName}_{str(padding % capturedFrameNumber)}.jpg')
            print(f'Creating frame at: {filePath}. Index of frame is: {frameIndex}')
            # Save the frame
            cv2.imwrite(filePath, frame)
            capturedFrameNumber += 1
            # Compute the index of the next frame that is to be captured
            frameIndex += extractRate
        else:
            break

    # Close the video file
    vidCap.release()


"""
Function Name: extractAllFrames
Number of parameters: 3
List of parameters:
    1. videoFilePath   | string | Path to a video.
    2. videoFileName   | string | Name of a video.
    3. destinationPath | string | Path to save the frames.
Pre-condition:
    1. 'videoFilePath' exists and points to a video file.
    2. 'destinationPath' exits.
Post-condition:
    1. Capture all frames from 'videoFilePath' and save them into 'destinationPath'.
    2. Nothing is returned.
"""
def extractAllFrames(videoFilePath, videoFileName, destinationPath):
    # Open a video file for video capturing
    vidCap        = cv2.VideoCapture(videoFilePath)
    # Get the number of frames in a video file
    numOfFrames   = int(vidCap.get(cv2.CAP_PROP_FRAME_COUNT))
    numOfDigits   = len(str(numOfFrames))
    padding       = f'%0{numOfDigits}d'

    # Number of frames that have been captured so far
    capturedFrameNumber = 0
    while True:
        # Get the (0-based) index of the frame that is going to be captured
        frameIndex = int(vidCap.get(cv2.CAP_PROP_POS_FRAMES))
        # Grab and return the next video frame, or return False if no frame was grabbed
        retVal, frame = vidCap.read()
        
        # Check to see if a frame was successfully grabbed
        if retVal:
            # Create the file path that will be used to save the frame
            filePath = str(pathlib.Path(destinationPath)/f'{videoFileName}_{str(padding % capturedFrameNumber)}.jpg')
            print(f'Creating frame at: {filePath}. Index of frame is: {frameIndex}')
            # Save the frame
            cv2.imwrite(filePath, frame)
            capturedFrameNumber += 1
        else:
            break

    # Close the video file
    vidCap.release()
