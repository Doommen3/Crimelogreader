import pdfplumber
import pandas as pd
import re
import os

# List of specified offenses
offenses_list = [
    "Theft Over $500", "Criminal Sexual Assault", "Battery", "Criminal Trespass To Real Property", "Assault",
    "False Police Report", "Domestic Battery", "Aggravated Domestic Battery", "Criminal Damage To Property", "Burglary",
    "Non-consensual Disseminat Private", "Theft $500 and Under", "Theft of Lost or Mislaid Property", "Disorderly Conduct",
    "Stalking", "Fail Notify Damage/Unattended Vehicle", "Tamper w/Sec, Fire, or Life Systems",
    "Illegal Consumption Of Alcohol By", "Aggravated Battery", "Possess Cannabis>10 gm to 100", "Possess Cannabis <10",
    "All Other Disorderly Conduct", "Motor Vehicle Theft", "Mob Action", "Traffic - Illinois Vehicle Code",
    "Possession Of Drug Equipment", "Armed Robbery", "Public Indecency", "Institutional Vandalism",
    "Criminal Trespass To Residence", "Credit Card Fraud", "Fail to Notify Damage/Unattended",
    "Illegal Possession Of Alcohol By Minor", "Harassment By Telephone", "Intimidation", "Leaving Scene Property Damage",
    "Fraud", "Unlawful Use Of Weapon", "Theft From Motor Vehicle", "Out of State Warrant", "Residential Burglary",
    "Deceptive Practices", "All Other Disorderly Conduct Exception", "Harassment through Electronic",
    "Violation Of Orders Of Protection", "Robbery", "Criminal Damage To Govern. Sup.", "Possess/Sale To/From Minors -Tobacco",
    "Criminal Sexual Abuse", "Fail to Notify Damage/Unattended Veh.", "Fail to Notify Damage/Unattended Vehicle",
    "Unauthorized Possession or Storage of Weapons", "Reckless Conduct", "Possess Cannabis>10 gm to 100 gm(Misdemeanor)",
    "Possess Cannabis <10 gm(Ordinance/Civil Viol)", "Purchase/Possess Liquor By Minor", "Aggravated Domestic Battery/Strangle",
    "Domestic Battery/Bodily Harm", "Domestic Battery/Physical Contact", "DPD-Fighting Within The City",
    "Consumption Of Alcohol", "Criminal Trespass To State Sup. Land", "In State Warrant", "Criminal Defacement Of Property",
    "Battery-Domestic", "Telephone Threat", "False Fire Alarm", "Hate Crime", "Bomb Threat", "Aggravated Assault",
    "In-State Warrant", "Failure to Give Notice of Accident", "Unlawful Restraint", "Possess Cannabis <10 gms",
    "Fraudulent Driver's License"
]

# Function to extract offenses from a single page
def extract_offenses_from_page(page):
    text = page.extract_text()
    lines = text.split('\n')
    offenses = []

    for line in lines:
        for offense in offenses_list:
            if offense in line:
                offenses.append({'Offense': offense})

    return offenses

# Function to process all PDFs in a folder
def process_pdfs_in_folder(folder_path):
    all_offenses_data = []

    for filename in os.listdir(folder_path):
        if filename.endswith('.pdf'):
            file_path = os.path.join(folder_path, filename)
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    all_offenses_data.extend(extract_offenses_from_page(page))

    return all_offenses_data

# Define the folder path
folder_path = '/Users/devin/carcrashreader_app/crime_pdfs2'

# Process all PDFs in the folder and extract offenses
offenses_data = process_pdfs_in_folder(folder_path)

# Convert to DataFrame
df = pd.DataFrame(offenses_data)

# Save to CSV
output_csv_path = 'extracted_offenses_from_all_pdfs.csv'
df.to_csv(output_csv_path, index=False)

print(f'Offenses extracted and saved to {output_csv_path}')
