import mysql.connector

conn = mysql.connector.connect(
    host = "localhost",
    user = "cf-python",
    passwd = "password"
)

cursor = conn.cursor()