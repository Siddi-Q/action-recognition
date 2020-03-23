import pathlib
import test

def getClassNames():
    ucfVideosPath = pathlib.Path(r"D:\ActionRecognition\UCF-101")
    res = ucfVideosPath.glob('*')
    classNames = []
    for item in res:
        classNames.append(item.name)
    return classNames[:3]

def getVideoFileNames():
    classNames = getClassNames()
    ucfVideosPath = pathlib.Path(r"D:\ActionRecognition\UCF-101")
    videoClassFolderNames = []
    for i in classNames:
        videoClassFolderNames.append(ucfVideosPath/i)
    allVideoPathsList = []
    for j in videoClassFolderNames:
        videoPathsList = list(j.glob('*.avi'))
        allVideoPathsList.append(videoPathsList)
    videoFileNames = []
    for k in range(len(allVideoPathsList)):
        for path in allVideoPathsList[k]:
            videoFileNames.append(path.stem)
    return [allVideoPathsList, videoFileNames]

def getVideoFileNameInfo():
    allVideoPathsList, videoFileNames = getVideoFileNames()
    videoFileNamesInfo = []
    for videoFileName in videoFileNames:
        videoFileNamesInfo.append(videoFileName.split('_'))

    allVideoPathsListFlattened = []
    for VideoPathList in allVideoPathsList:
        allVideoPathsListFlattened.extend(VideoPathList)

    for i in range(len(allVideoPathsListFlattened)):
        videoFileNamesInfo[i].append(allVideoPathsListFlattened[i])
    return videoFileNamesInfo

def createDirectories():
    rootPath = pathlib.Path(r"D:\ActionRecognition")
    classNames = getClassNames()
    imageDirectories = []
    imageDirectories.append(rootPath/'Train')
    imageDirectories.append(rootPath/'Test')
    for directory in imageDirectories:
        directory.mkdir()
        for className in classNames:
            (directory/className).mkdir()

def generateTrainAndTestSets():
    videoFilesInfo = getVideoFileNameInfo()[:]
    basePath = pathlib.Path(r"D:\ActionRecognition")
    for videoFileInfo in videoFilesInfo:
        destinationPath = basePath
        if videoFileInfo[2] > 'g07':
            destinationPath = destinationPath/'Train'
        else:
            destinationPath = destinationPath/'Test'
        destinationPath = destinationPath/videoFileInfo[1]
        destinationPath = str(destinationPath)
        videoFilePath = str(videoFileInfo[4])
        videoFileName = videoFileInfo[4].stem
        test.extractImages(videoFilePath, videoFileName, destinationPath, 1, 1, 1)

def main():
    createDirectories()
    generateTrainAndTestSets()

if __name__ == '__main__':
    main() 
