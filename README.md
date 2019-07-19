# pdf2images
Convert PDF file to image files **ROBUSTLY**.

# Example
```
$ ./pdf2images.py -h
usage: pdf2images.py [-h] [--max-size MAX_SIZE] pdf_file output_dir

positional arguments:
  pdf_file
  output_dir

optional arguments:
  -h, --help           show this help message and exit
  --max-size MAX_SIZE  max size of either side of the image
```

# Why another "pdf-to-image" package
Once in a while, I need to convert a pdf file (usually slides or academic
paper) into image files (thumbnails) in order to get a fast glance to the
readers without downloading the pdf file.

However, I found all the pdf2image solutions cannot robustly process all the
pdf files, since many pdf files are in non-standard format or come up with
extensions. They are always broken in some cases.

But to look them on the bright side, for any plausible case, there is almost
one of them can process it successfully. 

So I combined (a.k.a. *ensemble*) them together to make it work across most cases.

# Robustness
This package has successfully processed hundreds of thousands of arxiv papers
(for generating thumbnails).

