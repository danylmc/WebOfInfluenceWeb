import mysql.connector
from mysql.connector.errors import InterfaceError
import pandas as pd
from tabulate import tabulate


DEBUG = True  # Set False in production

def create_db(cursor, name):
    try:
        cursor.execute("SHOW DATABASES") 
        results = cursor.fetchall()
        if any(name == db[0] for db in results):
            return
        else:
            cursor.execute("CREATE DATABASE " + name)
            print(f"Database {name} created")
    except mysql.connector.errors.InterfaceError as e:
        print(f"Error occurred: {e}")

def use_db(cursor, name):
    try:
        cursor.execute("USE " + name)
        print(f"Using database {name}")
    except mysql.connector.errors.InterfaceError as e:
        print(f"Error occurred: {e}")

def create_tb(cursor, table_name, column_dict, foreign_keys=None):
    try:
        column_definitions = ", ".join(f"{col_name} {data_type}" for col_name, data_type in column_dict.items())

        foreign_key_definitions = ""
        if foreign_keys:
            fk_statements = [
                f"FOREIGN KEY ({col}) REFERENCES {ref_db}.{ref_table}({ref_col}) ON DELETE CASCADE"
                for col, ref_db, ref_table, ref_col in foreign_keys
            ]
            foreign_key_definitions = ", " + ", ".join(fk_statements)

        # Construct the CREATE TABLE query
        create_query = f"CREATE TABLE IF NOT EXISTS {table_name} ({column_definitions}{foreign_key_definitions})"
        if DEBUG:
            print(f"Executing SQL for table creation:\n{create_query}")  # ✅ Print the full query

        # Execute the create table query
        cursor.execute(create_query)
        if DEBUG:
            print(f"✅ Table {table_name} created successfully.")
    except mysql.connector.Error as e:
        print(f"❌ Error creating table {table_name}: {e}")

def import_data(connection, cursor, table_name, categories, data):
    columns = ", ".join(categories) 
    placeholders = ", ".join(["%s"] * len(data)) 
    query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
    try:
        # Execute the insert query
        cursor.execute(query, data)
        if DEBUG:
            print(f"Data {data} inserted into {table_name} ({columns})")
    except mysql.connector.Error as e: 
        print(f"❌ Error occurred: {e}")
    connection.commit()

def check_tb(cursor, name):
    cursor.execute(f"SELECT * FROM {name}")
    return cursor.fetchall()

def check_tb_categories(cursor, name):
    cursor.execute(f"DESCRIBE {name}")
    print(cursor.fetchall())

def delete_db(cursor, name):
    cursor.execute(f"DROP DATABASE IF EXISTS {name}")

def delete_tb(cursor, table_name):
    cursor.execute(f"DROP TABLE IF EXISTS {table_name}")

def clear_tb(cursor, table_name):
    cursor.execute(f"TRUNCATE TABLE {table_name}")

def show_dbs(cursor):
    cursor.execute("SHOW DATABASES")
    print(cursor.fetchall())

def check_tb_print(cursor, name):
    cursor.execute(f"SELECT * FROM {name}")
    rows = cursor.fetchall()
    if not rows:
        print(f"No data found in the table: {name}")
        return
    
    column_names = [desc[0] for desc in cursor.description]

    print(tabulate(rows, headers=column_names, tablefmt="grid"))
from tabulate import tabulate

def check_tb_print_range(cursor, name, start, end):
    cursor.execute(f"SELECT * FROM {name}")
    rows = cursor.fetchall()
    if not rows:
        print(f"No data found in the table: {name}")
        return
    if start < 0 or start >= len(rows) or end <= start or end > len(rows):
        print(f"Invalid range. The table has {len(rows)} rows.")
        return
    column_names = [desc[0] for desc in cursor.description]
    rows_to_print = rows[start:end]
    print(tabulate(rows_to_print, headers=column_names, tablefmt="grid"))

def get_id_match(cursor, database_name, table_name, condition_dict):
    if not condition_dict:
        if DEBUG:
            print("❌ No conditions provided for get_id_match.")
        return None
    
    conditions = []
    values = []
    
    for col_name, value in condition_dict.items():
        conditions.append(f"{col_name} = %s")
        values.append(value)
    
    checks = " AND ".join(conditions)
    if DEBUG:
        print(checks)  
    
    query = f"SELECT * FROM {database_name}.{table_name} WHERE {checks}"
    cursor.execute(query, tuple(values))  
    
    # Fetch the first matching row
    vals = cursor.fetchall()
    if not vals:
        if DEBUG:
            print("No match found.")
        return None
    return vals[0][0]

# This function maps party names to their official names
def map_party_names(name):
    if name == "GREENS":
        return "Green Party"
    elif name == "MANA MOVEMENT":
        return "MANA"
    elif name == 'LABOUR':
        return "LABOUR PARTY"
    elif name == 'THE OPPORTUNITIES PARTY (TOP)':
        return 'THE OPPORTUNITIES PARTY'
    elif name == 'NZ FIRST':
        return 'NEW ZEALAND FIRST PARTY'
    elif name == 'MAORI PARTY':
        return 'TE PATI MAORI'
    elif name == 'ACT NEW ZEALAND':
        return 'ACT'
    else :
        return name