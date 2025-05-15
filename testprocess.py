import pandas as pd
import re
from scratch import *


class ProcessCrashes:
    def __init__(self):
        self.complete_frame = pd.DataFrame()
        self.last_full_case = {}
        self.current_offense = None  # To store the current offense until the disposition is found
        self.relevant_pattern = ""
        self.disposition_date = None
        self.disposition = None
        self.previous_line = None
        self.next_line = None

    def process_crashes(self, text_lines):
        data = {
            'Case Number': [], 'Offense': [], 'Date Reported': [], 'Time Reported': [],
            'Date Occurred': [], 'Time Occurred': [], 'Location': [],
            'Disposition': [], 'Disposition Date': [], 'Location Address': []
        }
        temp_line = ""  # Temporary storage for building complete lines

        disposition_pattern = [
            r"(Suspended)\s+(\d{1,2}/\d{1,2}/\d{4})",
            r"(Open)\s+(\d{1,2}/\d{1,2}/\d{4})",
            r"(Closed By)\s+(\d{1,2}/\d{1,2}/\d{4})",
            r"(Unfounded)\s+(\d{1,2}/\d{1,2}/\d{4})",
            r"(Referred To)\s+(\d{1,2}/\d{1,2}/\d{4})",
            r"(Cleared - Adult)\s+(\d{1,2}/\d{1,2}/\d{4})",
            r"(Closed by)\s+(\d{1,2}/\d{1,2}/\d{4})",
            r"(Cleared -)\s+(\d{1,2}/\d{1,2}/\d{4})"

        ]

        non_relevant_patterns = [
            r"Daily Crime Log", r"NIU Department of Police and Public Safety", r"Log Entry Date:", r"Calendar Year:",
            r"Case Number Offense Date / Time",
            r"The Department of Public Safety discloses offense and arrest information in accordance with state and federal law. Page 1 of 1",
            r"Exception", "Arrest"
        ]

        relevant_patterns = [r"\bTheft Over \$500\b", r"\bCriminal Sexual Assault\b",
                             r"\bCriminal Trespass To Real Property\b",
                             r"Criminal Trespass to Real Property Arrest",
                             r"\bAssault\b",
                             r"\bFalse Police Report\b", r"\bDomestic Battery\b", r"\bBattery\b",
                             r"\bCriminal Damage To Property\b", r"\bBurglary\b",
                             r"\bNon-consensual Disseminat Private\b", r"\bTheft \$500 and Under\b",
                             r"\bTheft of Lost or Mislaid Property\b", r"\bDisorderly Conduct\b",
                             r"\bStalking\b", r"\bFail Notify Damage/Unatteded Vehicle\b",
                             r"\bTamper w/Sec, Fire, or Life Systems\b",
                             r"\bIllegal Consumption Of Alcohol By\b", r"\bAggravated Battery\b",
                             r"\bPossess Cannabis>10 gm to 100\b", r"\bPossess Cannabis <10\b",
                             r"\bAll Other Disorderly Conduct\b", r"\bMotor Vehicle Theft\b",
                             r"\bMob Action\b", r"\bTraffic - Illinois Vehicle Code\b", r"\bArmed Robbery\b",
                             r"\bPublic Indecency\b", r"\bInstitutional Vandalism\b",
                             r"\bCriminal Trespass To Residence\b", r"\bCredit Card Fraud\b",
                             r"\bFail to Notify Damage/Unattended\b", r"\bIllegal Possession Of Alcohol By Minor\b",
                             r"\bHarassment By Telephone\b", r"\bIntimidation\b", r"\bLeaving Scene Property Damage\b",
                             r"\bFraud\b", r"\bUnlawful Use Of Weapon\b", r"\bTheft From Motor Vehicle\b",
                             r"\bOut of State Warrant\b", r"\bResidential Burglary\b", r"\bDeceptive Practices\b",
                             r"\bHarassment through Electronic\b", r"\bIllegal Possession Of Alcohol By\b",
                             r"\bViolation Of Orders Of Protection\b", r"\bRobbery\b",
                             r"\bCriminal Damage To Govern. Sup.\b",
                             r"\bPossess/Sale To/From Minors -Tobacco\b",
                             r"\bAggravated Domestic Battery\b",
                             r"\bFail to Notify Damage/Unattended Veh.\b",
                             r"\bPossess Cannabis>10 gm to 100 gm(Misdemeanor) Closed By 10/14/2023\b",
                             r"\bPossess Cannabis <10 gm(Ordinance/Civil Viol)\b",
                             r"\bPurchase/Possess Liquor By Minor\b",
                             r"\bAggravated Domestic Battery/Strangle\b",
                             r"\bDPD-Fighting Within The City\b", r"\bConsumption Of Alcohol\b",
                             r"\bCriminal Trespass To State Sup. Land\b",
                             r"\bCriminal Damage to Property\b", r"\bCriminal Sexual Abuse\b",
                             r"\bIn State Warrant\b", r"\bCriminal Defacement Of Property\b",
                             r"\bReckless Conduct\b", r"\bPossession Of Drug Equipment\b",
                             r"\bBattery-Domestic\b", r"\bTelephone Threat\b", r"\bFalse Fire Alarm\b",
                             r"\bHate Crime\b", r"\bBomb Threat\b", r"\bAggravated Assault\b",
                             r"\bIn-State Warrant\b", r"\bUnauthorized Possession or Storage of\b",
                             r"\bFailure to Give Notice of Accident\b", r"\bUnlawful Restraint\b",
                             r"\bPossess Cannabis <10 gms\b", r"\bFraudulent Driver's License\b",
                             r"Unauthor. Videotaping/Live Vid.",
                             r"Reckless Conduct", r"All Other Disorderly Conduct Exception",
                             r"Home Invasion",
                             r"\bBurglary Arrest\b"]

        for line_group in text_lines:
            print(f' this is line group {line_group}')
            for line in line_group:
                print(f'this is line {line}')
                line = line.strip()

                if line == "Burglary Arrest":
                    print(f' this is burglary arrest')
                    self.relevant_pattern = line
                    self.add_data_entry(data)
                # Skip non-relevant lines

                if any(re.search(pattern, line) for pattern in non_relevant_patterns):
                    continue

                print(f"this is line 1 {line}")
                if re.match(r"^\d{12,}", line):  # New case entry
                    #if not re.search(r"(am|pm).*" + disposition_pattern, line, re.IGNORECASE):
                    print(f'this is line 2 {line}')
                    self.current_offense = None  # Reset current offense for new case
                    self.parse_line(line, data)

                matches = re.findall(r"(Open|Closed By|Suspended|Unfounded|Referred to|Cleared - Adult|Closed by|Referred To|Arrest|Cleared -|Referred To Other Agency|Referred)", line)
                disposition = matches[0] if matches else None
                print(f'this is dispo{disposition}')
                new_disposition = disposition
                self.last_full_case['Disposition'] = new_disposition

                if disposition is not None and len(line) == len(disposition):
                    print(f'this is length of disposition line {len(line)}')
                    print(f'this is the length of disposition {len(disposition)}')
                    self.relevant_pattern = self.previous_line
                    self.current_offense = self.relevant_pattern
                    print(f'this is only a disposition')
                    self.add_data_entry(data)

                elif (disposition is not None and any(re.search(pattern, line) for pattern in relevant_patterns)
                      and not re.match(r"^\d{12,}", line)):
                    print(f'this line has a dispo and something else')
                    match = re.search(disposition, line)
                    self.relevant_pattern = line[0:match.start()]
                    self.add_data_entry(data)

                elif any(re.search(pattern, line) for pattern in disposition_pattern) and not re.match(r"^\d{12,}", line):
                    print(f"this is line 3 {line}")
                    print(f'this is length of line {len(line)}')

                    self.current_offense = self.relevant_pattern
                    date_pattern = re.compile(r'\d{1,2}/\d{1,2}/\d{4}')
                    dates = [(m.group(), m.start()) for m in date_pattern.finditer(line)]

                    if dates:

                        disposition_date = dates[-1][0]
                        self.disposition_date = disposition_date

                        matches = re.findall(r"(Open|Closed By|Suspended|Unfounded|Referred to|Cleared - Adult|Closed by|Referred To|Arrest|Cleared -)", line)
                        disposition = matches[0] if matches else None

                        if disposition is not None:
                            if len(line) > len(disposition_date + disposition) + 1:
                                match = re.search(disposition, line)

                                self.relevant_pattern = line[0: match.start()]
                                print(f'this is match{self.relevant_pattern}')

                                #else:

                                #if self.previous_line:

                            elif (not re.search(r"^\d{12,}", self.previous_line) and
                                  not any(re.search(pattern, self.previous_line, re.IGNORECASE) for pattern in
                                          disposition_pattern)):
                                relevant_patterns.append(self.previous_line)
                                print(f'appending to relevant pattern')
                                self.relevant_pattern = self.previous_line
                                self.current_offense = self.relevant_pattern
                                print(f"This is relevant pattern 2: {self.relevant_pattern}")

                    else:
                        matches = re.findall(r"(Open|Closed By|Suspended|Unfounded|Referred to|Cleared - Adult|Closed by|Referred To|Arrest|Cleared -)", line)
                        disposition = matches[0] if matches else None

                        if disposition is not None:
                            if any(
                                    re.search(pattern, self.previous_line, re.IGNORECASE) for pattern in
                                    relevant_patterns) and not re.search(
                                r"^\d{12,}", self.previous_line) and not any(
                                re.search(pattern, self.previous_line, re.IGNORECASE) for pattern in
                                disposition_pattern):
                                print(f'this is relevant pattern line {line}')
                                self.relevant_pattern = line

                    #self.add_data_entry(data)
                    self.add_data_entry(data)
                    print(f'adding an entry')
                    self.previous_line = line
                self.previous_line = line
                #$self.parse_additional_offenses(self.current_offense, data)

        self.complete_frame = pd.DataFrame(data)
        self.complete_frame.to_csv('df_output.csv')

    def is_complete(self, line):
        complete_pattern = re.compile(r'\d{12}.*\d{1,2}:\d{2} [ap]m.*Closed By.*\d{1,2}/\d{1,2}/\d{4}')
        return bool(complete_pattern.search(line))

    def parse_line(self, line, data):
        """
        Parses a single line of text to extract and structure the crash data.
        Expected format:
        [Case Number] [Offense] [Date Reported] [Time Reported] [Date Occurred]
        [Time Occurred] [Location] [Disposition] [Disposition Date] [Location Address]
        """

        parts = re.split(r'\s+', line)
        if len(parts) < 10:
            print(f"this is where we're missing things {parts}")  # Not enough data to parse
            return

        # Regex patterns to identify parts of the data
        date_pattern = re.compile(r'\d{1,2}/\d{1,2}/\d{4}')
        time_pattern = re.compile(r'(\d{1,2}:\d{2} (?:AM|PM)?)')

        # Using finditer to capture both the matches and their positions
        dates = [(m.group(), m.start()) for m in date_pattern.finditer(line)]
        print(f'len of dates {len(dates)}')

        times = [(m.group(), m.start()) for m in time_pattern.finditer(line)]

        # Extracting and assigning values based on positions
        case_number = parts[0]
        offense = line.split(case_number)[-1].split(dates[0][0])[0].strip() if dates else "Unknown"

        # Handling dates and times
        date_reported = dates[0][0] if dates else "0"
        date_occurred = dates[1][0] if len(dates) > 1 else "0"
        disposition_date = dates[-1][0]

        time_reported = times[0][0] if times else "0"
        time_occurred = times[1][0] if len(times) > 1 else "0:00 PM"

        # Extracting disposition and location based on positions
        if len(times) > 1:
            disposition_start = times[-1][1] + len(times[-1][0])
            disposition_end = dates[-1][1]
            disposition = line[disposition_start:disposition_end].strip()
        else:
            disposition = "Unknown"

        location_start = times[1][1] + len(times[1][0]) if len(times) > 1 else times[0][1] + len(times[0][0])
        location_end = disposition_start if 'disposition_start' in locals() else len(line)
        location = line[location_start:location_end].strip()
        if location == "":
            print(f'location is blank')

        # Storing the extracted data
        data['Case Number'].append(case_number)
        data['Offense'].append(offense)
        data['Date Reported'].append(date_reported)
        data['Time Reported'].append(time_reported)
        data['Date Occurred'].append(date_occurred)
        data['Time Occurred'].append(time_occurred)
        data['Location'].append(location)
        data['Disposition'].append(disposition)
        data['Disposition Date'].append(disposition_date)
        data['Location Address'].append("0")  # Assuming no specific location address provided

        # Update last_full_case to reflect the newly parsed line
        self.last_full_case = {
            'Case Number': case_number,
            'Date Reported': date_reported,
            'Time Reported': time_reported,
            'Date Occurred': date_occurred,
            'Time Occurred': time_occurred,
            'Location': location,
            'Disposition': disposition,
            'Disposition Date': disposition_date,
        }

    def set_next_line(self, next_line):
        self.next_line = next_line

    def parse_additional_offenses(self, line, data):
        """Parses lines that contain additional offenses for an existing case."""
        matches = re.findall(
            r"'([^']+)',\s*'(Open|Closed by|Suspended|Unfounded|Referred to)'\s+(\d{1,2}/\d{1,2}/\d{4})", line)
        for offense, disposition, date in matches:
            data['Case Number'].append(self.last_full_case['Case Number'])
            data['Offense'].append(offense)
            data['Date Reported'].append(self.last_full_case['Date Reported'])
            data['Time Reported'].append(self.last_full_case['Time Reported'])
            data['Date Occurred'].append(self.last_full_case['Date Occurred'])
            data['Time Occurred'].append(self.last_full_case['Time Occurred'])
            data['Location'].append(self.last_full_case['Location'])
            data['Disposition'].append(disposition)
            data['Disposition Date'].append(date)
            data['Location Address'].append('0')  # Assuming no address is provided for additional offenses

    def add_data_entry(self, data):
        data['Case Number'].append(self.last_full_case.get('Case Number', 'Unknown'))
        data['Offense'].append(self.relevant_pattern)
        data['Date Reported'].append(self.last_full_case.get('Date Reported', 'Unknown'))
        data['Time Reported'].append(self.last_full_case.get('Time Reported', 'Unknown'))
        data['Date Occurred'].append(self.last_full_case.get('Date Occurred', 'Unknown'))
        data['Time Occurred'].append(self.last_full_case.get('Time Occurred', 'Unknown'))
        data['Location'].append(self.last_full_case.get('Location', 'Unknown'))
        data['Disposition'].append(self.last_full_case.get('Disposition', 'Unknown'))
        data['Disposition Date'].append(self.disposition_date)
        data['Location Address'].append('Unknown')

    def get_frame(self):
        """Returns the complete DataFrame processed."""
        return self.complete_frame

    # Initialize the DataFrame

#    enum_index = enumerate(index)
#    for item, ele in enumerate(index):
#        next_ele = next(enumerate(index))
#        print(f"this is ele {ele}")
#
#        print(f"this is split ele {split_list[ele: next(enum_index)]}")
#


#print(item.index(item[0]))
