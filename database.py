import mysql.connector

database = mysql.connector.connect(
    host='flaskmysql.cvmkmiemmv1r.us-east-1.rds.amazonaws.com',
    user='admin',
    password='carlitos1234',
    database='cyg'
)