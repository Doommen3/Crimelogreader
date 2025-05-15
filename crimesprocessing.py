import pandas
import pandas as pd
import numpy as np
from crimesreader import *
import re

class ProcessGrades:
    def __init__(self):
        """Constructors for Process Grades object"""

        # Set grades list variable to list passed into object
        self.grades_list = None
        # Create empty list
        self.complete_myframe = []
        # Create variable for cleaned list
        self.cleaned = None
        self.futureList = []
        self.startWords = ["WEATHER", "TOTALS", "TYPE", "CLASS OF CITY", "ROAD SURFACE CONDITION"]
        self.startIndex = []
        self.grades_list_copy = None
        self.endIndex = []
        self.endWordIndex = []
        self.endWords = ["Rd", "Ln", "St", "Suspended", "Cleared", "Closed", "Agency", "Open"]


    def complete_line_of_lists(self, line_of_list):
        """add line of list to the complete list """

        self.complete_myframe.append(line_of_list)

    def getFrame(self):
        """Returns a complete list"""
        return self.complete_myframe

    def contains_letter_followed_by_number(self, s):
        pattern = r'[a-zA-Z]\d'
        return bool(re.search(pattern, s))

    def process_classes(self, grades_list):

        self.grades_list = grades_list
        self.grades_list_copy = self.grades_list
        self.slice_list(self.grades_list)
        index_list = []
        index_list_two = []
        new_list = []

        for item in self.grades_list:
            if "," in item:
                str(item).replace(",", "")



    def slice_list(self, input_list):
        standalone_number_pattern = r'(?<!\d)(\d{12})(?!\d)'
        standalone_number_pattern_two = r'(?<!\d)(\d{13})(?!\d)'
        date_plus_number_pattern = r'(\d{1,2}/\d{1,2}/\d{4})(\d{12})'
        letter_plus_number_pattern = r'([a-zA-Z])(\d{12})'
        print(f"this is input {input_list}")

        # Clean the list: remove commas and separate numbers from preceding letters or dates
        cleaned_list = []
        for item in input_list:
            item = item.replace(",", "")
            # Check for dates followed by numbers without space
            date_matches = re.findall(date_plus_number_pattern, item)
            for date, number in date_matches:
                item = item.replace(date + number, date + ' ' + number)
            # Check for letters followed by numbers without space
            letter_matches = re.findall(letter_plus_number_pattern, item)
            for letter, number in letter_matches:
                item = item.replace(letter + number, letter + ' ' + number)
            cleaned_list.append(item)

        # Initialize indices lists
        start_index = []
        end_index = []
        end_words_index = []
        # Find indices of 12-digit numbers and end words
        for item_index, item in enumerate(cleaned_list):
            # Find standalone 12-digit numbers
            matches = re.findall(standalone_number_pattern, item)
            matches2 = re.findall(standalone_number_pattern_two, item)
            for match in matches:
                start_index.append(item_index)
            for match in matches2:
                start_index.append(item_index)

            # Find indices where end words appear
            if any(word in item for word in self.endWords):
                end_words_index.append(item_index)


        for i in range(len(cleaned_list) -1, -1, -1):
            input = cleaned_list[i]
            index = input.rfind("The")
            if index == 0:
                end_index = i

        (print(f"this is messing up? {start_index}"))
        print(f"this is messing up end index {end_words_index}")
        start_index_length = len(start_index)
        counter = 0
        print(f"this is cleaned list {cleaned_list}")
        if len(start_index) > 1:
            print(f"this is my note {len(start_index)}")

            # slice the string from the first 12 digit number until the next 12 digit number
            while counter < len(start_index):
                print(f"this is counter {counter}")
                if counter < len(start_index) - 1:
                    for item in range(0, len(start_index)):

                        if item < len(start_index) - 1:
                            print(f"this is item {item}")


                            if start_index[item] < end_words_index[item]:
                                sliced_str = cleaned_list[start_index[item]: start_index[item] + 17]
                                self.complete_line_of_lists(sliced_str)
                                print(f"this is the problem sliced sliced {sliced_str}")
                                print(cleaned_list[start_index[item]])
                                print(cleaned_list[end_words_index[item]])
                            counter += 1
                            if len(end_words_index) > 1 and start_index[item] > end_words_index[item]:
                                digit = 1

                                if start_index[item] > end_words_index[item] and item < len(end_words_index):
                                    while start_index[item] > end_words_index[item + digit]:
                                        digit += 1
                                if start_index[item] < end_words_index[item + digit]:
                                    sliced_str = cleaned_list[start_index[item]:  start_index[item] + 17]
                                    self.complete_line_of_lists(sliced_str)
                                    print(f"this is the problem sliced specific sliced {sliced_str}")
                                    print(cleaned_list[start_index[item]])
                                    print(cleaned_list[end_words_index[item]])

                            if len(end_words_index) == 1:
                                print(f"this is true")
                                if start_index[item] > end_words_index[item] :
                                    sliced_str = cleaned_list[start_index[item]: start_index[item] + 17]
                                    self.complete_line_of_lists(sliced_str)
                                    print(f"this is the problem sliced sliced {sliced_str}")
                                    print(cleaned_list[start_index[item]])
                                    print(cleaned_list[end_words_index[item]])

                            if len(end_words_index) == 0:
                                print(f"this is the test {start_index[item]}")
                                print(f"this is end test {end_words_index[item]}")
                                print(f"this is end test length {len(end_words_index)}")
                                print(f"this is end test index {end_words_index}")
                                sliced_str = cleaned_list[start_index[item]: end_words_index[item + 1]]
                                self.complete_line_of_lists(sliced_str)
                                print(f"this is the problem sliced sliced {sliced_str}")
                                print(cleaned_list[start_index[item]])
                                print(cleaned_list[end_words_index[item]])


                        # at the last 12 digit number slice the string until the index of the word "The"
                        print(f"endindex {end_index}")
                        if item == len(start_index) - 1:
                            sliced_str = cleaned_list[start_index[item]: ]
                            self.complete_line_of_lists(sliced_str)
                            print(f"this is sliced {sliced_str}")
                            counter += 1
                        if item == len(start_index) - 1 and end_index is []:
                            sliced_str = cleaned_list[start_index[item]:]
                            self.complete_line_of_lists(sliced_str)
                            counter += 1




        if len(start_index) < 2:
            for item in range(0, len(start_index)):

                sliced_str = cleaned_list[start_index[item]: start_index[item] + 17]
                self.complete_line_of_lists(sliced_str)
                print(f"this is sliced {sliced_str}")



