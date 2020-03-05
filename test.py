import cv2
import os

def func4():
    cam = cv2.VideoCapture(r"D:\ActionRecognition\UCF-101\Biking\v_Biking_g01_c01.avi")

    numOfFrames = int(cam.get(cv2.CAP_PROP_FRAME_COUNT))
    frameRate = int(cam.get(cv2.CAP_PROP_FPS))

    startFrameIndex = int(numOfFrames / 2) - 20
    endFrameIndex = int(numOfFrames / 2) + 20
    captureRate = 5
    capturedFrameIndex = 0

    frameIndex = startFrameIndex
    cam.set(cv2.CAP_PROP_POS_FRAMES, startFrameIndex)

    print(numOfFrames, frameRate)

    while(frameIndex <= endFrameIndex):
        ret, frame = cam.read()
        if ret:
            name = './TestImages3/frame' + str(capturedFrameIndex) + '.jpg'
            print('Creating... ' + name + " " + str(frameIndex))
            frameIndex += captureRate
            capturedFrameIndex += 1
            cam.set(cv2.CAP_PROP_POS_FRAMES, frameIndex)
        else:
            break
        frameIndex = int(cam.get(cv2.CAP_PROP_POS_FRAMES))
    
    cam.release()
    

def func3():
    cam = cv2.VideoCapture(r"D:\ActionRecognition\UCF-101\Biking\v_Biking_g01_c01.avi")
    numOfFrames = int(cam.get(cv2.CAP_PROP_FRAME_COUNT))
    frameRate = int(cam.get(cv2.CAP_PROP_FPS))

    startFrameIndex = int(numOfFrames / 2) - 20
    endFrameIndex = int(numOfFrames / 2) + 20
    captureRate = 5
    capturedFrameIndex = 0

    print(numOfFrames, frameRate)
    
    while(True):
        frameIndex = int(cam.get(cv2.CAP_PROP_POS_FRAMES))
        ret, frame = cam.read()
        if ret:
            if frameIndex >= startFrameIndex and frameIndex <= endFrameIndex and frameIndex % captureRate == 0:
                name = './TestImages2/frame' + str(capturedFrameIndex) + '.jpg'
                print('Creating... ' + name + " " + str(frameIndex))
##                cv2.imwrite(name, frame)
                capturedFrameIndex += 1
        else:
            break
    
    cam.release()

def func2():
    cam = cv2.VideoCapture(r"D:\ActionRecognition\UCF-101\Biking\v_Biking_g01_c01.avi")
    numOfFrames = int(cam.get(cv2.CAP_PROP_FRAME_COUNT))
    print(numOfFrames)
    cam.release()
    
def func1():
    cam = cv2.VideoCapture(r"D:\ActionRecognition\UCF-101\Biking\v_Biking_g01_c01.avi")
    currentframe = 0

    while(True):
        ret, frame = cam.read()
        if ret:
            name = './TestImages/frame' + str(currentframe) + '.jpg'
            print('Creating... ' + name)

            cv2.imwrite(name, frame)
            currentframe += 1
        else:
            break
    cam.release()
    
if __name__ == '__main__':
    func4()
