# database.py
import sqlite3
import csv
from tkinter import messagebox
import os  # Import the os module
import datetime # Needed for update_stock check

DATABASE_NAME = "Mazi_Store.db"  # Centralized database file

# Helper function to connect to the database
def get_connection():
    """Connects to the SQLite database."""
    try:
        # The connection itself doesn't need row_factory for these functions
        return sqlite3.connect(DATABASE_NAME)
    except sqlite3.Error as e:
        messagebox.showerror('Error', f"SQLite connection error: {e}")
        return None

# Function to initialize the database and create tables
def connect_database():
    """Initializes the database connection and ensures tables exist."""
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
                stock_quantity INTEGER NOT NULL DEFAULT 0
            )
        ''')

        conn.commit()
        print("Database connection established and tables checked/created.")
        conn.close()

    except sqlite3.Error as e:
        messagebox.showerror('Error', f"SQLite error during table creation: {e}")

# Insert a new sale into the sales table
def insert_sale(item_name, quantity, price, total_price, date):
    """Inserts a single sale record."""
    try:
        conn = get_connection()
        if not conn:
            return

        cursor = conn.cursor()
        cursor.execute('''INSERT INTO sales (item_name, quantity, price, total_price, date)
                        VALUES (?, ?, ?, ?, ?)''', (item_name, quantity, price, total_price, date))
        conn.commit()
        # print(f"Sale recorded successfully: {item_name} x{quantity}") # Optional confirmation
        conn.close()

    except sqlite3.Error as e:
        print(f"SQLite error during sale insertion: {e}")
        # Optionally show error: messagebox.showerror("DB Error", f"Failed to record sale: {e}")


# --- Employee Functions (Keep as they are in your original file) ---
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

def fetch_employees():
    try:
        conn = get_connection()
        if not conn: return []
        conn.row_factory = sqlite3.Row # Use Row factory here for easy dict conversion
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, surname, phone, position, gender, salary FROM employees")
        employees_rows = cursor.fetchall()
        conn.close()
        # Convert Row objects to dictionaries
        return [dict(row) for row in employees_rows]
    except sqlite3.Error as e:
        print(f"SQLite error while fetching employees: {e}")
        return []

def id_exist(table_name, column_name, id_value):
    conn = get_connection()
    if not conn: return False
    cursor = conn.cursor()
    try:
        query = f"SELECT 1 FROM {table_name} WHERE {column_name} = ? LIMIT 1"
        cursor.execute(query, (id_value,))
        result = cursor.fetchone()
        return result is not None
    except sqlite3.Error as e:
        print(f"SQLite error checking ID existence: {e}")
        return False # Assume doesn't exist on error
    finally:
        if conn: conn.close()
# --- End Employee Functions ---


# Export sales table data to a CSV file (uses default filename 'sales_report.csv')
def export_sales_to_csv():
    """Exports the sales table to sales_report.csv."""
    file_path = 'sales_report.csv' # Default filename from your code
    try:
        print("Starting CSV export...")
        conn = get_connection()
        if not conn:
            print("Database connection failed for export.")
            return

        cursor = conn.cursor()
        cursor.execute("SELECT id, item_name, quantity, price, total_price, date FROM sales") # Explicit columns
        sales_data = cursor.fetchall()
        conn.close() # Close connection after fetching

        if not sales_data:
             messagebox.showinfo("Export Info", "No sales data found to export.")
             print("No sales data to export.")
             return

        print(f"Sales data fetched ({len(sales_data)} rows). Writing to {file_path}...")
        with open(file_path, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            # Write header matching the SELECT query
            writer.writerow(["ID", "Item Name", "Quantity", "Price", "Total Price", "Date"])
            writer.writerows(sales_data)

        print(f"Sales exported successfully to {file_path}")
        messagebox.showinfo("Export Successful", f"Sales data exported successfully to {file_path}")

    except sqlite3.Error as e:
        messagebox.showerror("Export Error", f"SQLite error during export: {e}")
        print(f"SQLite error during export: {e}")
    except IOError as e:
         messagebox.showerror("Export Error", f"File writing error: {e}")
         print(f"File writing error during export: {e}")
    except Exception as e:
        messagebox.showerror("Export Error", f"An unexpected error occurred during export: {e}")
        print(f"General error during export: {e}")


# Function to read all data from the sales database for debugging
def check_sales_data():
    conn = get_connection()
    if not conn: return
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM sales")
        rows = cursor.fetchall()
        print("--- Sales Data ---")
        if rows:
            for row in rows:
                print(row)
        else:
            print("No data in sales table.")
        print("------------------")
    except sqlite3.Error as e:
        print(f"SQLite error checking sales data: {e}")
    finally:
        if conn: conn.close()


# --- Inventory Functions ---

def insert_inventory(item_name, stock_quantity):
    """Inserts or updates an item's stock quantity in the inventory table."""
    conn = get_connection()
    if not conn: return
    cursor = conn.cursor()
    try:
        # Use INSERT OR REPLACE to handle both new and existing items
        cursor.execute('''
            INSERT OR REPLACE INTO inventory (item_name, stock_quantity)
            VALUES (?, ?)
        ''', (item_name, stock_quantity))
        conn.commit()
        print(f"Inventory for '{item_name}' updated/inserted with quantity {stock_quantity}.")
    except sqlite3.Error as e:
        print(f"SQLite error while inserting/replacing inventory for '{item_name}': {e}")
        messagebox.showerror("DB Error", f"Failed to update inventory for {item_name}: {e}")
    finally:
        if conn: conn.close()


def get_inventory(item_name):
    """Gets the current stock quantity for a specific item. Returns 0 if not found."""
    conn = get_connection()
    if not conn: return 0 # Return 0 on connection error
    cursor = conn.cursor()
    try:
        cursor.execute('SELECT stock_quantity FROM inventory WHERE item_name = ?', (item_name,))
        result = cursor.fetchone()
        if result:
            return result[0] # Return the quantity
        else:
            # Item not found in inventory table
            return 0
    except sqlite3.Error as e:
        print(f"SQLite error getting stock for {item_name}: {e}")
        return 0 # Return 0 on query error
    finally:
        if conn: conn.close()


# --- !! ADDED FUNCTION !! ---
def update_stock(item_name, change_quantity):
    """
    Updates stock by a relative amount (e.g., -1 for selling one).
    Checks for sufficient stock before decreasing.
    Returns True on success, False on failure (e.g., insufficient stock or error).
    """
    conn = get_connection()
    if not conn: return False
    cursor = conn.cursor()
    try:
        # Get current stock first
        cursor.execute('SELECT stock_quantity FROM inventory WHERE item_name = ?', (item_name,))
        result = cursor.fetchone()
        current_stock = result[0] if result else 0 # Default to 0 if item doesn't exist yet

        # Check if sufficient stock for a decrease
        if change_quantity < 0 and current_stock + change_quantity < 0:
            print(f"Insufficient stock for {item_name}. Needed: {-change_quantity}, Available: {current_stock}")
            return False # Not enough stock

        # Calculate new stock and update
        new_stock = current_stock + change_quantity
        cursor.execute('UPDATE inventory SET stock_quantity = ? WHERE item_name = ?', (new_stock, item_name))
        conn.commit()
        # print(f"Stock updated for {item_name}. New stock: {new_stock}") # Optional confirmation
        return True # Update successful

    except sqlite3.Error as e:
        print(f"Error updating stock for {item_name}: {e}")
        conn.rollback() # Rollback changes on error
        return False # Indicate failure
    finally:
        if conn: conn.close()
# --- !! END ADDED FUNCTION !! ---


def fetch_all_inventory():
    """Fetches all items and their stock quantities from the inventory table."""
    conn = get_connection()
    if not conn: return []
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT item_name, stock_quantity FROM inventory ORDER BY item_name")
        rows = cursor.fetchall()
        # Convert list of tuples to list of dictionaries as expected by inventory_manager
        return [{"item_name": row[0], "stock_quantity": row[1]} for row in rows]
    except sqlite3.Error as e:
        print(f"SQLite error during fetch_all_inventory: {e}")
        messagebox.showerror("DB Error", f"Failed to fetch inventory list: {e}")
        return []
    finally:
        if conn: conn.close()

# --- End Inventory Functions ---

# Example Usage Block (Keep as in your original file)
if __name__ == "__main__":
    connect_database()  # Setup database and tables

    # Insert sample employees (optional)
    # Check if IDs exist before inserting to avoid errors if run multiple times
    # if not id_exist('employees', 'id', 1):
    #     insert_employee(1, "John Doe", "Doe", "1234567890", "Manager", "Male", 75000)
    # if not id_exist('employees', 'id', 2):
    #     insert_employee(2, "Jane Smith", "Smith", "9876543210", "Developer", "Female", 65000)

    # Insert initial inventory (Example - run only once or use insert_inventory)
    # insert_inventory("Castle Lager", 50)
    # insert_inventory("Savanna", 30)
    # insert_inventory("Coke", 100)

    print("\n--- Current Inventory ---")
    inventory_list = fetch_all_inventory()
    if inventory_list:
        for item in inventory_list:
            print(f"Item: {item['item_name']}, Stock: {item['stock_quantity']}")
    else:
        print("No inventory found.")
    print("-----------------------\n")


    # Fetch and display all employees
    employees = fetch_employees()
    if employees:
        print("--- Employees ---")
        for emp in employees:
            print(f"ID: {emp['id']}, Name: {emp['name']}, Position: {emp['position']}")
        print("-----------------\n")

    else:
        print("No employees found.")

    # Check current sales data
    print("\n--- Checking Sales Data ---")
    check_sales_data()
    print("-------------------------\n")

    # # Export sales to CSV
    # print("Attempting sales export...")
    # export_sales_to_csv()
    # --- NEW FUNCTION ---
def update_inventory_stock(item_name, new_stock_quantity):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE inventory SET stock_quantity = ? WHERE item_name = ?", (new_stock_quantity, item_name))
        conn.commit()
        return cursor.rowcount > 0
    except sqlite3.Error as e:
        print(f"Database error during inventory stock update: {e}")
        return False
    finally:
        conn.close()