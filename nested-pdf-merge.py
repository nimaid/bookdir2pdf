#!/usr/bin/env python3

import argparse, os, sys

# Test if this is a PyInstaller executable or a .py file
if getattr(sys, 'frozen', False):
    IS_EXE = True
    PROG_FILE = sys.executable
    PROG_PATH = os.path.dirname(PROG_FILE) 
    PATH = sys._MEIPASS
else:
    IS_EXE = False
    PROG_FILE = os.path.realpath(__file__)
    PROG_PATH = os.path.dirname(PROG_FILE)
    PATH = PROG_PATH

#TODO: Use 'PROG_PATH' if files are relative paths to .exe

# Parse arguments before running main program
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
ap.add_argument("-s", "--order_number_seperator", type=str, default=None,
    help="the character used to seperate the direcotry ordering numbers from the bookmark names (like '.' or ')')")
args = vars(ap.parse_args())

input_dir_name = args["input_dir"].strip(os.path.sep).split(os.path.sep)[-1]

if args["output_file"] == None:
    output_file = input_dir_name + os.path.extsep + "pdf"
else:
    out_dir, out_name = os.path.split(args["output_file"])
    out_name_split = out_name.split(os.path.extsep)
    if len(out_name_split) >= 2:
        # There is an extention
        output_file = args["output_file"]
        if out_name_split[-1].lower() != "pdf":
            output_file += os.path.extsep + "pdf"
    else:
        # No extention provided
        output_file = args["output_file"] + os.path.extsep + "pdf"

# Do main imports
from fpdf import FPDF
from PIL import Image
from functools import reduce
from collections import OrderedDict
from PyPDF2 import PdfFileWriter, PdfFileReader

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


#TODO: Put images before folders if they come first alphabetically
#TODO:     Currently, not... 
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
print("Adding images to PDF...")
temp_pdf = "temp_" + output_file
pdf = FPDF(unit = "pt", format = [width, height])
for page in page_list:
    print("Adding page: " + page)
    pdf.add_page()
    pdf.image(page, 0, 0)
print("Saving temporary PDF '{}'".format(temp_pdf))
pdf.output(temp_pdf, "F")


# Load PDF into PyPDF2
print("Loading temporary PDF into editing library...")
output_pdf = PdfFileWriter()
input_pdf = PdfFileReader(open(temp_pdf, 'rb'))
for p in range(input_pdf.numPages):
    output_pdf.addPage(input_pdf.getPage(p))

# Delete temporary PDF
print("Deleting temporary PDF '{}'".format(temp_pdf))
os.remove(temp_pdf)

# Add nested bookmarks from page_dict
print()
print("Creating nested bookmarks...")
ident = ""
ident_str = "--- "
last_page_index = 0
path_list = list()
bookmark_list = list()
def iterdict(d, base_path=""):
    global ident
    global path_list
    global last_page_index

    for k, v in d.items():        
        if isinstance(v, OrderedDict):
            #TODO: Strip leading numbers more dynamically
            if args["order_number_seperator"] == None:
                bm_name = k
            else:
                bm_name = args["order_number_seperator"].join(k.split(args["order_number_seperator"])[1:]).strip(" ")
            print(ident + bm_name + "\tPage #" + str(last_page_index + 1))
            ident += ident_str
            
            path_list.append(k)
            
            # Add bookmark w/ parent
            if len(bookmark_list) > 0:
                bm_parent = bookmark_list[-1]
            else:
                bm_parent = None
            
            bm = output_pdf.addBookmark(bm_name, last_page_index, parent=bm_parent)
            bookmark_list.append(bm)
            
            iterdict(v, base_path=base_path)
            
            temp = bookmark_list.pop()
            temp = path_list.pop()
            
            ident = ident[:-len(ident_str)]
        else:
            filename = os.path.join(base_path, os.path.sep.join(path_list + [k]))
            page_index = page_list.index(filename)
            last_page_index = page_index + 1
            #print(ident + k + "\tPage #" + str(page_index + 1))
iterdict(page_dict[input_dir_name], base_path=input_dir_name)

# Save final PDF
print("Saving bookmarked PDF '{}'".format(output_file))
with open(output_file, 'wb') as f:
    output_pdf.write(f)
