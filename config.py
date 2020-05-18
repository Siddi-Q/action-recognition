import pathlib

"""
Documentation:
- pathlib
    1. pathlib.Path(), /
        - https://docs.python.org/3/library/pathlib.html
"""

"""
Class Name: Config
Description: The Config class contains variables that will be referenced in the other files.
Number of member variables: 7
List of member variables:
    1. numClasses     | int | The number of classes to be used in the dataset.
    2. maxNumOfFrames | int | The maximum number of frames that will be extracted from each video.
    3. extractRate    | int | The frequency at which frames are to be extracted. (E.g. 3 => Extract every THIRD frame)
    4. rootPath       | str | The path to the Top-Level (root) directory that should contain the UCF-101 directory.
                              Other directories/files will be stored within the directory at this path.
    5. ucfVideosPath  | str | The path to the UCF-101 directory, that contains the UCF-101 dataset.
    6. framesPath     | str | The path to the frames directory, that is within the rootPath.
    7. sequencesPath  | str | The path to the sequences directory, that is within the rootPath.
Number of methods: 0
List of methods: n/a
"""
class Config():
    def __init__(self):
        self.numClasses     = 3
        self.maxNumOfFrames = 2
        self.extractRate    = 3
        self.rootPath       = r"D:\ActionRecognition"
        self.ucfVideosPath  = str(pathlib.Path(self.rootPath)/"UCF-101")
        self.framesPath     = str(pathlib.Path(self.rootPath)/"Frames")
        self.sequencesPath  = str(pathlib.Path(self.rootPath)/"Sequences")
