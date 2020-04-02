import pathlib
import test
import shutil
import csv

# Removes directory at dirpath
def removeDirectory(dirpath):
    if dirpath.exists() and dirpath.is_dir():
        shutil.rmtree(dirpath)

# Removes the Train and Test Directories
def removeDirectories(rootPath):
    trainPath = rootPath/'Train'
    testPath = rootPath/'Test'
    removeDirectory(trainPath)
    removeDirectory(testPath)

# Gets the class names
def getClassNames(ucfVideosPath, numOfClasses):
    res = ucfVideosPath.glob('*')
    classNames = []
    for item in res:
        classNames.append(item.name)
    return classNames[:numOfClasses]

def getVideoFilePaths(ucfVideosPath, classNames):
    videoClassPaths = []
    for i in classNames:
        videoClassPaths.append(ucfVideosPath/i)
    
    allVideoFilePaths = []
    for j in videoClassPaths:
        videoPathsList = list(j.glob('*.avi'))
        allVideoFilePaths.extend(videoPathsList)
    return allVideoFilePaths

def getVideoFileNames(allVideoFilePaths):
    videoFileNames = []
    for path in allVideoFilePaths:
        videoFileNames.append(path.stem)
    return videoFileNames

def getVideoFileNamesInfo(videoFileNames):
    videoFileNamesInfo = []
    for videoFileName in videoFileNames:
        videoFileNamesInfo.append(videoFileName.split('_'))
    return videoFileNamesInfo

def appendVideoFilePath(allVideoFilePaths, videoFileNamesInfo):
    for i in range(len(allVideoFilePaths)):
        videoFileNamesInfo[i].append(allVideoFilePaths[i])

def createDirectories(rootPath, classNames):
    imageDirectories = []
    imageDirectories.append(rootPath/'Train')
    imageDirectories.append(rootPath/'Test')
    for directory in imageDirectories:
        if not directory.exists():
            directory.mkdir()
        for className in classNames:
            if not (directory/className).exists():
                (directory/className).mkdir()

def generateTrainAndTestSets(rootPath, videoFileNamesInfo):
    data = []
    for videoFileNameInfo in videoFileNamesInfo:
        if videoFileNameInfo[2] > 'g07':
            destinationPath = rootPath/'Train'
            testOrTrain = "Train"
        else:
            destinationPath = rootPath/'Test'
            testOrTrain = "Test"
            
        destinationPath = str(destinationPath/videoFileNameInfo[1])
        videoFilePath = str(videoFileNameInfo[4])
        videoFileName = videoFileNameInfo[4].stem
        test.extractImages(videoFilePath, videoFileName, destinationPath, 1, 1, 1)
        numFrames = getNumFramesFromVideo(destinationPath, videoFileName)
        data.append([testOrTrain, videoFileNameInfo[1], videoFileName, numFrames])
    writeDataToCsv(data, rootPath)

def getNumFramesFromVideo(destinationPath, videoFileName):
    partialPath = pathlib.Path(destinationPath)
    items = list(partialPath.glob(videoFileName + '*.jpg'))
    return len(items)

def writeDataToCsv(data, destinationPath):
    filename = 'data.csv'
    filePath = destinationPath/filename
    
    with open(filePath, 'w', newline='') as csvfile:
        csvWriter = csv.writer(csvfile)
        csvWriter.writerows(data)
    

def main():
    rootPath = pathlib.Path(r"D:\ActionRecognition")
    ucfVideosPath = pathlib.Path(r"D:\ActionRecognition\UCF-101") #path to ucf-101 dataset
    numOfClasses = 1
    
    removeDirectories(rootPath)
    classNames = getClassNames(ucfVideosPath, numOfClasses)
    allVideoFilePaths = getVideoFilePaths(ucfVideosPath, classNames)
    videoFileNames = getVideoFileNames(allVideoFilePaths)
    videoFileNamesInfo = getVideoFileNamesInfo(videoFileNames)
    appendVideoFilePath(allVideoFilePaths, videoFileNamesInfo)
    createDirectories(rootPath, classNames)
    generateTrainAndTestSets(rootPath, videoFileNamesInfo)

if __name__ == '__main__':
    main() 
