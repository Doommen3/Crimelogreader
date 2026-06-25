<div align="center">

# NIU Crime Map

**A PDF-to-map pipeline that turns NIU Police crime-log PDFs into an interactive campus crime map, published monthly in a live newsroom.**

[![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![R](https://img.shields.io/badge/R-276DC3?style=flat&logo=r&logoColor=white)](https://www.r-project.org/)
[![R Shiny](https://img.shields.io/badge/R_Shiny-016DAE?style=flat&logo=rstudioide&logoColor=white)](https://shiny.posit.co/)
[![Leaflet](https://img.shields.io/badge/Leaflet-199900?style=flat&logo=leaflet&logoColor=white)](https://leafletjs.com/)

[Read the newsroom story →](https://northernstar.info/121584/news/northern-star-launches-niu-pd-crime-map/)

</div>

## Overview

NIU Crime Map ingests the daily offense-log PDFs published by the Northern Illinois University Police Department, parses each report into structured records, geocodes the incident locations, and renders them on an interactive Leaflet map served through an R Shiny app. The map ran on a monthly cadence in a live newsroom: the *Northern Star* embedded it in its published crime-log coverage so readers could explore incidents across the DeKalb campus. The repository captures the full production pipeline, including several iterations of the PDF parser developed while reverse-engineering the report layout.

## Features

- **PDF scraping** — downloads daily offense-log PDFs directly from the NIU Public Safety web blotter by date.
- **Layout-aware parsing** — extracts case number, date, offense, location, and disposition from positional word data; multiple parser iterations handle inconsistent report formatting.
- **Geocoding** — resolves campus place names and addresses to latitude/longitude via the Google Maps Geocoding API, with a hardcoded address book for known NIU buildings and lots.
- **Interactive map** — an R Shiny + Leaflet app with filters for offense type, month, and year, and popups that group multiple offenses per location.

## Tech stack

| Layer | Tools |
| --- | --- |
| Scraping | Python, `requests` |
| Parsing | Python, `pdfplumber`, `PyPDF2`, `pandas` |
| Cleaning | R, `tidyverse` |
| Geocoding | Python, `geopy` (Google Maps `GoogleV3`) |
| Mapping | R, `shiny`, `leaflet`, `dplyr`, `readr`, `lubridate` |
| Publishing | Quarto (`crimelog.qmd`), shinyapps.io |

## How it works

The pipeline runs in four stages:

1. **Download** — `crimePdfdownload.py` builds offense-log URLs by date and saves each PDF locally.
2. **Parse** — `pdf_parser.py` (and earlier iterations such as `process2.py` and `crimesprocessing.py`) read the PDFs with `pdfplumber`, group words into rows by their vertical position, assign them to columns by horizontal position, and write structured CSVs. The R script `final_crimelogscript.R` cleans dispositions and normalizes offense labels.
3. **Geocode** — `location_create.py` reads the cleaned CSV and uses the Google Maps Geocoding API (via `geopy`) to attach `Full_Address`, `Latitude`, and `Longitude` to each record, drawing on a lookup table of known campus locations.
4. **Render** — `app.R` loads the geocoded CSV and serves an interactive Shiny + Leaflet map; `crimelog.qmd` embeds the hosted app for newsroom publication.

## Getting started

> The scripts were written for a specific NIU report layout and contain absolute paths and dates from the original runs. Treat the steps below as a best-effort guide; expect to adjust file paths and date ranges for your own data.

### Python scraper and parser

```bash
# Install dependencies
pip install requests pdfplumber pandas geopy

# 1. Download offense-log PDFs (edit the months/year range in the script)
python crimePdfdownload.py

# 2. Parse a PDF into a CSV
python pdf_parser.py 20230920.pdf output.csv

# 3. Geocode the cleaned CSV (requires a Google Maps API key;
#    update the input path and API_KEY inside the script)
python location_create.py
```

### R Shiny app

```r
# Install dependencies
install.packages(c("shiny", "leaflet", "readr", "dplyr", "lubridate"))

# Run the app from the repository root.
# app.R reads updated_crime_data_google_with_coords_combined.csv
shiny::runApp("app.R")
```

The app opens a local Leaflet map of the NIU campus with dropdown filters for offense, month, and year.

## Author

**Devin Oommen** — [devinoommen.com](https://devinoommen.com) · Oommen & Company

## License

Released under the [MIT License](LICENSE).
