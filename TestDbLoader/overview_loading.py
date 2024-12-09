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
ld.use_db(mycursor, "Overviews_Candidate_Donations_By_Year")

def clean_dollar_value(dollar_str):
    """
        Gets rid of extra dollar sign so values can be evaluated numerically
    """
    try:
        return float(dollar_str.replace("$", "").replace(",", "").strip())
    except ValueError:
        print(f"Invalid dollar value: {dollar_str}")


def create_election_year_candidates_table():
    column_dict = {
        "id": "INT AUTO_INCREMENT PRIMARY KEY",
        "total_donations": "FLOAT",
        "total_expenses": "FLOAT",
        "part_a": "FLOAT",
        "part_b": "FLOAT",
        "part_c": "FLOAT",
        "part_d": "FLOAT",
        "part_f": "FLOAT",
        "part_g": "FLOAT",
        "part_h": "FLOAT"
    }
    
    foreign_keys = [
        ("people_id", "Entities", "People", "id"),
        ("party_id", "Entities", "Parties", "id"),
        ("electorate_id", "Entities", "Electorates", "id")
    ]
    
    ld.create_tb(mycursor, "2023_Candidate_Donation_Overview", column_dict, foreign_keys)

create_election_year_candidates_table()
ld.check_tb_categories(mycursor, "2023_Candidate_Donation_Overview")