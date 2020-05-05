import pathlib
import shutil

# Removes directory at dirpath
def removeDirectory(dirpath):
    if dirpath.exists() and dirpath.is_dir():
        shutil.rmtree(dirpath)

# Creates a directory at dirpath
def createDirectory(dirpath):
    if not dirpath.exists():
        dirpath.mkdir(parents = True)
