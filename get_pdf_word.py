#!/usr/bin/env python
# coding: utf-8

# Fetch text from PDF and Word

import PyPDF2 as PyP
from PyPDF2 import PdfFileReader


def get_info(path):
    with open(path, 'rb') as f:
        pdf = PdfFileReader(f)
        info = pdf.getDocumentInfo()
        number_of_pages = pdf.getNumPages()
    return number_of_pages, info


def get_text_from_pdf(path):
    """ Fetch text from pdf file """
    text = ""
    with open(path, 'rb') as f:
        pdf = PdfFileReader(f)
        number_of_pages = pdf.getNumPages()
        for p in range(number_of_pages):
            page = pdf.getPage(p)
            text += page.extractText()
    return text

def pdf_files(path):
    """ Get a list of PDFs from path """
    import os
    r, d, f = next(os.walk(path))
    pdfer = [file for file in f if file.endswith('.pdf')]
    return pdfer

def get_text_from_word(document):
    """Find all text in a Word document"""
    import sys
    import zipfile
    import re
    from bs4 import BeautifulSoup
    
    with zipfile.ZipFile(document, 'r') as zfp:
        with zfp.open('word/document.xml') as fp:
            soup = BeautifulSoup(fp.read(), 'xml')
    return soup.get_text()





