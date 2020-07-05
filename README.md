# bookdir2pdf
Merges a directory structure of images into a PDF with nested bookmarks.

```
usage: bookdir2pdf.py [-h] -i INPUT_DIR [-o OUTPUT_FILE]
                      [-s ORDER_NUMBER_SEPERATOR] [-t]
                      [-p [PURIFY [PURIFY ...]]]

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
  -t, --table_of_contents
                        just scan directory and print table of contents
  -p [PURIFY [PURIFY ...]], --purify [PURIFY [PURIFY ...]]
                        purify scanned B&W page ( greyscale, sharpen,
                        threshold ), named sub-argumets: (sharpen|s)
                        (threshold|t)
```

The PDF here was made using:

`./bookdir2pdf.py -i test_dir/ -s . -p s=1`

The `.` is what seperates the ordering numbers from the bookmark name in the directory name.

The `-p s=1` means to not sharpen, only threshold.

For example, the directory name `01. The First Part` has a `.` between the ordering number `01` and the bookmark name `The First Part`.