import pathlib
import shutil

"""
Documentation:
- pathlib
    1. exists(), is_dir(), mkdir()
        - https://docs.python.org/3/library/pathlib.html
- shutil
    1. rmtree()
        - https://docs.python.org/3/library/shutil.html
"""

"""
Function Name: removeDirectory
Number of parameters: 1
List of parameters:
    1. dirpath | pathlib.Path | Path to the directory that is to be removed.
Pre-condition: n/a
Post-condition:
    1. The directory (and all directories inside of it) are removed.
"""
def removeDirectory(dirpath):
    if dirpath.exists() and dirpath.is_dir():
        shutil.rmtree(dirpath)

"""
Function Name: createDirectory
Number of parameters: 1
List of parameters:
    1. dirpath | pathlib.Path | Path to the dirctory that is to be created.
Pre-condition: n/a
Post-condition:
    1. The directory (and all parent directories that don't already exist) are created.
"""
def createDirectory(dirpath):
    if not dirpath.exists():
        dirpath.mkdir(parents = True)
