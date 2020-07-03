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

if not os.path.isabs(args["input_dir"]):
    input_dir = os.path.join(PROG_PATH, args["input_dir"])
else:
    input_dir = args["input_dir"]

input_dir_name = input_dir.strip(os.path.sep).split(os.path.sep)[-1]


if args["output_file"] == None:
    output_file = input_dir + os.path.extsep + "pdf"
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

output_file_dir, output_file_name = os.path.split(output_file)

# Do main imports
from fpdf import FPDF
from PIL import Image
from collections import OrderedDict
from PyPDF2 import PdfFileWriter, PdfFileReader
from pathlib import Path

# Walk though folder structure (recursive alphabetical, mixed files/folders)
# Save image paths to ordered list
page_list = [str(p) for p in sorted(Path(input_dir).glob('**/*')) if p.is_file()]

# Ignore certain files
ignored_file_exts = [".ignore", ".db"]
page_list = [x for x in page_list if os.path.splitext(x)[-1].lower() not in ignored_file_exts]

# Create nested ordered dictionary from list
page_dict = OrderedDict()
for p in page_list:
    p = os.path.relpath(p, input_dir) # Make relative
    current_level = page_dict
    for part in p.split(os.path.sep):
        if part not in current_level:
            current_level[part] = OrderedDict()
        current_level = current_level[part]

# Get size from first page
cover = Image.open(page_list[0])
width, height = cover.size

# Create PDF from page_list(no bookmarks)
print("Adding images to PDF...")
temp_pdf = os.path.join(output_file_dir, "temp_" + output_file_name)
pdf = FPDF(unit = "pt", format = [width, height])
for page in page_list:
    print("Adding page: " + page)
    pdf.add_page()
    pdf.image(page, 0, 0)
print("Saving temporary PDF '{}'".format(temp_pdf))
pdf.output(temp_pdf, "F")

# Load PDF into PyPDF2
print()
print("Loading temporary PDF into editing library...")
output_pdf = PdfFileWriter()

input_pdf_file = open(temp_pdf, 'rb')
input_pdf = PdfFileReader(input_pdf_file)
for p in range(input_pdf.numPages):
    output_pdf.addPage(input_pdf.getPage(p))

# Add nested bookmarks from page_dict
#TODO: Add bookmarks for empty folders
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
        if len(v) > 0:
            if args["order_number_seperator"] == None:
                bm_name = k
            else:
                bm_name = args["order_number_seperator"].join(k.split(args["order_number_seperator"])[1:]).strip(" ")
            print(ident + bm_name + "\tPage #" + str(last_page_index + 1))
            ident += ident_str
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
iterdict(page_dict, base_path=input_dir)

# Save final PDF
print("Saving bookmarked PDF '{}'".format(output_file))
with open(output_file, 'wb') as f:
    output_pdf.write(f)

# Delete temporary PDF
print()
print("Deleting temporary PDF '{}'".format(temp_pdf))
input_pdf_file.close()
os.remove(temp_pdf)