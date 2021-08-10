from flask import Flask, redirect, url_for, render_template, request
import mysql.connector
from mysql.connector import Error
#from sqlalchemy import create_engine

#engine = create_engine("mysql+mysqldb://root:joepettit@localhost:3306/foo")


def create_connection(host_name, user_name, user_password):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password
        )
        print("Connection to MySQL DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")

    return connection

def get_columns(database, table, mycursor):
    #mycursor.execute("USE " + database + ";")
    #mycursor.execute("SHOW COLUMNS FROM "+ table + ";")
    column_array = ['Course', 'Tees', 'Score', 'Date']
    #for (x) in mycursor:
        #column_array.append(x[0])
    return column_array

def get_rows(database, table, mycursor, session):
    print(session['id'])
    mycursor.execute("USE " + database + ";")
    mycursor.execute("SELECT course, tees_played, score, date_played FROM "+ table + " WHERE user_id=%s;", (session['id'],))
    rows_array = []
    for (x) in mycursor:
        print(x)
        rows_array.append(x)
    return rows_array