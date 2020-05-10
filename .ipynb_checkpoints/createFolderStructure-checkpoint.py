import directoryFunctions
import extractFrames
import pathlib
import shutil
import csv
from google.cloud import storage
import requests
from contextlib import closing
import csv
import codecs
import os 
import re
import boto3
import googleapiclient.discovery

# Gets the class names
def getClassNames(numOfClasses):
    #request to grab sub directory names in bucket
    service = googleapiclient.discovery.build('storage', 'v1')
    req = service.objects().list(bucket="action-recognition-dataset-1", prefix="UCF 101 MP4/", delimiter='/')
    res = req.execute()
    names = res['prefixes'] #list containing ["UCF 101 MP4/ApplyLipstick/"...]
    classNames = []
    for name in names :
        name = re.sub("UCF 101 MP4/", '', name)
        name = re.sub("/", '', name)
        classNames.append(name)
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

def createDirectories(dirpath, classNames):
    directories = []
    directories.append(dirpath/'Train')
    directories.append(dirpath/'Validation')
    directories.append(dirpath/'Test')
    
    for directory in directories:
        for className in classNames:
            directoryFunctions.createDirectory(directory/className)

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
        
        #extractFrames.extractFrames(videoFilePath, videoFileName, destinationPath, 1, 3)
        
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
#     BUCKET = 'gcs-cred-yukkee'
#     KEY = 'Senior-Design-1-1ccfbb525add.json'
#     s3 = boto3.resource('s3')
#     s3.Bucket(BUCKET).download_file(KEY, 'Senior-Design-1-1ccfbb525add.json')
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] =  'Senior-Design-1-1ccfbb525add.json'

    rootAWSPath      = pathlib.Path(r"/home/ec2-user/SageMaker/action-recognition") # Top-level ("root") path
    rootGCSPath      = pathlib.Path(r"/home/jupyter/action-recognition")
    ucfVideosPath = pathlib.Path(r"https://storage.googleapis.com/action-recognition-dataset-1/UCF%20101%20MP4")                             
    framesPath    = rootAWSPath/'Frames'                     # path to Frames Data Directory
    sequencesPath = rootAWSPath/'Sequences'                  # path to Sequences Data Directory
    numOfClasses  = 44
    
#     directoryFunctions.removeDirectory(framesPath)
    directoryFunctions.removeDirectory(sequencesPath)
    
    classNames         = getClassNames(numOfClasses)
    allVideoFilePaths  = getVideoFilePaths(ucfVideosPath, classNames)
    videoFileNames     = getVideoFileNames(allVideoFilePaths)
    videoFileNamesInfo = getVideoFileNamesInfo(videoFileNames)
    
    appendVideoFilePath(allVideoFilePaths, videoFileNamesInfo)
    #createDirectories(framesPath, classNames)
    createDirectories(sequencesPath, classNames)
    generateTrainAndTestFrames(rootAWSPath, framesPath, videoFileNamesInfo)
    


    

if __name__ == '__main__':
    main()






