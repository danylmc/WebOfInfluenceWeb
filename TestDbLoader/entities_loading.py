import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import loader as ld
import pandas 
import os

# Load environment variables
load_dotenv()
print("Loaded DB_NAME:", os.getenv("DB_NAME"))

# Establish DB connection
try:
    connection = mysql.connector.connect(
        host=os.environ.get("DB_HOST", "localhost"),
        user=os.environ.get("DB_USER", "root"),
        passwd=os.environ.get("DB_PASSWORD", "engr4892025"),
        database=os.environ.get("DB_NAME")
    )
    mycursor = connection.cursor()
except Error as e:
    print(f"Database connection error: {e}")
    raise

# Use Entities DB - Remove below if havent created
ld.use_db(mycursor, "Entities")

# === Table Creation ===
def create_people_table():
    ld.create_tb(mycursor, "People", {
        "id": "INT AUTO_INCREMENT PRIMARY KEY", 
        "first_name": "VARCHAR(255)", 
        "last_name": "VARCHAR(255)"
    })
    
def create_party_table():
    ld.create_tb(mycursor, "Parties", {
        "id": "INT AUTO_INCREMENT PRIMARY KEY", 
        "party_name": "VARCHAR(255)"
    })

def create_electorate_table():
    ld.create_tb(mycursor, "Electorates", {
        "id": "INT AUTO_INCREMENT PRIMARY KEY", 
        "electorate_name": "VARCHAR(255)"
    })

def create_donor_table():
    ld.create_tb(mycursor, "Donors", {
        "id": "INT AUTO_INCREMENT PRIMARY KEY", 
        "first_name": "VARCHAR(255)", 
        "last_name": "VARCHAR(255)"
    })

# === People Loading ===
def load_csv_people_23_17_14_11(cursor, file):
    file = pandas.read_csv(file)
    for index, row in file.iterrows():
        if pandas.isna(row['CandidateName_First']) or pandas.isna(row['CandidateName_Last']):
            print(f"Skipping row {index} due to missing PARTY value.")
            continue 
        person_check = ld.check_tb(cursor, (f"People WHERE first_name = \"{(row['CandidateName_First']).upper()}\" AND last_name = \"{(row['CandidateName_Last']).upper()}\""))
        if not person_check:
            ld.import_data(connection, cursor, "People", ("first_name", "last_name"), (row['CandidateName_First'].upper(), row['CandidateName_Last'].upper()))

def load_csv_people_20(cursor, file):
    file = pandas.read_csv(file)
    for index, row in file.iterrows():
        if pandas.isna(row['FIRST NAME(S)']) or pandas.isna(row['SURNAME']):
            print(f"Skipping row {index} due to missing PARTY value.")
            continue 
        person_check = ld.check_tb(cursor, (f"People WHERE first_name = \"{(row['FIRST NAME(S)'].upper())}\" AND last_name = \"{(row['SURNAME'].upper())}\""))
        if not person_check:
            ld.import_data(connection, cursor, "People", ("first_name", "last_name"), (row['FIRST NAME(S)'].upper(), row['SURNAME'].upper()))

def populate_people_table():
    load_csv_people_23_17_14_11(mycursor, "candidate_csv/2011_candidate_donations.csv")
    load_csv_people_23_17_14_11(mycursor, "candidate_csv/2014_candidate_donations.csv")
    load_csv_people_23_17_14_11(mycursor, "candidate_csv/2017_candidate_donations.csv")
    load_csv_people_20(mycursor, "candidate_csv/2020_candidate_donations.csv")
    load_csv_people_23_17_14_11(mycursor, "candidate_csv/2023_candidate_donations.csv")
    connection.commit()

# === Party Loading ===
def load_csv_party_23_17_14_11(cursor, file):
    file = pandas.read_csv(file)
    for index, row in file.iterrows():
        if pandas.isna(row['Party']):
            print(f"Skipping row {index} due to missing PARTY value.")
            continue 
        party_check = ld.check_tb(cursor, (f"Parties WHERE party_name = \"{(row['Party']).upper()}\""))
        if not party_check:
            ld.import_data(connection, cursor, "Parties", ("party_name", ), ((row['Party']).upper(), ))

def load_csv_party_20(cursor, file):
    file = pandas.read_csv(file)
    for index, row in file.iterrows():
        if pandas.isna(row['PARTY']):
            print(f"Skipping row {index} due to missing PARTY value.")
            continue 
        print(row['PARTY'])
        party_check = ld.check_tb(cursor, (f"Parties WHERE party_name = \"{(row['PARTY']).upper()}\""))
        if not party_check:
            ld.import_data(connection, cursor, "Parties", ("party_name",), ((row['PARTY']).upper(),))

def populate_party_table():
    load_csv_party_23_17_14_11(mycursor, "candidate_csv/2011_candidate_donations.csv")
    load_csv_party_23_17_14_11(mycursor, "candidate_csv/2014_candidate_donations.csv")
    load_csv_party_23_17_14_11(mycursor, "candidate_csv/2017_candidate_donations.csv")
    load_csv_party_20(mycursor, "candidate_csv/2020_candidate_donations.csv")
    load_csv_party_23_17_14_11(mycursor, "candidate_csv/2023_candidate_donations.csv")
    connection.commit()


def clean_parties():
    to_remove = [
        'GREENS', 'MANA MOVEMENT', 'LABOUR',
        'THE OPPORTUNITIES PARTY (TOP)',
        'NZ FIRST', 'MAORI PARTY', 'ACT NEW ZEALAND'
    ]
    for party in to_remove:
        mycursor.execute("DELETE FROM Parties WHERE party_name = %s", (party,))
    connection.commit()

# === Electorate Loading ===
def load_csv_electorate_23_17_14_11(cursor, file):
    file = pandas.read_csv(file)
    for index, row in file.iterrows():
        if pandas.isna(row['Electorate']):
            print(f"Skipping row {index} due to missing PARTY value.")
            continue 
        electorate_check = ld.check_tb(cursor, (f"Electorates WHERE electorate_name = \"{(row['Electorate']).upper()}\""))
        if not electorate_check:
            ld.import_data(connection, cursor, "Electorates", ("electorate_name", ), ((row['Electorate']).upper(), ))

def load_csv_electorate_20(cursor, file):
    file = pandas.read_csv(file)
    for index, row in file.iterrows():
        if pandas.isna(row['ELECTORATE']):
            print(f"Skipping row {index} due to missing PARTY value.")
            continue 
        electorate_check = ld.check_tb(cursor, (f"Electorates WHERE electorate_name = \"{(row['ELECTORATE']).upper()}\""))
        if not electorate_check:
            ld.import_data(connection, cursor, "Electorates", ("electorate_name", ), ((row['ELECTORATE']).upper(), ))

def populate_electorate_table():
    load_csv_electorate_23_17_14_11(mycursor, "candidate_csv/2011_candidate_donations.csv")
    load_csv_electorate_23_17_14_11(mycursor, "candidate_csv/2014_candidate_donations.csv")
    load_csv_electorate_23_17_14_11(mycursor, "candidate_csv/2017_candidate_donations.csv")
    load_csv_electorate_20(mycursor, "candidate_csv/2020_candidate_donations.csv")
    load_csv_electorate_23_17_14_11(mycursor, "candidate_csv/2023_candidate_donations.csv")
    connection.commit()

# === Full Loader ===
def create_db():
    ld.create_db(mycursor, "Entities")
    connection.commit()
    
def full_load_entities():
    # Ensure the database exists
    create_db()

    # Switch to using that DB
    ld.use_db(mycursor, "Entities")

    # Step 3: Create and populate tables
    create_people_table()
    populate_people_table()

    create_party_table()
    populate_party_table()

    clean_parties()

    create_electorate_table()
    populate_electorate_table()

    create_donor_table()

    connection.commit()
