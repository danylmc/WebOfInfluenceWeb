import mysql.connector
from mysql.connector.errors import InterfaceError
import pandas as pd

       
# Connect to the database and csv file
connection = mysql.connector.connect(
    host="localhost",
    user = "root",
    passwd = "root"
)
mycursor = connection.cursor()  
file = pd.read_csv("candidate_csv/2023_candidate_donations.csv")

# Puts data in db
def import_data(cursor, donation_id, first_name, last_name, electorate, party, total_expense, acd_total, part_a, part_b, part_c, part_d, part_f, part_g, part_h):
    cursor.execute("INSERT INTO 2023Candidates (CandidateDonations2023Test_Id, CandidateName_First, CandidateName_Last, Electorate, Party, TotalExpenses, TotalTotalDonationsACD, TotalPartA, TotalPartB, TotalPartC, TotalPartD, TotalPartF, TotalPartG, TotalPartH) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (int(donation_id), first_name, last_name, electorate, party, total_expense,  acd_total, part_a, part_b, part_c, part_d, part_f, part_g, part_h))

#init db
def init_db(cursor):
    try:
        cursor.execute("SHOW DATABASES") 
        results = cursor.fetchall()
        if any('CandidateDonations2023Test' == db[0] for db in results):
            cursor.execute("USE CandidateDonations2023Test")
        else:
            cursor.execute("CREATE DATABASE CandidateDonations2023Test")
        cursor.execute("SHOW TABLES") 
        result_tables = cursor.fetchall()
        if any('2023Candidates' == table[0] for table in result_tables):
            print("stop")
            return
        else: 
            cursor.execute("""
                            CREATE TABLE 2023Candidates(
                                CandidateDonations2023Test_Id INT,
                                CandidateName_First VARCHAR(255),
                                CandidateName_Last VARCHAR(255),
                                Electorate VARCHAR(255),
                                Party VARCHAR(255),
                                TotalExpenses VARCHAR(255),
                                TotalTotalDonationsACD VARCHAR(255),
                                TotalPartA VARCHAR(255),
                                TotalPartB VARCHAR(255),
                                TotalPartC VARCHAR(255),
                                TotalPartD VARCHAR(255),
                                TotalPartF VARCHAR(255),
                                TotalPartG VARCHAR(255),
                                TotalPartH VARCHAR(255)
                                )
                            """)
    except mysql.connector.errors.InterfaceError as e:
        print(f"Error occurred: {e}")

def do_fill(): 
    for index, row in file.iterrows():
        import_data(mycursor, 
                    row['CandidateDonations2023Test_Id'], 
                    row['CandidateName_First'], 
                    row['CandidateName_Last'], 
                    row['Electorate'], 
                    row['Party'], 
                    row['TotalExpensesFG'], 
                    row['TotalDonationsACD'], 
                    row['TotalPartA'], 
                    row['TotalPartB'], 
                    row['TotalPartC'], 
                    row['TotalPartD'], 
                    row['TotalPartFCandidateOnlyExpenses'], 
                    row['TotalPartGSharedExpenses'], 
                    row['TotalPartH'])
    connection.commit()

def check_db_categories():
    mycursor.execute("DESCRIBE 2023Candidates")
    print(mycursor.fetchall())

def check_db():
    mycursor.execute("SELECT * FROM 2023Candidates")
    table_output = mycursor.fetchall()
    df = pd.DataFrame(table_output, columns=["CandidateDonations2023Test_Id",
                                              "CandidateName_First", 
                                              "CandidateName_Last", 
                                              "Electorate", 
                                              "Party", 
                                              "TotalExpenses", 
                                              "TotalTotalDonationsACD", 
                                              "TotalPartA", 
                                              "TotalPartB", 
                                              "TotalPartC", 
                                              "TotalPartD", 
                                              "TotalPartF", 
                                              "TotalPartG", 
                                              "TotalPartH"])
    
    # Display the DataFrame
    print(df)

def clear_table():
    mycursor.execute("TRUNCATE TABLE 2023Candidates")
    connection.commit()  

def delete_table(name):
    mycursor.execute(f"DROP TABLE IF EXISTS {name}")
    connection.commit()
    print(f"Table {name} deleted")
    
init_db(mycursor)
do_fill()
#delete_table("2023Candidates")
check_db()
#check_db_categories()