# nested-pdf-merge
 Merges a directory structure of images into a PDF with nested bookmarks.

The PDF here was made using:
`./nested-pdf-merge.py -i test_dir/ -s "."`
The `"."` is what seperates the ordering numbers from the bookmark name in the directory name.
For example, `01. The First Part` has a `.` between the ordering number `01` and the bookmark name `The First Part`.