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
ld.use_db(mycursor, "Ministerial_")