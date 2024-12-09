import mysql.connector
from mysql.connector.errors import InterfaceError
import pandas as pd
from tabulate import tabulate

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
        
        create_query = f"""
            CREATE TABLE {table_name} (
                {column_definitions}
                {foreign_key_definitions}
            )
        """
        cursor.execute(create_query)
        print(f"Table {table_name} created successfully.")
    except mysql.connector.errors.InterfaceError as e:
        print(f"Error occurred: {e}")
    except mysql.connector.Error as e:
        print(f"Error occurred: {e}")

def import_data(connection, cursor, table_name, categories, data):
    columns = ", ".join(categories) 
    placeholders = ", ".join(["%s"] * len(data)) 
    query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
    try:
        cursor.execute(query, data)
        print(f"Data {data} inserted into {table_name} ({columns})")
    except mysql.connector.Error as e: 
        print(f"Error occurred: {e}")
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