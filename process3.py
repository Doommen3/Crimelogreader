from PyPDF2 import *


class read_pdf:

    def __init__(self, pdf_data="unofficial_transcript.pdf"):
        self.reader = PdfReader(pdf_data)
        self.num_pages = len(self.reader.pages)
        self.process = None
        self.complete_myframe = []
        self.extracted_text = None
        self.full_list = []
        self.list_to_process = []
        self.startIndex = []
        self.startWords = []
        self.list_to_send = []

    def updateProcess(self, process):
        """Sets the self.process variable to the list pass through parameter"""
        self.process = process
        self.con = True

        # Calls the process_classes method from ProcesGrades and passes a list

    def pdf_read(self):
        """Reads a pdf file"""

        # Iterates through each page in the pdf
        for page_num in range(0, self.num_pages):

            # Stores text extracted from the file to the page variable
            page = (self.reader.pages[page_num]).extract_text(Tj_sep=" ")
            print(page)

            # Splits the text from the page variable into a group of lists and stores it in the extracted_text variable
            self.extracted_text = page.split()

            for num in range(0, len(self.extracted_text)):
                self.full_list.append(self.extracted_text[num])
        print(self.full_list)

  #     for item in range(0, len(self.full_list)):
  #         if self.full_list[item] in self.startWords:
  #             self.startIndex.append(item)
  #
  #     for item2 in range(0, len(self.startIndex)):
  #         if item2 < len(self.startIndex) - 1:
  #             process = self.full_list[self.startIndex[item2]: self.startIndex[item2 + 1]]
  #             for num1 in range(0, len(process)):
  #                 self.list_to_send.append(process[num1])
  #         if item2 == len(self.startIndex) - 1:
  #             process = self.full_list[self.startIndex[item2]: ]
  #             for num1 in range(0, len(process)):
  #                 self.list_to_send.append(process[num1])
  #

if __name__ == '__main__':
    transcript = "/Users/devin/carcrashreader_app/crime_pdfs/20230802.pdf"
    # Instantiate read pdf object and pass the transcript
    r = read_pdf(transcript)
    # Call the pdf read function with r object
    r.pdf_read()