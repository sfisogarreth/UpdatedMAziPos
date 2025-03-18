import sqlite3


class InventoryManager:
    def __init__(self, db_path='Mazi~flow~order.db'):
        self.db_path = db_path

    def create_connection(self):
        return sqlite3.connect(self.db_path)

    def update_stock(self, item_name, quantity_sold):
        """ Deduct sold quantity from stock and notify if running low. """
        conn = self.create_connection()
        cursor = conn.cursor()

        # Check current stock
        cursor.execute("SELECT stock_quantity FROM inventory WHERE item_name = ?", (item_name,))
        result = cursor.fetchone()

        if result:
            current_stock = result[0]
            new_stock = max(0, current_stock - quantity_sold)  # Ensure stock doesn't go negative

            # Update stock in the database
            cursor.execute("UPDATE inventory SET stock_quantity = ? WHERE item_name = ?", (new_stock, item_name))
            conn.commit()

            if new_stock < 5:  # Set threshold for low stock warning
                print(f"Warning: Low stock for {item_name}! Only {new_stock} left. Consider restocking.")

        else:
            print(f"Item {item_name} not found in inventory.")

        conn.close()

    def add_stock(self, item_name, quantity):
        """ Increase stock for an item. """
        conn = self.create_connection()
        cursor = conn.cursor()

        # Check if item already exists
        cursor.execute("SELECT stock_quantity FROM inventory WHERE item_name = ?", (item_name,))
        result = cursor.fetchone()

        if result:
            # Update existing stock
            new_stock = result[0] + quantity
            cursor.execute("UPDATE inventory SET stock_quantity = ? WHERE item_name = ?", (new_stock, item_name))
        else:
            # Insert new item
            cursor.execute("INSERT INTO inventory (item_name, stock_quantity) VALUES (?, ?)", (item_name, quantity))

        conn.commit()
        conn.close()
        print(f"Stock updated: {item_name} now has {quantity} more units.")

    def check_low_stock(self):
        """ Retrieve and display items with low stock. """
        conn = self.create_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT item_name, stock_quantity FROM inventory WHERE stock_quantity < 5")
        low_stock_items = cursor.fetchall()
        conn.close()

        if low_stock_items:
            print("Low stock items:")
            for item in low_stock_items:
                print(f"{item[0]} - {item[1]} left")
        else:
            print("All items are sufficiently stocked.")


# Example Usage
if __name__ == "__main__":
    inventory = InventoryManager()
    inventory.check_low_stock()