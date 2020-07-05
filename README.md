# bookdir2pdf
Merges a directory structure of images into a PDF with nested bookmarks.

```
$ bookdir2pdf.py --help

usage: bookdir2pdf.py [-h] -i INPUT_DIR [-o OUTPUT_FILE]
                      [-s ORDER_NUMBER_SEPERATOR] [-c]
                      [-p [PURIFY [PURIFY ...]]] [-d DPI] [-t TITLE]
                      [-a AUTHOR]

Merge nested image direcotry into PDF with nested bookmarks.

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT_DIR, --input_dir INPUT_DIR
                        path to nested image directory to merge
  -o OUTPUT_FILE, --output_file OUTPUT_FILE
                        output file path ( defaults to [input_dir].pdf )
  -s ORDER_NUMBER_SEPERATOR, --order_number_seperator ORDER_NUMBER_SEPERATOR
                        the character used to seperate the direcotry ordering
                        numbers from the bookmark names ( like '.' or ')' )
  -c, --table_of_contents
                        just scan directory and print table of contents
  -p [PURIFY [PURIFY ...]], --purify [PURIFY [PURIFY ...]]
                        purify scanned B&W page ( greyscale, sharpen,
                        threshold ), named sub-argumets: (sharpen|s)
                        (threshold|t)
  -d DPI, --dpi DPI     dots-per-inch of the input images
  -t TITLE, --title TITLE
                        the PDF title ( defaults to the directory basename )
  -a AUTHOR, --author AUTHOR
                        the PDF author ( defaults to 'bookdir2pdf', pass ''
                        for no author )
```

The PDF here was made using:

`bookdir2pdf.py --input_dir test_dir/ --order_number_seperator . --purify sharpen=1 --title "Example PDF" --dpi 72`

The `.` is what seperates the ordering numbers from the bookmark name in the directory name. For example, the directory name `01. The First Part` has a `.` between the ordering number `01` and the bookmark name `The First Part`.

The `sharpen=1` means not to sharpen during the purification step.

The bookmark structure can be previewed without actually processing any files:

```
$ bookdir2pdf.py --input_dir test_dir/ --table_of_contents

... [output removed] ...

Example PDF - Table of Contents
-------------------------------
Page #1    Cover Page
Page #2    --- Empty Directory Example #1
Page #2    --- --- Nested Empty Directory Level 1
Page #2    --- --- --- Nested Empty Directory Level 2
Page #2    --- --- --- --- Nested Empty Directory Level 3
Page #2    Empty Directory Example #2
Page #2    The First Part
Page #2    --- Chapter 1
Page #4    --- Chapter 2
Page #6    The Middle Part
Page #6    --- Chapter 3
Page #8    --- Chapter 4
Page #10   The Final Part
Page #10   --- Chapter 5
Page #12   --- Chapter 6