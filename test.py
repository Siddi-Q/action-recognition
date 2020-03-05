import cv2

"""
Function Name: method1
Number of parameters: 0
List of parameters: n/a
Pre-condition: n/a
Post-condition: Captures frames from a video file and save them into a selected directory
List of sources:
        1. cv2.VideoCapture Overloaded Constructor: https://docs.opencv.org/master/d8/dfe/classcv_1_1VideoCapture.html#ac4107fb146a762454a8a87715d9b7c96
        2. cv2.VideoCapture get method:             https://docs.opencv.org/master/d8/dfe/classcv_1_1VideoCapture.html#aa6480e6972ef4c00d74814ec841a2939
        3. cv2.VideoCapture properties:             https://docs.opencv.org/master/d4/d15/group__videoio__flags__base.html#gaeb8dd9c89c10a5c63c139bf7c4f5704d
        4. cv2.VideoCapture read method:            https://docs.opencv.org/master/d8/dfe/classcv_1_1VideoCapture.html#a473055e77dd7faa4d26d686226b292c1
        5. cv2.imwrite method:                      https://docs.opencv.org/master/d4/da8/group__imgcodecs.html#gabbc7ef1aa2edfaa87772f1202d67e0ce
        6. cv2.VideoCapture release method:         https://docs.opencv.org/master/d8/dfe/classcv_1_1VideoCapture.html#afb4ab689e553ba2c8f0fec41b9344ae6
"""
def method1():
    videoFilePath = r"D:\ActionRecognition\UCF-101\Biking\v_Biking_g01_c01.avi" # Absolute path to a video file (.avi file)
    vidCap        = cv2.VideoCapture(videoFilePath)                             # Opens a video file for video capturing;(See source #1)
    numOfFrames   = int(vidCap.get(cv2.CAP_PROP_FRAME_COUNT))                   # Gets the number of frames in a video file; (See sources #2, #3)
    
    startFrameIndex     = 0                                                     # Frame index that we will start from 
    endFrameIndex       = numOfFrames - 1                                       # Frame index that we will end at
    captureRate         = 1                                                     # How frequently we will capture frames from a video
    capturedFrameNumber = 0                                                     # Number of frames that have been captured so far

    while(True):
        frameIndex = int(vidCap.get(cv2.CAP_PROP_POS_FRAMES))                   # Gets the (0-based) index of the frame that is going to be captured; (See source #3)
        retVal, frame = vidCap.read()                                           # Grabs and returns the next video frame, and returns False if no frames were grabbed (See source #4)
        
        if retVal:                                                              # Check to see if a frame was successfully grabbed
            if frameIndex >= startFrameIndex and \
               frameIndex <= endFrameIndex   and \
               int(frameIndex  - capturedFrameNumber*captureRate) == \
               startFrameIndex:                                                 # Check to see if a frame is within the frame range and captureRate
                   fileName = '../TestImages1/frame'    + \
                              str(capturedFrameNumber) + \
                              '.jpg'                                            # Create the filename that will be used to save the frame
                   print('Creating... ' + fileName + " " + str(frameIndex))
                   cv2.imwrite(fileName, frame)                                 # Save the frame as the given filename (See source #5)
                   capturedFrameNumber += 1                                     
        
        else:                                                                   # Frame was not grabbed signifying there are no more frames in the video left to be read
            break
        
    vidCap.release()                                                            # Closes the video file (See source #6)
    
"""
Function Name: method2
Number of parameters: 0
List of parameters: n/a
Pre-condition: n/a
Post-condition: Captures frames from a video file and saves them into a selected directory
List of sources:
        1. cv2.VideoCapture Overloaded Constructor: https://docs.opencv.org/master/d8/dfe/classcv_1_1VideoCapture.html#ac4107fb146a762454a8a87715d9b7c96
        2. cv2.VideoCapture get method:             https://docs.opencv.org/master/d8/dfe/classcv_1_1VideoCapture.html#aa6480e6972ef4c00d74814ec841a2939
        3. cv2.VideoCapture properties:             https://docs.opencv.org/master/d4/d15/group__videoio__flags__base.html#gaeb8dd9c89c10a5c63c139bf7c4f5704d
        4. cv2.VideoCapture set method:             https://docs.opencv.org/master/d8/dfe/classcv_1_1VideoCapture.html#a8c6d8c2d37505b5ca61ffd4bb54e9a7c
        5. cv2.VideoCapture read method:            https://docs.opencv.org/master/d8/dfe/classcv_1_1VideoCapture.html#a473055e77dd7faa4d26d686226b292c1
        6. cv2.imwrite method:                      https://docs.opencv.org/master/d4/da8/group__imgcodecs.html#gabbc7ef1aa2edfaa87772f1202d67e0ce
        7. cv2.VideoCapture release method:         https://docs.opencv.org/master/d8/dfe/classcv_1_1VideoCapture.html#afb4ab689e553ba2c8f0fec41b9344ae6
"""
def method2():
    videoFilePath = r"D:\ActionRecognition\UCF-101\Biking\v_Biking_g01_c01.avi" # Absolute path to a video file (.avi file)
    vidCap        = cv2.VideoCapture(videoFilePath)                             # Opens a video file for video capturing; (See source #1)
    numOfFrames   = int(vidCap.get(cv2.CAP_PROP_FRAME_COUNT))                   # Gets the number of frames in a video file; (See sources #2, #3)
    
    startFrameIndex     = 0                                                     # Frame index that we will start from 
    endFrameIndex       = numOfFrames - 1                                       # Frame index that we will end at
    captureRate         = 3                                                     # How frequently we will capture frames from a video
    capturedFrameNumber = 0                                                     # Number of frames that have been captured so far
    frameIndex          = startFrameIndex                                       # Frame index that we want to go to
    

    while(frameIndex <= endFrameIndex):
        vidCap.set(cv2.CAP_PROP_POS_FRAMES, frameIndex)                         # Sets the (0-based) index of the frame that is going to be captured (See source #4)
        retVal, frame = vidCap.read()                                           # Grabs and returns the next video frame, and returns False if no frames were grabbed (See source #5)
        
        if retVal:                                                              # Check to see if a frame was successfully grabbed
            fileName = '../TestImages2/frame'     + \
                        str(capturedFrameNumber) + \
                        '.jpg'                                                  # Create the path and filename that will be used to save the frame
            print('Creating... ' + fileName + " " + str(frameIndex))
            cv2.imwrite(fileName, frame)                                        # Save the frame as the given filename (See source #6)
            capturedFrameNumber += 1                                            
            frameIndex += captureRate                                           # Computes the index of the next frame that is to be captured
        else:
            break

    vidCap.release()                                                            # Closes the video file (See source #7)
    
if __name__ == '__main__':
    method2()
