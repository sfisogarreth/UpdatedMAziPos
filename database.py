import pymysql
from tkinter import messagebox

def connect_database():
    global mycursor, conn
    try:
        conn = pymysql.connect(host='localhost', user='root', password='Maybe14031997&')
        print("Database connection established")
        mycursor = conn.cursor()
    except pymysql.MySQLError as e:
        messagebox.showerror('Error', f'Something went wrong: {e}')
        return
    try:
        mycursor.execute('CREATE DATABASE IF NOT EXISTS employee_data')
        mycursor.execute('USE employee_data')
        mycursor.execute('''
            CREATE TABLE IF NOT EXISTS data(
                ID VARCHAR(20),
                Name VARCHAR(20),
                Surname VARCHAR(50),
                PhoneNumber VARCHAR(15),
                Position VARCHAR(30),
                Gender VARCHAR(10),
                Salary DECIMAL(10,3)
            )
        ''')
    except pymysql.MySQLError as e:
        messagebox.showerror('Error', f'SQL Error: {e}')
    finally:
        conn.close()

def insert(ID, Name, Surname, Phone, Position, Gender, Salary):
    try:
        conn = pymysql.connect(host='localhost', user='root', password='Maybe14031997&', database='employee_data')
        mycursor = conn.cursor()
        mycursor.execute('INSERT INTO data VALUES(%s,%s,%s,%s,%s,%s,%s)', (ID, Name, Surname, Phone, Position, Gender, Salary))
        conn.commit()
        print("Data inserted successfully")
    except pymysql.MySQLError as e:
        print(f"Error executing query: {e}")
    finally:
        conn.close()

def id_exist(id):
    try:
        conn = pymysql.connect(host='localhost', user='root', password='Maybe14031997&', database='employee_data')
        mycursor = conn.cursor()
        mycursor.execute('SELECT COUNT(*) FROM data WHERE ID=%s', (id,))
        result = mycursor.fetchone()
        print(result)
        return result[0] > 0
    except pymysql.MySQLError as e:
        print(f"Error executing query: {e}")
        return False
    finally:
        conn.close()

def fetch_employees():
    try:
        conn = pymysql.connect(host='localhost', user='root', password='Maybe14031997&', database='employee_data')
        mycursor = conn.cursor()
        mycursor.execute('SELECT * FROM data')
        result = mycursor.fetchall()
        return result
    except pymysql.MySQLError as e:
        print(f"Error executing query: {e}")
        return []
    finally:
        conn.close()

connect_database()