import mysql.connector
from mysql.connector.errors import InterfaceError
import pandas as pd

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

def create_tb(cursor, table_name, column_dict):
    try:
        column_definitions = ", ".join(f"{col_name} {data_type}" for col_name, data_type in column_dict.items())
        cursor.execute(f"""
                        CREATE TABLE {table_name}(
                            {column_definitions}
                            )
                        """)
    except mysql.connector.errors.InterfaceError as e:
        print(f"Error occurred: {e}")

def import_data(connection, cursor, table_name, categories, data):
    columns = ", ".join(categories) 
    placeholders = ", ".join(["%s"] * len(data)) 
    query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
    try:
        # Execute the parameterized query
        cursor.execute(query, data)
        print(f"Data {data} inserted into {table_name} ({columns})")
    except mysql.connector.Error as e:  # Catch a broader set of MySQL errors
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