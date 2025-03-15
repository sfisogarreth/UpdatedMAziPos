import sqlite3
from tkinter import messagebox
import datetime


class LiquorStorePOS:
    def __init__(self):
        self.create_table()  # Ensure the table exists when initializing

    def create_connection(self):
        """Establish connection to SQLite database."""
        return sqlite3.connect('liquor_store.db')

    def create_table(self):
        """Create the sales table if it does not exist."""
        conn = self.create_connection()
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sales (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                item_name TEXT,
                quantity INTEGER,
                price REAL,
                total_price REAL,
                date TEXT
            )
        ''')
        conn.commit()
        conn.close()

    def gather_cart_data(self):
        """Extracts cart data from the POS system."""
        cart_data = []
        for row_id in self.tree.get_children():
            values = self.tree.item(row_id)["values"]
            if values:
                item_name = values[1]
                quantity = values[2]
                price = float(values[3][1:])  # Convert price to float after removing "R"
                total_price = quantity * price
                cart_data.append((item_name, quantity, price, total_price))
        return cart_data

    def insert_into_database(self, cart_data):
        """Saves sales data into the database."""
        conn = self.create_connection()
        cursor = conn.cursor()
        for item_name, quantity, price, total_price in cart_data:
            cursor.execute('''
                INSERT INTO sales (item_name, quantity, price, total_price, date)
                VALUES (?, ?, ?, ?, ?)
            ''', (item_name, quantity, price, total_price, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        conn.commit()
        conn.close()

    def pay_bill(self):
        """Processes the payment and stores the sales data."""
        cart_data = self.gather_cart_data()
        if not cart_data:
            messagebox.showwarning("No Items", "There are no items in the cart to pay.")
            return

        self.insert_into_database(cart_data)
        self.tree.delete(*self.tree.get_children())  # Clear the cart
        self.update_total()  # Reset total
        messagebox.showinfo("Payment", "Bill paid and data saved to database!")