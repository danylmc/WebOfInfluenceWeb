import mysql.connector
from mysql.connector.errors import InterfaceError
import loader as ld
import pandas 
import re
from datetime import datetime

connection = mysql.connector.connect(
    host="localhost",
    user = "root",
    passwd = "root"
)
mycursor = connection.cursor()
# ld.use_db(mycursor, "Ministerial_")

# Time normaliser 
def get_time_tuple(time_string):
    pattern = r"(\d{1,2}:\d{2}\s?[APM]{2})"
    time_matches = re.findall(pattern, time_string)
    
    if not time_matches or len(time_matches) != 2:
        raise ValueError("Time string not in correct format or does not contain exactly two times.")
    
    time_1200_format = []
    
    for time in time_matches:
        # Ensure a space exists between the time and AM/PM
        time = time.strip()
        if time[-2:] not in ["AM", "PM"]:
            time = time[:-2] + " " + time[-2:]
        
        try:
            # Convert to 24-hour format and format as HHMM
            time_obj = datetime.strptime(time, "%I:%M %p")
            time_1200_format.append(time_obj.strftime("%H%M"))
        except ValueError:
            raise ValueError(f"Invalid time format: {time}")
    
    return tuple(time_1200_format)

# Location normaliser (Updated at Andrew Hoggard)
def get_location(location_string):
    wellington_based = [
        'Parliament Buildings', 
        'Te Papa', 
        'Government House', 
        'Welington', 
        'Wellingtgon', 
        'Wellington', 
        'Microsoft Teams Meeting',
        'Teams Meeting', 
        'Online', 
        'Video Conference', 
        'L1 Library meeting room; Room 013'
    ]
    if location_string in wellington_based:
        return 'Wellington'
    return wellington_based

def get_minister_id(minister_name_first, minister_name_last):
    ld.use_db(mycursor, "Entities")
    person_check = ld.check_tb(mycursor, (f"People WHERE first_name = \"{minister_name_first}\" AND last_name = \"{minister_name_last}\""))
    if not person_check:
        ld.import_data(connection, mycursor, "People", ("first_name", "last_name"), (minister_name_first.upper(), minister_name_last.upper()))
    return ((ld.check_tb(mycursor, (f"People WHERE first_name = \"{minister_name_first}\" AND last_name = \"{minister_name_last}\"")))[0])
    
