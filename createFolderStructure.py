import directoryFunctions ####
import extractFrames
import pathlib
import shutil
import csv

#### removed removeDirectory function

# Gets the class names
def getClassNames(ucfVideosPath, numOfClasses):
    directories = ucfVideosPath.glob('*')
    classNames  = []
    for directory in directories:
        classNames.append(directory.name)
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

#### removed createDirectory function

#### removed some lines
def createDirectories(dirpath, classNames):
    directories = []
    directories.append(dirpath/'Train')
    directories.append(dirpath/'Validation')
    directories.append(dirpath/'Test')
    
    for directory in directories:
        for className in classNames:
            createDirectory(directory/className)

def generateTrainAndTestFrames(rootPath, framesPath, videoFileNamesInfo):
    data = []
    for videoFileNameInfo in videoFileNamesInfo:
        if videoFileNameInfo[2] > 'g10':
            destinationPath = framesPath/'Train'
            datasetType     = "Train"
        elif videoFileNameInfo[2] > 'g05' and videoFileNameInfo[2] < 'g11':
            destinationPath = framesPath/'Validation'
            datasetType     = "Validation"
        else:
            destinationPath = framesPath/'Test'
            datasetType     = "Test"
            
        destinationPath = str(destinationPath/videoFileNameInfo[1])
        videoFilePath   = str(videoFileNameInfo[4])
        videoFileName   = videoFileNameInfo[4].stem
        
        extractFrames.extractFrames(videoFilePath, videoFileName, destinationPath, 2, 3)
        
        numFrames = getNumFramesFromVideo(destinationPath, videoFileName)
        data.append([datasetType, videoFileNameInfo[1], videoFileName, numFrames])
    writeDataToCsv(data, rootPath)

def getNumFramesFromVideo(destinationPath, videoFileName):
    partialPath = pathlib.Path(destinationPath)
    items       = list(partialPath.glob(videoFileName + '*.jpg'))
    return len(items)

def writeDataToCsv(data, destinationPath):
    filename = 'data.csv'
    filePath = destinationPath/filename
    
    with open(filePath, 'w', newline='') as csvfile:
        csvWriter = csv.writer(csvfile)
        csvWriter.writerows(data)
    

def main():
    rootPath      = pathlib.Path(r"D:\ActionRecognition") # Top-level ("root") path
    ucfVideosPath = rootPath/'UCF-101'                    # path to ucf-101 dataset
    framesPath    = rootPath/'Frames'                     # path to Frames Data Directory
    sequencesPath = rootPath/'Sequences'                  # path to Sequences Data Directory
    numOfClasses  = 3
    
    directoryFunctions.removeDirectory(framesPath)
    directoryFunctions.removeDirectory(sequencesPath)
    
    classNames         = getClassNames(ucfVideosPath, numOfClasses)
    allVideoFilePaths  = getVideoFilePaths(ucfVideosPath, classNames)
    videoFileNames     = getVideoFileNames(allVideoFilePaths)
    videoFileNamesInfo = getVideoFileNamesInfo(videoFileNames)
    
    appendVideoFilePath(allVideoFilePaths, videoFileNamesInfo)
    createDirectories(framesPath, classNames)
    createDirectories(sequencesPath, classNames)
    generateTrainAndTestFrames(rootPath, framesPath, videoFileNamesInfo)

if __name__ == '__main__':
    main()






