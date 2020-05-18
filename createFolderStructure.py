import directoryFunctions
import extractFrames
import pathlib
import config
import csv

"""
Documentation:
- csv
    1. writer(), writerows()
        - https://docs.python.org/3/library/csv.html
- pathlib
    1. Path(), /, .name, .stem, .glob()
        - https://docs.python.org/3/library/pathlib.html
"""

"""
Function Name: getClassNames
Number of parameters: 2
List of parameters:
    1. ucfVideosPath | pathlib.Path | Path to the ucf101 dataset.
    2. numClasses    | int          | Number of classes to be used in the dataset.
Pre-condition:
    1. 'ucfVideosPath' exists and points to the directory that contains the ucf101 dataset.
    2. 'numClasses' is an integer (inclusively) between 0 and 101.
Post-condition:
    1. Returns a sorted list of class names of length 'numClasses'.
"""
def getClassNames(ucfVideosPath, numClasses):
    directories = sorted(ucfVideosPath.glob('*'))
    classNames  = []
    for directory in directories:
        classNames.append(directory.name)
    return classNames[:numClasses]

"""
Function Name: getVideoFilePaths
Number of parameters: 2
List of parameters:
    1. ucfVideosPath | pathlib.Path | Path to the ucf101 dataset.
    2. classNames    | list         | List of classnames.
Pre-condition:
    1. 'ucfVideosPath' exists and points to the directory that contains the ucf-101 dataset.
    2. 'classNames' contains strings that matches some of the directory names inside the ucf101 dataset.
Post-condition:
    1. Returns a dict where the keys are class names and the values are sorted lists of video file paths corresponding to
       the key (class name).
"""
def getVideoFilePaths(ucfVideosPath, classNames):
    videoClassPaths = {}
    for className in classNames:
            videoClassPaths[className] = ucfVideosPath/className
    
    allVideoFilePaths = {}
    for className in videoClassPaths:
        allVideoFilePaths[className] = list(sorted(videoClassPaths[className].glob('*.avi')))
    return allVideoFilePaths

"""
Function Name: getVideoFileNames
Number of parameters: 1
List of parameters:
    1. allVideoFilePaths | dict | Dict where the keys are class names and the values are sorted lists of video file paths.
Pre-condition: n/a
Post-condition:
    1. Returns a dict where the keys are class names and the values are a sorted list of video file names corresponding to
       the key (class name).
."""
def getVideoFileNames(allVideoFilePaths):
    videoFileNames = {}
    for className in allVideoFilePaths:
        for videoFilePath in allVideoFilePaths[className]:
            if className not in videoFileNames:
                videoFileNames[className] = [videoFilePath.stem]
            else:
                videoFileNames[className].append(videoFilePath.stem)
    return videoFileNames

"""
Function Name: getVideoFileNamesInfo
Number of parameters: 1
List of parameters:
    1. videoFileNames | dict | Dict where the keys are class names and the values are sorted list of video file names.
Pre-condition: n/a
Post-condition:
    1. Returns a dict where the keys are class names and the values are list of lists, where each inner list contains the values
       of a video file name after being split by the '_' separator.
"""
def getVideoFileNamesInfo(videoFileNames):
    videoFileNamesInfo = {}
    for className in videoFileNames:
        for videoFileName in videoFileNames[className]:
            if className not in videoFileNamesInfo:
                videoFileNamesInfo[className] = [videoFileName.split('_')]
            else:
                videoFileNamesInfo[className].append(videoFileName.split('_'))
    return videoFileNamesInfo

"""
Function Name: appendVideoFilePath
Number of parameters: 2
List of parameters:
    1. allVideoFilePaths  | dict | Dict where the keys are class names and the values are sorted lists of video file paths.
    2. videoFileNamesInfo | dict | Dict where the keys are class names and the values are list of lists where each inner list
                                   contains the result of splitting each video file name.
Pre-condition:
    1. 'allVideoFilePaths' and 'videoFileNamesInfo' are the same length.
Post-condition:
    1. 'videoFileNamesInfo' is amended such that each inner list in the value field is appended with a (corresponding)
        video file path (based on a common class name and position in their respective list).
    2. Nothing is returned.
"""    
def appendVideoFilePath(allVideoFilePaths, videoFileNamesInfo):
    for className in allVideoFilePaths:
        for i in range(len(allVideoFilePaths[className])):
            videoFileNamesInfo[className][i].append(allVideoFilePaths[className][i])

"""
Function Name: createDirectories
Number of parameters: 2
List of parameters:
    1. dirpath    | pathlib.Path | Path where the directories will be created at.
    2. classNames | list         | List of classnames.
Pre-condition:
    1. 'dirpath' exists.
Post-condition:
    1. Train, Validation, and Test directories are created at 'dirpath'. Within each directory, a directory is created for each
       class name in classNames.
    2. Nothing is returned.
"""
def createDirectories(dirpath, classNames):
    directories = []
    directories.append(dirpath/'Train')
    directories.append(dirpath/'Validation')
    directories.append(dirpath/'Test')
    
    for directory in directories:
        for className in classNames:
            directoryFunctions.createDirectory(directory/className)

"""
Function Name: generateFrameDatasets
Number of parameters: 5
List of parameters:
    1. rootPath           | pathlib.Path | Root path that contains the other directories.
    2. framesPath         | pathlib.Path | Path to the frames directory.
    3. videoFileNamesInfo | dict         | Dict where the keys are class names and the values are list of lists where each inner list
                                           contains the result of splitting each video file name and the path to the video.
    4. maxNumOfFrames     | int          | Maximum number of frames to be extracted.
    5. extractRate        | int          | The frequency at which frames are to be extracted. (E.g. 3 => Extract every THIRD frame)
Pre-condition:
    1. 'rootPath' and 'framesPath' exists.
Post-condition:
    1. Create 'maxNumOfFrames' frames for each video file in 'videoFileNamesInfo' and store them in their repsective directory.
    2. Creates a csv file at 'rootPath' that stores the datasetType, className, videoFileName and numFrames
       for each video file in 'videoFileNamesInfo'.
    3. Nothing is returned.
"""
def generateFrameDatasets(rootPath, framesPath, videoFileNamesInfo, maxNumOfFrames, extractRate):
    data = []
    for className in videoFileNamesInfo:
        for videoFileNameInfo in videoFileNamesInfo[className]:
            if videoFileNameInfo[2] > 'g10':
                destinationPath = framesPath/'Train'
                datasetType     = "Train"
            elif videoFileNameInfo[2] > 'g05' and videoFileNameInfo[2] < 'g11':
                destinationPath = framesPath/'Validation'
                datasetType     = "Validation"
            else:
                destinationPath = framesPath/'Test'
                datasetType     = "Test"
            
            destinationPath = str(destinationPath/className)
            videoFilePath   = str(videoFileNameInfo[4])
            videoFileName   = videoFileNameInfo[4].stem
            
            extractFrames.extractFrames(videoFilePath, videoFileName, destinationPath, maxNumOfFrames, extractRate)
            numFrames = getNumFramesFromVideo(destinationPath, videoFileName)
            data.append([datasetType, className, videoFileName, numFrames])
    writeDataToCsv(data, rootPath)

"""
Function Name: getNumFramesFromVideo
Number of parameters: 2
List of parameters:
    1. destinationPath | str | Path to the directory that contains the frames to one of the three datasets.
    2. videoFileName   | str | Name of a video file.
Pre-condition:
    1. 'destinationPath' exists.
Post-condition:
    1. Returns the number of images (.jpg files) in 'destinationPath' whose names start with 'videoFileName'.
"""
def getNumFramesFromVideo(destinationPath, videoFileName):
    partialPath = pathlib.Path(destinationPath)
    items       = list(sorted(partialPath.glob(videoFileName + '*.jpg')))
    return len(items)

"""
Function Name: writeDataToCsv
Number of parameters: 2
List of parameters:
    1. data            | list         | List of data to write to a csv file.
    2. destinationPath | pathlib.Path | Path where the csv file will be saved at.
Pre-condition:
    1. 'destinationPath' exists.
Post-condition:
    1. Data is written to a csv file, data.csv.
    2. Nothing is returned.
"""
def writeDataToCsv(data, destinationPath):
    filename = 'data.csv'
    filePath = destinationPath/filename
    
    with open(filePath, 'w', newline='') as csvfile:
        csvWriter = csv.writer(csvfile)
        csvWriter.writerows(data)
    
"""
Function Name: main
Number of parameters: 0
List of parameters: n/a
Pre-condition:
Post-condition:
    1. Frames and Sequences directories are created. Within each, directories for the three datasets
       (Train, Validation, and Test) are created. And within each, directories for each class is created.
    2. Videos in some classes have their frames extracted and then stored in one of the directories in the
       frames directory.
    3. Data on the frames extracted from each video is stored in a csv file (data.csv), that is within the 'rootpath'.
"""
def main():
    cf            = config.Config()
    rootPath      = pathlib.Path(cf.rootPath)
    ucfVideosPath = pathlib.Path(cf.ucfVideosPath)
    framesPath    = pathlib.Path(cf.framesPath)
    sequencesPath = pathlib.Path(cf.sequencesPath)
    numClasses    = cf.numClasses

    maxNumOfFrames = cf.maxNumOfFrames
    extractRate    = cf.extractRate
    
    directoryFunctions.removeDirectory(framesPath)
    directoryFunctions.removeDirectory(sequencesPath)
    
    classNames         = getClassNames(ucfVideosPath, numClasses)
    allVideoFilePaths  = getVideoFilePaths(ucfVideosPath, classNames)
    videoFileNames     = getVideoFileNames(allVideoFilePaths)
    videoFileNamesInfo = getVideoFileNamesInfo(videoFileNames)
    
    appendVideoFilePath(allVideoFilePaths, videoFileNamesInfo)
    
    createDirectories(framesPath, classNames)
    createDirectories(sequencesPath, classNames)
    
    generateFrameDatasets(rootPath, framesPath, videoFileNamesInfo, maxNumOfFrames, extractRate)

if __name__ == '__main__':
    main()
