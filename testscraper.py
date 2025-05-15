import pdfplumber
import pandas as pd

# Open the PDF file
pdf_path = '/Users/devin/carcrashreader_app/crime_pdfs2/0424/20240411.pdf'
data = []

with pdfplumber.open(pdf_path) as pdf:
    for page_number, page in enumerate(pdf.pages, start=1):
        # Extract text boxes
        text_boxes = page.extract_words()

        for box in text_boxes:
            data.append({
                "text": box['text'],
                "x0": box['x0'],
                "y0": box['top'],
                "x1": box['x1'],
                "y1": box['bottom'],
                "page": page_number
            })

# Create a DataFrame
df = pd.DataFrame(data)
df.to_csv('test.csv')
print(df)
