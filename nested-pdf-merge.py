#!/usr/bin/env python3

# Parse arguments before running main program
import argparse, os

def dir_path(string):
    if os.path.isdir(string):
        return string
    else:
        raise NotADirectoryError(string)

ap = argparse.ArgumentParser(description="Merge nested image direcotry into PDF with nested bookmarks.")
ap.add_argument("-i", "--input_dir", type=dir_path, required=True,
    help="path to nested image directory to merge")
ap.add_argument("-o", "--output_file", type=str, default=None,
    help="output file path (defaults to [input_dir].pdf)")
args = vars(ap.parse_args())

# Declare functions
def sorted_walk(top, topdown=True, onerror=None):
    # Ripped from os module and slightly modified for alphabetical sorting
    names = os.listdir(top)
    names.sort()
    dirs, nondirs = [], []
 
    for name in names:
        if os.path.isdir(os.path.join(top, name)):
            dirs.append(name)
        else:
            nondirs.append(name)
 
    if topdown:
        yield top, dirs, nondirs
    for name in dirs:
        path = os.path.join(top, name)
        if not os.path.islink(path):
            for x in sorted_walk(path, topdown, onerror):
                yield x
    if not topdown:
        yield top, dirs, nondirs

# Walk though folder structure (recursive alphabetical)
for root, sub_folders, files in sorted_walk(args["input_dir"]):
    files.sort()
    for file in files:
        file_name = os.path.join(root,file)
        
        #TODO: Actually make PDF
        print(file_name)