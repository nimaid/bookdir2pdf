#!/usr/bin/env python3

import argparse, os, sys
from pathlib import Path

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

# Get path that the command was called from
COMMAND_PATH = Path().absolute()

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
ap.add_argument("-t", "--table_of_contents", action="store_true",
    help="just scan directory and print table of contents")
args = vars(ap.parse_args())

input_dir = args["input_dir"]
input_dir = os.path.normpath(input_dir)
# Resolve input dir into absolute path (relative to working directory!)
if not os.path.isabs(input_dir):
    input_dir_split = input_dir.split(os.path.sep)
    if input_dir_split[0] == os.path.curdir:
        input_dir = os.path.sep.join(input_dir_split[1:])
    input_dir = os.path.join(COMMAND_PATH, input_dir)

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

print()
print("Scanning input directory...")

# Walk though folder structure (recursive alphabetical, include all files/folders)
input_dir_list = [str(p) for p in sorted(Path(input_dir).glob('**/*'))]

# Set file extentions to ignore
ignored_file_exts = [".ignore", ".db"]

# Set valid image extentions
page_exts = [".jpg", ".jpeg", ".png", ".gif"]

valid_exts = ignored_file_exts + page_exts

# Save image paths (and empty/ignored-file dirs) paths to ordered list
page_list = list()
for p in input_dir_list:
    if os.path.isfile(p):
        # Check if it's an invalid extention, and if so, fully ignore it
        p_ext = os.path.splitext(p)[-1].lower()
        if p_ext not in valid_exts:
            print("[WARNING]: Unsupported file, ignoring: '{}'".format(p))
            continue
        
        # Test if it should be ignored, and if so, fully ignore it
        if p_ext in ignored_file_exts:
            print("Ignoring file: '{}'".format(p))
            continue
            
        page_list.append(p)
    elif os.path.isdir(p):
        # Get files and directories inside p
        p_list = [str(x) for x in sorted(Path(p).glob('*'))]
        p_dir_list = [x for x in p_list if os.path.isdir(x)]
        p_file_list = [x for x in p_list if os.path.isfile(x)]
        
        # Make ignored file list
        p_file_list_ignored = list()
        for x in p_file_list:
            x_ext = os.path.splitext(x)[-1].lower()
            if (x_ext not in ignored_file_exts) and (x_ext in valid_exts):
                p_file_list_ignored.append(x)
        
        # Test if it's empty or contains only ignored files
        if len(p_dir_list) <= 0 and len(p_file_list_ignored) <= 0:
            # Add path (used to make "empty" bookmarks)
            page_list.append(p)

# Make page_list but with only files
page_list_files = [p for p in page_list if os.path.isfile(p)]

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
cover = Image.open(page_list_files[0])
width, height = cover.size

# Get number of pages
num_pages = len(page_list_files)

if not args["table_of_contents"]:
    # Create PDF from page_list(no bookmarks)
    print()
    print("Adding images to PDF...")
    temp_pdf = os.path.join(output_file_dir, "temp_" + output_file_name)
    pdf = FPDF(unit = "pt", format = [width, height])
    for page in page_list_files:
        #TODO: Process with blur+sharpen
        #TODO: Process with adaptive threshold
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
print()
if args["table_of_contents"]:
    toc_title = input_dir_name + " - Table of Contents"
    print(toc_title)
    print(''.join(['-' for x in range(len(toc_title))]))
else:
    print("Creating nested bookmarks...")
ident = ""
ident_str = "--- "
pagenum_pre = "Page #"
pagenum_space = 5
last_page_index = -1 # Because we want the next page to be 0
path_list = list()
bookmark_list = list()
def iterdict(d, base_path="", empty_parents_in=list()):
    global ident
    global path_list
    global last_page_index

    for k, v in d.items(): 
        filename = os.path.join(base_path, os.path.sep.join(path_list + [k]))
        
        # Get parent bookmark
        if len(bookmark_list) > 0:
            bm_parent = bookmark_list[-1]
        else:
            bm_parent = None
        
        # Remove leading order numbers from dir name (if applicable)
        if args["order_number_seperator"] == None:
            bm_name = k
        else:
            bm_name = args["order_number_seperator"].join(k.split(args["order_number_seperator"])[1:]).strip(" ")
        
        page_ref = last_page_index + 1
        
        # Test if it's a file or a directory
        if len(v) > 0:
            # It's a not-fully-empty dir (pages/folders)
            
            # Get recursive list of files and folders
            v_list = [str(x) for x in Path(filename).glob('**/*')]
            v_dir_list = [x for x in v_list if os.path.isdir(x)]
            v_file_list = [x for x in v_list if os.path.isfile(x) and os.path.splitext(x)[-1] in page_exts]
            
            # Deal with recursively empty folders
            empty_parents = list()
            if len(v_file_list) <= 0:
                # Test if is not a subdir of an empty_parent
                is_subdir_of_empty_parent = False
                for empty_parent in empty_parents:
                    if os.path.commonpath([filename, empty_parent]) == empty_parent:
                        is_subdir_of_empty_parent = True
                if not is_subdir_of_empty_parent:
                    # This is the main parent
                    page_ref += 1
                    empty_parents.append(filename)
            
            # Prevent referencing non-existent pages
            page_ref = min(page_ref, num_pages - 1)
            
            
            # Print row of ToC
            page_toc_prefix = pagenum_pre + str(page_ref + 1).ljust(pagenum_space)
            print(page_toc_prefix + ident + bm_name)
            ident += ident_str
            
            if not args["table_of_contents"]:
                # Add bookmark w/ parent, save as potential parent
                bm = output_pdf.addBookmark(bm_name, page_ref, parent=bm_parent)
                
                # Add to bookmarks list
                bookmark_list.append(bm)
            
            path_list.append(k)
            
            # Do recursion
            iterdict(v, base_path=base_path, empty_parents_in=empty_parents)
            
            if not args["table_of_contents"]:
                temp = bookmark_list.pop()
            temp = path_list.pop()
            
            ident = ident[:-len(ident_str)]
        else:
            # Either it's a file or an empty (placeholder) dir
            if os.path.isdir(filename):
                # It's a totally empty directory, make an "empty" bookmark (no pages/children, references next page)
                
                # Deal with children of empty parents
                empty_parents = empty_parents_in
                is_subdir_of_empty_parent = False
                for empty_parent in empty_parents:
                    if os.path.commonpath([filename, empty_parent]) == empty_parent:
                        is_subdir_of_empty_parent = True
                if is_subdir_of_empty_parent:
                    # Adjust page number forward
                    page_ref += 1
                
                # Prevent referencing non-existent pages
                page_ref = min(page_ref, num_pages - 1)
                
                # Print row of ToC
                page_toc_prefix = pagenum_pre + str(page_ref + 1).ljust(pagenum_space)
                print(page_toc_prefix + ident + bm_name)
                
                if not args["table_of_contents"]:
                    # Add bookmark w/ parent, abandon as potential parent
                    temp = output_pdf.addBookmark(bm_name, page_ref, parent=bm_parent)
            else:
                # It's a file
                page_index = page_list_files.index(filename)
                last_page_index = page_index
iterdict(page_dict, base_path=input_dir)

if not args["table_of_contents"]:
    # Save final PDF
    print("Saving bookmarked PDF '{}'".format(output_file))
    with open(output_file, 'wb') as f:
        output_pdf.write(f)

    # Delete temporary PDF
    print()
    print("Deleting temporary PDF '{}'".format(temp_pdf))
    input_pdf_file.close()
    os.remove(temp_pdf)