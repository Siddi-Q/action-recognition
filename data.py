import csv
import pathlib

class Data():
    def __init__(self):
        self.dataCSVPath = pathlib.Path(r"D:\ActionRecognition\data.csv")
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

##if __name__ == '__main__':
##    Data()
            
    
