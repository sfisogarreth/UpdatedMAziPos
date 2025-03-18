import pymysql
import csv
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
        mycursor.execute('CREATE DATABASE IF NOT EXISTS liquor_store')
        mycursor.execute('USE liquor_store')
        mycursor.execute('''
            CREATE TABLE IF NOT EXISTS sales (
                id INT AUTO_INCREMENT PRIMARY KEY,
                item_name VARCHAR(100),
                quantity INT,
                price DECIMAL(10,2),
                total_price DECIMAL(10,2),
                date DATETIME
            )
        ''')
    except pymysql.MySQLError as e:
        messagebox.showerror('Error', f'SQL Error: {e}')
    finally:
        conn.close()

def insert_sale(item_name, quantity, price, total_price):
    try:
        conn = pymysql.connect(host='localhost', user='root', password='Maybe14031997&', database='liquor_store')
        mycursor = conn.cursor()
        mycursor.execute('''
            INSERT INTO sales (item_name, quantity, price, total_price, date)
            VALUES (%s, %s, %s, %s, NOW())
        ''', (item_name, quantity, price, total_price))
        conn.commit()
        print("Sale recorded successfully")
    except pymysql.MySQLError as e:
        print(f"Error executing query: {e}")
    finally:
        conn.close()

def export_sales_to_csv():
    """Exports all sales data to a CSV file."""
    try:
        conn = pymysql.connect(host='localhost', user='root', password='Maybe14031997&', database='liquor_store')
        mycursor = conn.cursor()
        mycursor.execute('SELECT * FROM sales')
        sales = mycursor.fetchall()

        with open('sales_report.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["ID", "Item Name", "Quantity", "Price", "Total Price", "Date"])
            writer.writerows(sales)

        print("Sales exported to sales_report.csv")
        messagebox.showinfo("Export Successful", "Sales data exported successfully to sales_report.csv")

    except pymysql.MySQLError as e:
        messagebox.showerror("Export Error", f"Error exporting sales: {e}")
    finally:
        conn.close()

# Ensure database and tables exist
connect_database()