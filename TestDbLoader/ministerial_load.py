import mysql.connector
from mysql.connector.errors import InterfaceError
import loader as ld
import pandas 


connection = mysql.connector.connect(
    host="localhost",
    user = "root",
    passwd = "root"
)
mycursor = connection.cursor()
# ld.use_db(mycursor, "Ministerial_")

def get_minister_id(minister_name_first, minister_name_last):
    ld.use_db(mycursor, "Entities")
    person_check = ld.check_tb(mycursor, (f"People WHERE first_name = \"{minister_name_first}\" AND last_name = \"{minister_name_last}\""))
    if not person_check:
        ld.import_data(connection, mycursor, "People", ("first_name", "last_name"), (minister_name_first.upper(), minister_name_last.upper()))
    return ((ld.check_tb(mycursor, (f"People WHERE first_name = \"{minister_name_first}\" AND last_name = \"{minister_name_last}\"")))[0])
    
