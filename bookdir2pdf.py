#!/usr/bin/env python3

import argparse, os, sys
from pathlib import Path
import re

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

PROG_FILE_NAME = os.path.splitext(os.path.basename(PROG_FILE))[0]

# Get path that the command was called from
COMMAND_PATH = Path().absolute()

# Parse arguments before running main program
def dir_path(string):
    if os.path.isdir(string):
        return string
    else:
        raise NotADirectoryError(string)

# TODO: Add usage examples
ap = argparse.ArgumentParser(description="Merge nested image direcotry into PDF with nested bookmarks.")
ap.add_argument("-i", "--input_dir", type=dir_path, required=True,
    help="path to nested image directory to merge")
ap.add_argument("-o", "--output_file", type=str, default=None,
    help="output file path ( defaults to [input_dir].pdf )")
ap.add_argument("-s", "--order_number_seperator", type=str, default=None,
    help="the character used to seperate the direcotry ordering numbers from the bookmark names ( like '.' or ')' )")
ap.add_argument("-c", "--table_of_contents", action="store_true",
    help="just scan directory and print table of contents")
ap.add_argument("-p", "--purify", action="store", default=None, nargs="*", type=str, 
    help="purify scanned B&W page ( greyscale, sharpen, threshold ), named sub-argumets: (sharpen|s) (threshold|t)")
ap.add_argument("-d", "--dpi", type=int, default=300,
    help="dots-per-inch of the input images")
ap.add_argument("-t", "--title", type=str, default=None,
    help="the PDF title ( defaults to the directory basename )")
ap.add_argument("-a", "--author", type=str, default=None,
    help="the PDF author ( defaults to '{}', pass '' for no author )".format(PROG_FILE_NAME))
args = vars(ap.parse_args())

print()

# Resolve input dir into absolute path (relative to working directory!)
input_dir = args["input_dir"]
input_dir = os.path.realpath(input_dir)
if not os.path.isabs(input_dir):
    input_dir_split = input_dir.split(os.path.sep)
    if input_dir_split[0] == os.path.curdir:
        input_dir = os.path.sep.join(input_dir_split[1:])
    input_dir = os.path.join(COMMAND_PATH, input_dir)

input_dir_name = input_dir.strip(os.path.sep).split(os.path.sep)[-1]

# Get main directory
main_dir = os.path.sep.join(input_dir.rstrip(os.path.sep).split(os.path.sep)[:-1])

# Limit DPI
if args["dpi"] != None:
    if (args["dpi"] < 72) or (args["dpi"] > 4800):
        raise argparse.ArgumentTypeError("DPI must be 72 <= DPI <= 4800.")

# Test if/which purify flavor is being used
if args["purify"] != None:
    purify = True
    purify_args = args["purify"]
else:
    purify = False
    purify_args = ()

# Do not purify if --table_of_contents is set
if args["table_of_contents"]:
    purify = False

# Parse purify sub-arguments (values)
if purify:
    # Defaults
    sharpen_factor = 2
    thresh_setting = 170
    
    for p_arg in purify_args:
        p_arg_split = p_arg.split("=")
        
        # Only allow [string]=[string]
        if len(p_arg_split) != 2:
            raise argparse.ArgumentTypeError("Invalid argument format. Use arg_name=arg_value.")

        # Get name and value seperately
        p_arg_name, p_arg_value = [x.lower().strip() for x in p_arg_split]

        # Parse purify named sub-arguments
        if p_arg_name in ["sharpen", "s"]:
            # Test if it's a float and set
            worked = True
            try:
                sharpen_factor = float(p_arg_value)
            except(ValueError):
                worked = False
            
            # Test if it's greater than 0
            if sharpen_factor <= 0:
                worked = False
            
            if not worked:
                raise argparse.ArgumentTypeError("(--purify | -p) sharpness must be a float greater than 0.")
        elif p_arg_name in ["threshold", "t"]:
            # Test if it's a float and set
            worked = True
            try:
                thresh_setting = float(p_arg_value)
            except(ValueError):
                worked = False
            
            # Test if it's positive
            if thresh_setting < 0:
                worked = False
            
            # Test if it's <= 255
            if thresh_setting > 255:
                worked = False
            
            if not worked:
                raise argparse.ArgumentTypeError("(--purify | -p) threshold must be a positive float <= 255.")
        else:
            raise argparse.ArgumentTypeError("'{}' is not a valid option for (--purify | -p).".format(p_arg_name))
    
    print("Will purify with a sharpening amount of {} and a threshold of {}.".format(sharpen_factor, thresh_setting))
    print()

if args["table_of_contents"] and args["purify"] != None:
    print("[WARNING]: Both (--purify|-p) and (--table_of_contents|-c) arguments were passed, will not purify images.")

# Set PDF title
if args["title"] != None:
    pdf_title = args["title"]
    print()
    if len(pdf_title) <= 0:
        print("PDF will have no title.")
    else:
        print("PDF title will be set to '{}'".format(pdf_title))
else:
    pdf_title = input_dir_name

# Set PDF author
if args["author"] != None:
    pdf_author = args["author"].strip()
    print()
    if len(pdf_author) <= 0:
        print("PDF will have no author.")
    else:
        print("PDF author will be set to '{}'".format(pdf_author))
else:
    pdf_author = PROG_FILE_NAME

def get_valid_filename(s):
    s = str(s).strip()
    return re.sub(r'(?u)[^-\w.\ ,\!\'\&]', '_', s)

if args["table_of_contents"]:
    print("Will only print the Table of Contents, will NOT process images or save PDF.")
else:
    # Resolve output filename
    if args["output_file"] == None:
        #TODO: Default to title if possible
        pdf_title_safe_filename = get_valid_filename(pdf_title)
        output_file = os.path.join(main_dir, pdf_title_safe_filename) + os.path.extsep + "pdf"
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
    
    output_file = os.path.realpath(output_file)
    
    # Print target filename
    if args["output_file"] == None:
        print("No output filename supplied, using '{}'".format(output_file))
    else:
        print("Will save PDF as '{}'".format(output_file))
    
    output_file_dir, output_file_name = os.path.split(output_file)

# Do main imports
import img2pdf
from PIL import Image, ImageEnhance
from collections import OrderedDict
from PyPDF2 import PdfFileWriter, PdfFileReader
import shutil

print()
print("Scanning input directory...")

# Walk though folder structure (recursive alphabetical, include all files/folders)
input_dir_list = [str(p) for p in sorted(Path(input_dir).glob('**/*'))]

# Set file extentions to ignore
ignored_file_exts = [".ignore", ".db"]

# Set valid image extentions
page_exts = [".jpg", ".jpeg", ".png", ".gif"]

# Set rename extentions
rename_exts = [".rename", ".name", ".title"]

valid_exts = ignored_file_exts + page_exts + rename_exts
ignored_file_exts += rename_exts

# Prefix to prepend to temporary file/folder names
temp_name_prepend = "__temp__"

# Make final input dir names
if purify:
    # Make temp directory name
    final_input_dir_name = temp_name_prepend + input_dir_name
    final_input_dir = os.path.join(main_dir, final_input_dir_name)
else:
    # The original directories
    final_input_dir = input_dir
    final_input_dir_name = input_dir_name  

# Save image paths (and empty/ignored-file dirs) paths to ordered list
page_list = list()
# Make dict with rename (dir, bm_name)
page_dir_rename_dict = dict()
for p in input_dir_list:
    if os.path.isfile(p):
        # Check if it's an invalid extention, and if so, fully ignore it
        p_path, p_filename = os.path.split(p)
        p_basename, p_ext = os.path.splitext(p_filename)
        p_ext = p_ext.lower()
        if p_ext == "":
            # No name, just extention
            p_ext = p_basename
        
        if p_ext not in valid_exts:
            print("[WARNING]: Unsupported file, ignoring: '{}'".format(p))
            continue
        
        # Test if it should be ignored, and if so, fully ignore it
        if p_ext in ignored_file_exts:
            if p_ext not in rename_exts:
                # Don't print if it's a rename file (not really ignoring per-se)
                print("Ignoring file: '{}'".format(p))
            continue
            
        page_list.append(p)
    elif os.path.isdir(p):
        # Get files and directories inside p
        p_list = [os.path.realpath(str(x)) for x in sorted(Path(p).glob('*'))]
        p_dir_list = [x for x in p_list if os.path.isdir(x)]
        p_file_list = [x for x in p_list if os.path.isfile(x)]
        
        # Make file list without ignored files
        p_file_list_ignored = list()
        # Also update page_dir_rename_dict
        for x in p_file_list:
            x_path, x_filename = os.path.split(x)
            x_basename, x_ext = os.path.splitext(x_filename)
            x_ext = x_ext.lower()
            if x_ext == "":
                # No name, just extention
                x_ext = x_basename
            
            # Check if it's a valid extention
            if x_ext in valid_exts:
                # If not ignored file, append to file list
                if x_ext not in ignored_file_exts:
                    p_file_list_ignored.append(x)
                # If it's a rename file, parse and append to rename dict
                if x_ext in rename_exts:
                    # If purify, make sure it's referencing the final input dir
                    if purify:
                        relative_x_path = os.path.relpath(x_path, input_dir)
                        rename_dir = os.path.join(final_input_dir, relative_x_path)
                    else:
                        rename_dir = x_path
                    
                    # Parse .rename files
                    with open(x) as f:
                        rename_file_contents = f.read()
                    
                    rename_name = rename_file_contents.strip().split("\n")[0].strip()
                    
                    page_dir_rename_dict[rename_dir] = rename_name
        
        # Test if it's empty or contains only ignored files
        if len(p_dir_list) <= 0 and len(p_file_list_ignored) <= 0:
            # Add path (used to make "empty" bookmarks)
            page_list.append(p)

# Run purification (save to temporary directory)
if purify:
    print()
    print("Purifying pages...")
    
    # Delete temp dir (or file with same name) if it already exists
    if os.path.exists(final_input_dir):
        if os.path.isdir(final_input_dir):
            shutil.rmtree(final_input_dir)
        elif os.path.isfile(final_input_dir):
            os.remove(final_input_dir)
    
    # Create new page_list
    new_page_list = list()
    new_page_list_dirs = list()
    new_page_list_files = list()
    for p in page_list:
        # Make final_p (replace input_dir with final_input_dir)
        rel_p = os.path.relpath(p, input_dir)
        final_p = os.path.join(final_input_dir, rel_p)
        new_page_list.append(final_p)
        if os.path.isdir(p):
            new_page_list_dirs.append(final_p)
        else:
            new_page_list_files.append(final_p)
    
    # Make all directories first
    for p in new_page_list_dirs:
        Path(p).mkdir(parents=True, exist_ok=True)
    for p in new_page_list_files:
        Path(os.path.dirname(p)).mkdir(parents=True, exist_ok=True)
    
    # Process image files
    for x, p in enumerate(page_list):
        final_p = new_page_list[x]
        if os.path.isfile(p):
            # It's an image file
            with Image.open(p) as page_im:
                if purify:
                    print("\tPurifying '{}'".format(p))
                    # Make greyscale
                    gray = page_im.convert('L')
                    
                    # Sharpen 
                    enhancer = ImageEnhance.Sharpness(gray)
                    sharpen = enhancer.enhance(sharpen_factor)
                    
                    # Apply threshold
                    thresh = sharpen.point(lambda p: p > thresh_setting and 255)  
                    
                    # Make 1 bit
                    final_page_im = thresh.convert('1')
                else:
                    final_page_im = page_im
            
            # Save image
            final_page_im.save(final_p, "PNG")

    # Update page_list with new images/paths
    page_list = new_page_list

# Make page_list but with only files
page_list_files = [p for p in page_list if os.path.isfile(p)]

# Get size from first page
with Image.open(page_list_files[0]) as cover:
    width, height = cover.size

# Get number of pages
num_pages = len(page_list_files)

# Create nested ordered dictionary from list
page_dict = OrderedDict()
for p in page_list:
    p = os.path.relpath(p, final_input_dir) # Make relative
    current_level = page_dict
    for part in p.split(os.path.sep):
        if part not in current_level:
            current_level[part] = OrderedDict()
        current_level = current_level[part]

if not args["table_of_contents"]:
    # Create PDF from page_list(no bookmarks)
    print()
    temp_pdf = os.path.join(output_file_dir, temp_name_prepend + output_file_name)
    print("Saving temporary PDF '{}'".format(temp_pdf))
    with open(temp_pdf, "wb") as f:
        f.write(img2pdf.convert(page_list_files, dpi=args["dpi"]))
    
    # Load PDF into PyPDF2
    print()
    print("Loading temporary PDF into editing library...")
    output_pdf = PdfFileWriter()
    input_pdf_file = open(temp_pdf, 'rb')
    input_pdf = PdfFileReader(input_pdf_file)
    output_pdf.appendPagesFromReader(input_pdf)

# Add nested bookmarks from page_dict
print()
if args["table_of_contents"]:
    toc_title = pdf_title + " - Table of Contents"
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
        filepath = os.path.join(base_path, os.path.sep.join(path_list))
        filename = os.path.join(filepath, k)
        filename = os.path.realpath(filename)
        
        # Get parent bookmark
        if len(bookmark_list) > 0:
            bm_parent = bookmark_list[-1]
        else:
            bm_parent = None
        
        # Get bookmark name
        if filename in page_dir_rename_dict:
            # Name is defined in a rename file
            bm_name = page_dir_rename_dict[filename]
        elif args["order_number_seperator"] != None:
            # Remove leading order numbers from dir name
            bm_name = args["order_number_seperator"].join(k.split(args["order_number_seperator"])[1:]).strip(" ")
        else:
            bm_name = k
        
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
iterdict(page_dict, base_path=final_input_dir)

if not args["table_of_contents"]:
    # Add metadata to PDF
    output_pdf.addMetadata({
        '/Title': pdf_title,
        '/Author': pdf_author
        })
    
    # Save final PDF
    print("Saving bookmarked PDF '{}'".format(output_file))
    with open(output_file, 'wb') as f:
        output_pdf.write(f)

    # Delete temporary PDF
    print()
    print("Deleting temporary PDF '{}'".format(temp_pdf))
    input_pdf_file.close()
    os.remove(temp_pdf)

if purify and (os.path.realpath(final_input_dir) != os.path.realpath(input_dir)):
    print()
    print("Delete temporary directory '{}'".format(final_input_dir))
    shutil.rmtree(final_input_dir)