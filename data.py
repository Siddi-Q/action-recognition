import csv
import pathlib
import config

"""
Documentation:
- csv
    1. reader()
        - https://docs.python.org/3/library/csv.html
- pathlib
    1. Path(), /, .glob()
        - https://docs.python.org/3/library/pathlib.html
"""

"""
Class Name: Data
Description: The Data class is an interface to the data.csv file.
Number of member variables: 4
List of member variables:
    1. dataCSVPath | pathlib.Path | Path to the data.csv file.
    2. data        | list         | List of lists, where each inner list cooresponds to a row in the data.csv file.
    3. classes     | list         | List of classes in self.data.
    4. numClasses  | int          | Number of classes (length of self.classes).
Number of methods: 8
List of methods:
    1. __init__(self)
    2. getData(self)
    3. getClasses(self)
    4. getNumClasses(self)
    5. getClassIndex(self, className)
    6. getDatasetCount(self, datasetType)
    7. getMaxFrameCount(self)
    8. getFramesForVideo(dataRow)
"""
class Data():
    """
    Method Name: __init__
    Number of parameters: 0
    List of parameters: n/a
    Pre-condition: n/a
    Post-condition:
        1. Initializes a Data object.
    """
    def __init__(self):
        self.dataCSVPath = pathlib.Path(config.Config().rootPath)/"data.csv"
        self.data = self.getData()
        self.classes = self.getClasses()
        self.numClasses = self.getNumClasses()

    """
    Method Name: getData
    Number of parameters: 0
    List of parameters: n/a
    Pre-condition:
    Post-condition:
        1. Returns a list of lists, where each inner list corresponds to a row in the data.csv file.
    """
    def getData(self):
        with open(self.dataCSVPath, newline='') as csvfile:
            csvReader = csv.reader(csvfile)
            data = list(csvReader)
        return data

    """
    Method Name: getClasses
    Number of parameters: 0
    List of parameters: n/a
    Pre-condition: n/a
    Post-condition:
        1. Returns a list of classes based on self.data.
    """
    def getClasses(self):
        classes = []
        for row in self.data:
            dataClass = row[1]
            if dataClass not in classes:
                classes.append(dataClass)
        classes.sort()
        return classes

    """
    Method Name: getNumClasses
    Number of parameters: 0
    List of parameters: n/a
    Pre-condition: n/a
    Post-condition:
        1. Returns the number of classes.
    """
    def getNumClasses(self):
        return len(self.classes)

    """
    Method Name: getClassIndex
    Number of parameters: 1
    List of parameters:
        1. className | str | The name of the class that is used to determine what index it is located in self.classes.
    Pre-condition: n/a
    Post-condition:
        1. Returns the index of 'className' in self.classes.
    """
    def getClassIndex(self, className):
        return self.classes.index(className)

    """
    Method Name: getDatasetCount
    Number of parameters: 1
    List of parameters:
        1. datasetType | str | The name of a dataset type ('Train', 'Validation', 'Test').
    Pre-condition: n/a
    Post-condition:
        1. Returns the number of data rows in the 'datasetType' dataset.
    """
    def getDatasetCount(self, datasetType):
        count = 0
        for row in self.data:
            if row[0] == datasetType:
                count += 1
        return count

    """
    Method Name: getMaxFrameCount
    Number of parameters: 0
    List of parameters: n/a
    Pre-condition: n/a
    Post-condition:
        1. Returns the maximum number of frames that was extracted from all the videos.
    """
    def getMaxFrameCount(self):
        maxFrameCount = 0
        for row in self.data:
            if int(row[3]) > maxFrameCount:
                maxFrameCount = int(row[3])
        return maxFrameCount

    """
    Method Name: getFramesForVideo
    Number of parameters: 1
    List of parameters:
        1. dataRow | list | A data row in self.data.
    Pre-condition: n/a
    Post-condition: Returns a sorted list of paths to frames for the video in 'dataRow'.
    """
    @staticmethod
    def getFramesForVideo(dataRow):
        videoFilename = dataRow[2]
        framesPath    = pathlib.Path(config.Config().framesPath)/dataRow[0]/dataRow[1]
        frames        = sorted(framesPath.glob(videoFilename + '*')) # sorted list so that the frames are in 'sequential' order
        return frames
