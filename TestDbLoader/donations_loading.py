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
ld.use_db(mycursor, "Entities")

def create_people_table():
    ld.create_tb(mycursor, "People", {"id": "INT AUTO_INCREMENT PRIMARY KEY", "first_name": "VARCHAR(255)", "last_name": "VARCHAR(255)"})

def load_csv_people(cursor, file):
    file = pandas.read_csv(file)
    for index, row in file.iterrows():
        person_check = ld.check_tb(cursor, (f"People WHERE first_name = \"{row['CandidateName_First']}\" AND last_name = \"{row['CandidateName_Last']}\""))
        if not person_check:
            ld.import_data(connection, cursor, "People", ("first_name", "last_name"), (row['CandidateName_First'], row['CandidateName_Last']))
load_csv_people(mycursor, "candidate_csv/2023_candidate_donations.csv")
#mycursor.execute("SELECT * FROM People WHERE id = 1")  
#ld.check_tb_categories(mycursor, "People")
