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
        return classes

    # returns the number of classes
    def getNumClasses(self):
        return len(self.classes)

    # returns a list of paths to frames for a video
    @staticmethod
    def getFramesForVideo(dataRow):
        videoFilename = dataRow[2]
        framesPath    = pathlib.Path(r"/home/jupyter/action-recognition")/dataRow[0]/dataRow[1]
        frames        = sorted(framesPath.glob(videoFilename + '*')) # sorted list so that the frames are in 'sequential' order
        return frames

##if __name__ == '__main__':
##    d = Data()
##    d.getFramesForVideo(d.data[0])
            
    
