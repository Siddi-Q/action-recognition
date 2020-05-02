import csv
import pathlib

class Data():
    def __init__(self):
        self.dataCSVPath = pathlib.Path(r"/home/jupyter/action-recognition/data.csv")
        self.data = self.getData()
        self.classes = self.getClasses()
        self.numClasses = self.getNumClasses()

    # returns a list of lists, where each inner list corresponds to a row in the data.csv file
    def getData(self):
        with open(self.dataCSVPath, newline='') as csvfile:
            csvReader = csv.reader(csvfile)
            data = list(csvReader)
        return data

    # returns a list of classes based on self.data
    def getClasses(self):
        classes = []
        for row in self.data:
            dataClass = row[1]
            if dataClass not in classes:
                classes.append(dataClass)
        classes.sort()
        return classes

    # returns the number of classes
    def getClassIndex(self, className):
        return self.classes.index(className)

    def getDatasetCount(self, datasetType):
        count = 0
        for row in self.data:
            if row[0] == datasetType:
                count += 1
        return count
    
    # returns a list of paths to frames for a video
    @staticmethod
    def getFramesForVideo(dataRow):
        videoFilename = dataRow[2]
        framesPath    = pathlib.Path(r"/home/jupyter/action-recognition/Frames")/dataRow[0]/dataRow[1]
        frames        = sorted(framesPath.glob(videoFilename + '*')) # sorted list so that the frames are in 'sequential' order
        return frames

##if __name__ == '__main__':
##    d = Data()
##    print(d.getDatasetCount("Test"))
