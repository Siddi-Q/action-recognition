import cv2

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
def extractFrames(videoFilePath, videoFileName, destinationPath, maxNumOfFrames, captureRate):
    vidCap        = cv2.VideoCapture(videoFilePath)                             # Opens a video file for video capturing; (See source #1)
    numOfFrames   = int(vidCap.get(cv2.CAP_PROP_FRAME_COUNT))                   # Gets the number of frames in a video file; (See sources #2, #3)

    midFrameIndex    = numOfFrames // 2
    deviationFromMid = (maxNumOfFrames * captureRate) // 2
    
    startFrameIndex = max(0, midFrameIndex - deviationFromMid)
    endFrameIndex   = min(midFrameIndex + deviationFromMid, numOfFrames - 1)
    
    capturedFrameNumber = 0                                                     # Number of frames that have been captured so far
    frameIndex          = startFrameIndex                                       # Frame index that we want to go to

    while(frameIndex <= endFrameIndex and capturedFrameNumber < maxNumOfFrames):
        vidCap.set(cv2.CAP_PROP_POS_FRAMES, frameIndex)                         # Sets the (0-based) index of the frame that is going to be captured (See source #4)
        retVal, frame = vidCap.read()                                           # Grabs and returns the next video frame, and returns False if no frames were grabbed (See source #5)
        
        if retVal:                                                              # Check to see if a frame was successfully grabbed
            #change to "\\" for local windows directory or "/" for GCS/Mac/Linux
            #fileName = destinationPath + "\\"    + \
            fileName = destinationPath + "/"    + \
                       videoFileName   + "_"    + \
                       str('%04d' % capturedFrameNumber) + \
                        '.jpg'                                                  # Create the path and filename that will be used to save the frame
            print('Creating... ' + fileName + " " + str(frameIndex))
            cv2.imwrite(fileName, frame)                                        # Save the frame as the given filename (See source #6)
            capturedFrameNumber += 1                                            
            frameIndex += captureRate                                           # Computes the index of the next frame that is to be captured
        else:
            break

    vidCap.release()                                                            # Closes the video file (See source #7)


def extractAllFrames(videoFilePath, videoFileName, destinationPath):
    vidCap        = cv2.VideoCapture(videoFilePath)                             # Opens a video file for video capturing; (See source #1)
    numOfFrames   = int(vidCap.get(cv2.CAP_PROP_FRAME_COUNT))                   # Gets the number of frames in a video file; (See sources #2, #3)
    numOfDigits   = len(str(numOfFrames))
    padding       = f'%0{numOfDigits}d'

    
    capturedFrameNumber = 0                                                     # Number of frames that have been captured so far
    while True:
        frameIndex = int(vidCap.get(cv2.CAP_PROP_POS_FRAMES))                   # Gets the (0-based) index of the frame that is going to be captured; (See source #3)
        retVal, frame = vidCap.read()                                           # Grabs and returns the next video frame, and returns False if no frames were grabbed (See source #4)

        if retVal:                                                              # Check to see if a frame was successfully grabbed
            fileName = destinationPath + "/" + \
                       videoFileName   + "_"  + \
                       str(padding % capturedFrameNumber) + \
                        '.jpg'                                                  # Create the path and filename that will be used to save the frame
            print('Creating... ' + fileName + " " + str(frameIndex))
            cv2.imwrite(fileName, frame)                                        # Save the frame as the given filename (See source #6)
            capturedFrameNumber += 1
        else:
            break
            
    vidCap.release()                                                            # Closes the video file (See source #7)    
    
if __name__ == '__main__':
##    method2()
    pass
