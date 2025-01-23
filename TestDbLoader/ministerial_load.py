import mysql.connector
from mysql.connector.errors import InterfaceError
import loader as ld
import pandas 
import re
from datetime import datetime
import requests
import json 

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
        time = time.strip()
        if time[-2:] not in ["AM", "PM"]:
            time = time[:-2] + " " + time[-2:]
        try:
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

import requests

def search_ministers(params):
    url = "http://127.0.0.1:5000/candidates/search"
    response = requests.get(url, params=params)
    try:
        data = response.json()  
        if isinstance(data, list) and len(data) > 1:
            return None  
        elif isinstance(data, list) and len(data) == 1:
            return data[0]  
        else:
            return None  
    except ValueError:
        return response.text
    
def parse_and_search(attendees):
    parsed_data = []

    names = [name.strip() for name in attendees.split(",")]

    for name in names:
        if "Minister" in name:
            name_parts = [part for part in name.split() if part != "Minister"]
            last_name = name_parts[-1]  
            params = {"last_name": last_name}
            minister_data = search_ministers(params)
            if minister_data:
                parsed_data.append(minister_data)
        
        elif name and not ("Event Attendees" in name or "Multiple Ministers" in name or "Representatives" in name):
            name_parts = name.split()
            first_name = name_parts[0]
            last_name = name_parts[-1] if name_parts[-1] not in ["MP", "MPs"] else name_parts[-2]  
            params = {"first_name": first_name, "last_name": last_name}
            person_data = search_ministers(params)
            if person_data:
                parsed_data.append(person_data)

    if not parsed_data:
        return json.dumps([])

    return json.dumps(parsed_data)

attendees_data_test = [
    "Minister R, Minister Smith",
    "Todd Stephenson MP, Andy Thompson",
    "Event Attendees",
    "Simon Kebbell & Dan Kneebone",
    "NZ Avocado Representatives",
    "Minister Costello"
]

for attendee in attendees_data_test:
    print(parse_and_search(attendee))

def get_minister_id(minister_name_first, minister_name_last):
    ld.use_db(mycursor, "Entities")
    person_check = ld.check_tb(mycursor, (f"People WHERE first_name = \"{minister_name_first}\" AND last_name = \"{minister_name_last}\""))
    if not person_check:
        ld.import_data(connection, mycursor, "People", ("first_name", "last_name"), (minister_name_first.upper(), minister_name_last.upper()))
    return ((ld.check_tb(mycursor, (f"People WHERE first_name = \"{minister_name_first}\" AND last_name = \"{minister_name_last}\"")))[0])
    
