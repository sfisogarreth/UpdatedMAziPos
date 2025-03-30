import sqlite3
import csv
from tkinter import messagebox

DATABASE_NAME = "Mazi_Store.db"  # Centralized database file

# Helper function to connect to the database
def get_connection():
    try:
        return sqlite3.connect("Mazi_Store.db")
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
                            surname TEXT,
                            phone TEXT,
                            position TEXT,
                            gender TEXT,
                            salary REAL
                        )''')
        # Create inventory table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS inventory (
                item_name TEXT PRIMARY KEY,
                stock_quantity INTEGER
            )
        ''')

        conn.commit()
        print("Database connection established and tables created.")
        conn.close()

    except sqlite3.Error as e:
        messagebox.showerror('Error', f"SQLite error: {e}")

# Insert a new sale into the sales table
def insert_sale(item_name, quantity, price, total_price, date):
    try:
        conn = get_connection()
        if not conn:
            return

        cursor = conn.cursor()

        cursor.execute('''INSERT INTO sales (item_name, quantity, price, total_price, date)
                          VALUES (?, ?, ?, ?, ?)''', (item_name, quantity, price, total_price, date))
        conn.commit()
        print("Sale recorded successfully.")
        conn.close()

    except sqlite3.Error as e:
        print(f"SQLite error during sale insertion: {e}")

# Insert a new employee into the employees table
def insert_employee(id, name, surname, phone, position, gender, salary):
    try:
        conn = get_connection()
        if not conn:
            return

        cursor = conn.cursor()

        cursor.execute('''INSERT INTO employees (id, name, surname, phone, position, gender, salary)
                          VALUES (?, ?, ?, ?, ?, ?, ?)''', (id, name, surname, phone, position, gender, salary))
        conn.commit()
        print(f"Employee {name} added successfully.")
        conn.close()

    except sqlite3.Error as e:
        print(f"SQLite error while inserting employee: {e}")

# Fetch all employees from the employees table
def fetch_employees():
    """Fetch all employees from the employees table."""
    try:
        conn = get_connection()
        if not conn:
            return []

        cursor = conn.cursor()

        cursor.execute("SELECT id, name, surname, phone, position, gender, salary FROM employees")
        employees = cursor.fetchall()
        conn.close()

        return [dict(id=row[0], name=row[1], surname=row[2], phone=row[3],
                     position=row[4], gender=row[5], salary=row[6]) for row in employees]

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

# Function to read all data from the sales database for debugging
def check_sales_data():
    conn = get_connection()
    if not conn:
        return

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM sales")
    rows = cursor.fetchall()
    conn.close()

    for row in rows:
        print(row)

# Function to insert data into the inventory table.

def id_exist(table_name, column_name, id_value):
    """Check if a specific ID exists in a table."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        query = f"SELECT 1 FROM {table_name} WHERE {column_name} = ? LIMIT 1"
        cursor.execute(query, (id_value,))
        result = cursor.fetchone()
        return result is not None  # Return True if the ID exists, otherwise False
    finally:
        conn.close()

# Function to get inventory of specific item
def insert_inventory(item_name, stock_quantity):
    conn = get_connection()
    if not conn:
        return

    cursor = conn.cursor()

    try:
        cursor.execute('''
            INSERT OR REPLACE INTO inventory (item_name, stock_quantity)
            VALUES (?, ?)
        ''', (item_name, stock_quantity))
        conn.commit()
        print(f"Inventory for {item_name} updated to {stock_quantity}.")
    except sqlite3.Error as e:
        print(f"SQLite error while inserting inventory: {e}")
    finally:
        conn.close()

def get_inventory(item_name):
    conn = get_connection()
    if not conn:
        return None

    cursor = conn.cursor()

    try:
        cursor.execute('''
            SELECT stock_quantity FROM inventory WHERE item_name = ?
        ''', (item_name,))
        result = cursor.fetchone()
        if result:
            return result[0]
        else:
            return 0
    except sqlite3.Error as e:
        print(f"SQLite error during get_inventory: {e}")
        return None
    finally:
        conn.close()

def fetch_all_inventory():
    conn = get_connection()
    if not conn:
        return []

    cursor = conn.cursor()

    try:
        cursor.execute("SELECT item_name, stock_quantity FROM inventory")
        rows = cursor.fetchall()
        return [{"item_name": row[0], "stock_quantity": row[1]} for row in rows]
    except sqlite3.Error as e:
        print(f"SQLite error during fetch_all_inventory: {e}")
        return []
    finally:
        conn.close()


# Example Usage
if __name__ == "__main__":
    connect_database()  # Setup database and tables

    # Insert sample employees (optional)
    insert_employee(1, "John Doe", "Doe", "1234567890", "Manager", "Male", 75000)
    insert_employee(2, "Jane Smith", "Smith", "9876543210", "Developer", "Female", 65000)

    # Insert a sample sale
    insert_sale("Item A", 10, 5.5, 55.0, "2024-07-09 12:00:00")

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