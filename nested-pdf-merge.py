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
# Save image paths to list
page_list = list()
for root, sub_folders, files in sorted_walk(args["input_dir"]):
    files.sort()
    for file in files:
        file_name = os.path.join(root,file)
        page_list.append(file_name)

# Get size from first page
cover = Image.open(page_list[0])
width, height = cover.size

# Create PDF (no bookmarks)
pdf = FPDF(unit = "pt", format = [width, height])
for page in page_list:
    print("Adding page: " + page)
    pdf.add_page()
    pdf.image(page, 0, 0)
pdf.output(output_file, "F")

#TODO: Add nested bookmarks