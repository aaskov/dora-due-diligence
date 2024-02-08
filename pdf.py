#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re
from PyPDF2 import PdfReader


def ReadAndCleanPdfFile(filepath):
    """Read and clean the text content of a PDF file.

    This function reads in the text from a PDF file and returns the cleaned
    text (assuming everything is in English).


    Parameters
    ----------
    filepath : strig
        The filepath to the file that is going to be read.

    Returns
    -------
    text : string
        The cleaned content of the PDF file

    """

    print('Reading text from file')
    reader = PdfReader(filepath)

    print('Extracting text from pages')
    text = ""
    for i in range(len(reader.pages)):
        text += reader.pages[i].extract_text()

    print('Cleaning extracted content')
    # Removes non special Unicode chars
    text = "".join([i if ord(i) < 128 else ' ' for i in text])

    # Replaces new-line chars whit whitespace
    text = re.sub(r'\n',' ', text)

    # Replace consecutive whitespace chars with a single withspace
    text = re.sub(r'[\s]+', ' ', text)

    return(text)
