import pathlib
import extractImages
import shutil
import csv
from google.cloud import storage
import requests
from contextlib import closing
import csv
import codecs
import os 
import re

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

# Gets the class names by GET request for .csv in GCS that contains all classnames
def getClassNames(ucfVideosPath, numOfClasses):
    #url = ucfVideosPath/"UCF_classnames.csv"
    url = "https://storage.googleapis.com/action-recognition-dataset-1/UCF%20101%20MP4/UCF_classnames.csv"
    with closing(requests.get(url, stream=True)) as r:
        reader = csv.reader(codecs.iterdecode(r.iter_lines(), 'utf-8'), delimiter=',', quotechar='"')
        #classNames is the list of all the rows items from the .csv
        for classNames in reader: 
            continue
    return classNames[:numOfClasses]

def getVideoFilePaths(ucfVideosPath, classNames):
    #get video paths from google cloud storage
    bucket_name = "action-recognition-dataset-1"
    storage_client = storage.Client()
    
    #note: can't pass just the base bc they're files (.csv) in the bucket 
    base="UCF 101 MP4/"
    
    #list to hold all the video names by classes
    allVideoFilePaths =[]
    videoNames = []
    
    for className in classNames:
        blobs = storage_client.list_blobs(
            bucket_name, prefix=base+className
        )
        for blob in blobs:
            #use regex to remove prefix to obtain classname/video_names
            videoName = re.sub(base, '', blob.name)
            blobPath = pathlib.Path(videoName)
            videoName = ucfVideosPath/blobPath
            allVideoFilePaths.append(videoName)
            
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
        extractImages.extractImages(videoFilePath, videoFileName, destinationPath, 1, 1, 1)
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
    rootPath = pathlib.Path(r"/home/jupyter/action-recognition")
    ucfVideosPath = pathlib.Path(r"https://storage.googleapis.com/action-recognition-dataset-1/UCF%20101%20MP4") #path to ucf-101 dataset
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
