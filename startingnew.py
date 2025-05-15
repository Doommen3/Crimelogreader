import pdfplumber
import re
from PyPDF2 import *
import pandas
import pandas as pd
import numpy as np
import os
import csv
from testprocess import *
from crimesprocessing import *


class read_pdf:
    def __init__(self,pdf_data="20230920.pdf"):
        self.reader = PdfReader(pdf_data)

    def pdf_read(self):
        page = self.reader.pages[0].extract_text()
        print(page)
        self.extracted_text = page.split()


if __name__ == '__main__':
    crime_log = "20230920.pdf"
    # Instantiate read pdf object and pass the transcript
    r = read_pdf(crime_log)
    # Call the pdf read function with r object
    r.pdf_read()