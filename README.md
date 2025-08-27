# Crime Log Parser

This repository contains scripts for downloading crime log PDFs and converting them into structured CSV files.

## Key scripts
- `crimePdfdownload.py` – optional helper to download PDFs from the source website.
- `pdf_parser.py` – parses a crime log PDF into a CSV using positional data from each word.

The remaining `.csv`, `.txt`, `.R`, and older prototype scripts were intermediate artifacts from earlier experiments and can be removed once you migrate to the new parser.

## Usage
```bash
python pdf_parser.py 20230920.pdf output.csv
```
The script expects the `pdfplumber` package. Install it with `pip install pdfplumber`.
