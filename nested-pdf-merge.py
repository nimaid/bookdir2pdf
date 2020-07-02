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

if args["output_file"] == None:
    input_dir_name = args["input_dir"].strip(os.path.sep).split(os.path.sep)[-1]
    output_file = input_dir_name + ".pdf"
else:
    out_dir, out_name = os.path.split(args["output_file"])
    out_name_split = out_name.split(os.path.extsep)
    if len(out_name_split) >= 2:
        # There is an extention
        output_file = args["output_file"]
        if out_name_split[-1].lower() != "pdf":
            output_file += ".pdf"
    else:
        # No extention provided
        output_file = args["output_file"] + ".pdf"

# Do main imports
from fpdf import FPDF
from PIL import Image
from functools import reduce
from collections import OrderedDict 

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

def get_directory_structure(rootdir):
    # Creates a nested ordered dictionary that represents the folder structure of rootdir
    # Keys are added in alphebetical order, recursively
    # Also returns a list with ordered file paths
    dir_dict = OrderedDict()
    dir_list = list()
    rootdir = rootdir.rstrip(os.sep)
    start = rootdir.rfind(os.sep) + 1
    for path, dirs, files in sorted_walk(rootdir):
        files.sort()
        folders = path[start:].split(os.sep)
        subdir = OrderedDict.fromkeys(files)
        parent = reduce(OrderedDict.get, folders[:-1], dir_dict)
        parent[folders[-1]] = subdir
        
        for file in files:
            filename = os.path.join(path, file)
            dir_list.append(filename)
    return dir_dict, dir_list

# Walk though folder structure (recursive alphabetical)
# Save image paths to ordered dictionary
page_dict, page_list = get_directory_structure(args["input_dir"])

# Get size from first page
cover = Image.open(page_list[0])
width, height = cover.size

# Create PDF from page_list(no bookmarks)
pdf = FPDF(unit = "pt", format = [width, height])
for page in page_list:
    print("Adding page: " + page)
    pdf.add_page()
    pdf.image(page, 0, 0)
print("Saving '{}'".format(output_file))
pdf.output(output_file, "F")

# Add nested bookmarks from page_dict
print()
ident = ""
last_page_index = 0
path_list = list()
def iterdict(d):
    global ident
    global path_list
    global last_page_index
    for k, v in d.items():        
        if isinstance(v, OrderedDict):
            #TODO: Add bookmark w/ parent
            print(str(last_page_index) + "  " + ident + k)
            ident += '\t'
            
            path_list.append(k)
            iterdict(v)
            temp = path_list.pop()
            
            ident = ident[:-1]
        else:
            filename = os.path.sep.join(path_list + [k])
            page_index = page_list.index(filename)
            last_page_index = page_index + 1
            print(str(page_index) + "  " + ident + k)
iterdict(page_dict)



    
    