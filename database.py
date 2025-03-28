import sqlite3
import csv
from tkinter import messagebox

DATABASE_NAME = "Mazi_Store.db"  # Centralized database file

# Helper function to connect to the database
def get_connection():
    try:
        return sqlite3.connect(DATABASE_NAME)
    except sqlite3.Error as e:
        messagebox.showerror('Error', f"SQLite connection error: {e}")
        return None

# Function to initialize the database and create tables
def connect_database():
    try:
        conn = get_connection()
        if not conn:
            return

        cursor = conn.cursor()

        # Create `sales` table
        cursor.execute('''CREATE TABLE IF NOT EXISTS sales (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            item_name TEXT,
                            quantity INTEGER,
                            price REAL,
                            total_price REAL,
                            date TEXT
                        )''')

        # Create `employees` table
        cursor.execute('''CREATE TABLE IF NOT EXISTS employees (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            name TEXT,
                            position TEXT,
                            salary REAL
                        )''')

        conn.commit()
        print("Database connection established and tables created.")
        conn.close()

    except sqlite3.Error as e:
        messagebox.showerror('Error', f"SQLite error: {e}")

# Insert a new sale into the sales table
def insert_sale(item_name, quantity, price, total_price):
    try:
        conn = get_connection()
        if not conn:
            return

        cursor = conn.cursor()

        cursor.execute('''INSERT INTO sales (item_name, quantity, price, total_price, date)
                          VALUES (?, ?, ?, ?, datetime('now'))''', (item_name, quantity, price, total_price))
        conn.commit()
        print("Sale recorded successfully.")
        conn.close()

    except sqlite3.Error as e:
        print(f"SQLite error during sale insertion: {e}")

# Insert a new employee into the employees table
def insert_employee(name, position, salary):
    try:
        conn = get_connection()
        if not conn:
            return

        cursor = conn.cursor()

        cursor.execute('''INSERT INTO employees (name, position, salary)
                          VALUES (?, ?, ?)''', (name, position, salary))
        conn.commit()
        print(f"Employee {name} added successfully.")
        conn.close()

    except sqlite3.Error as e:
        print(f"SQLite error while inserting employee: {e}")

# Fetch all employees from the employees table
def fetch_employees():
    try:
        conn = get_connection()
        if not conn:
            return []

        cursor = conn.cursor()

        cursor.execute("SELECT id, name, position, salary FROM employees")
        employees = cursor.fetchall()  # List of tuples

        conn.close()

        # Convert into list of dictionaries for better readability
        employee_list = [
            {"id": emp[0], "name": emp[1], "position": emp[2], "salary": emp[3]}
            for emp in employees
        ]

        return employee_list

    except sqlite3.Error as e:
        print(f"SQLite error while fetching employees: {e}")
        return []

# Export sales table data to a CSV file
def export_sales_to_csv():
    try:
        conn = get_connection()
        if not conn:
            return

        cursor = conn.cursor()

        cursor.execute("SELECT * FROM sales")
        sales = cursor.fetchall()

        with open('sales_report.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["ID", "Item Name", "Quantity", "Price", "Total Price", "Date"])  # Column headers
            writer.writerows(sales)

        print("Sales exported to sales_report.csv.")
        messagebox.showinfo("Export Successful", "Sales data exported successfully to sales_report.csv")
        conn.close()

    except sqlite3.Error as e:
        messagebox.showerror("Export Error", f"SQLite error: {e}")

# Example Usage
if __name__ == "__main__":
    connect_database()  # Setup database and tables

    # Insert sample employees (optional)
    insert_employee("John Doe", "Manager", 75000)
    insert_employee("Jane Smith", "Developer", 65000)

    # Insert a sample sale
    insert_sale("Item A", 10, 5.5, 55.0)

    # Fetch and display all employees
    employees = fetch_employees()
    if employees:
        print("Employees:")
        for emp in employees:
            print(f"ID: {emp['id']}, Name: {emp['name']}, Position: {emp['position']}, Salary: {emp['salary']}")
    else:
        print("No employees found.")

    # Export sales to CSV
    export_sales_to_csv()
