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
#ld.create_db(mycursor, "Overviews")
ld.show_dbs(mycursor)