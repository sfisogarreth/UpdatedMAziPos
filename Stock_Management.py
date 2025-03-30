import tkinter as tk
from tkinter import ttk
from customtkinter import *
import database  # Assuming your database.py is in the same directory
from tkinter import messagebox

class SalesDashboard:
    def __init__(self, root):
        self.root = root
        self.itemFrames = {}
        self.CategoryFrame = ttk.Frame(root)
        self.CategoryFrame.grid(row=0, column=0, sticky="nsew") # corrected to grid
        self.create_category_buttons()

    def create_category_buttons(self):
        self.categories = {
            "Beers": [
                ("Castle Lager", "images/Castlelager.jpeg", 29.99),
                ("Black Label", "images/black label.jpeg", 29.99),
                ("Castle Lite", "images/castleLite.jpeg", 29.99),
                ("Budweiser", "images/Budwiser.jpeg", 29.99),
                ("Heineken", "images/Heineken.jpeg", 34.99),
                ("Amstel Lager", "images/Amstel.jpeg", 34.99),
                ("W/Draught", "images/Windhoek Draught.jpeg", 34.99),
                ("W/Lager", "images/Windhoek.jpeg", 34.99),
                ("Miller", "images/Heineken.jpeg", 34.99)
            ],
            "Ciders": [
                ("Savanna", "images/savanna.jpeg", 34.99),
                ("Hunters Gold", "images/huntersgold.jpeg", 32.99),
                ("Smirnoff Spin", "images/Spin.jpeg", 34.99),
                ("Brutal", "images/Brutal.jpeg", 34.99),
                ("Bernini Blush", "images/beniniBlush.jpeg", 34.99),
                ("Black Crown", "images/Blackcrown.jpeg", 34.99),
                ("Strongbow", "images/Strongbow.jpeg", 34.99),
                ("Hunters Dry", "images/huntersdry.jpeg", 34.99)
            ],
            "Tots": [
                ("Jameson", "images/Jameson.jpeg", 39.99),
                ("Jack Daniels", "images/Jackdaniels.jpeg", 44.99),
                ("Chivas Regal", "images/chivas.jpeg", 42.99),
                ("Hennessy", "images/henessy.jpeg", 49.99),
                ("Bacardi", "images/Bacardi.jpeg", 24.99),
                ("Tequila", "images/Tequila.jpeg", 24.99),
                ("Bacardi", "images/Bacardi.jpeg", 24.99),
                ("Jagermeister", "images/Bacardi.jpeg", 24.99),
                ("Bacardi", "images/Bacardi.jpeg", 24.99),
            ],
            "Drinks": [
                ("Coke", "images/Coca Cola.jpeg", 24.99),
                ("Sprite", "images/sprite.jpeg", 24.99),
                ("Fanta", "images/fanta.jpeg", 24.99),
                ("Red Bull", "images/Redbul.jpeg", 38.99),
                ("Still Water", "images/still water.jpeg", 17.99),
                ("Sparkling", "images/Sparkling.jpeg", 17.99),
                ("Monster", "images/monsterenergy.jpeg", 17.99),
                ("Dragon", "images/Dragon.jpeg", 17.99)
            ],
            "Specials": [
                ("G & T", "images/2Gin&Tonic Sprite.jpeg", 74.99),
                ("Whisky&Coke", "images/2Whisky & Coke.jpeg", 64.99),
                ("Mojito", "images/mojito.jpeg", 64.99),
                ("Long Island", "images/LongIsland.jpeg", 64.99),
                ("Tequila Sunrise", "images/Tequila Sunrise.jpeg", 64.99)
            ],
            "Food": [
                ("Burger", "images/Burger.jpeg", 64.99),
                ("Pizza", "images/pizza.jpeg", 55.00),
                ("Hot Dog", "images/c.jpeg", 34.99),
                ("Steak", "images/Steak.jpeg", 79.99),
                ("Burger", "images/Burger.jpeg", 64.99),
                ("Pizza", "images/pizza.jpeg", 55.00),
                ("Hot Dog", "images/c.jpeg", 34.99),
                ("Steak", "images/Steak.jpeg", 79.99)
            ]
        }
        for category in self.categories.keys():
            frame = ttk.Frame(self.root, style="Item.TFrame")
            self.itemFrames[category] = frame
            frame.grid(row=2, column=0, sticky="nsew") # corrected to grid
            frame.grid_remove()

        for i, text in enumerate(self.categories.keys()):
            ttk.Button(
                self.CategoryFrame,
                text=text,
                style="Category.TButton",
                command=lambda text=text: self.show_items(text)
            ).grid(row=0, column=i, padx=5, pady=5)

    def show_items(self, category):
        for frame in self.itemFrames.values():
            frame.grid_remove()
        frame = self.itemFrames[category]
        frame.grid(row=2, column=0, sticky="nsew") # corrected to grid
        for i, item in enumerate(self.categories[category]):
            item_name, image_path, price = item
            ttk.Button(
                frame,
                text=item_name,
                command=lambda name=item_name: self.update_inventory_on_sale(name)
            ).grid(row=i, column=0, padx=5, pady=5)

    def update_inventory_on_sale(self, item_name):
        """Updates inventory when an item is sold."""
        try:
            current_stock = database.get_inventory(item_name)
            if current_stock > 0:
                new_stock = current_stock - 1  # Assuming quantity is 1
                database.insert_inventory(item_name, new_stock)
                messagebox.showinfo("Success", f"{item_name} stock updated.")
            else:
                messagebox.showerror("Error", f"{item_name} is out of stock.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

def inventory_page(window):
    inventory_frame = CTkFrame(window)

    # Treeview for inventory display
    tree = ttk.Treeview(inventory_frame, columns=("Item Name", "Stock Quantity"), show="headings")
    tree.heading("Item Name", text="Item Name")
    tree.heading("Stock Quantity", text="Stock Quantity")
    tree.pack(pady=20, padx=20, fill=BOTH, expand=True)

    def populate_treeview():
        for item in tree.get_children():
            tree.delete(item)
        inventory_data = database.fetch_all_inventory()
        for item in inventory_data:
            tree.insert('', 'end', values=(item['item_name'], item['stock_quantity']))

    populate_treeview()

    # Entry fields and buttons for adding stock
    add_item_name_label = CTkLabel(inventory_frame, text="Add Item Name:")
    add_item_name_label.pack(pady=5)
    add_item_name_entry = CTkEntry(inventory_frame)
    add_item_name_entry.pack(pady=5)

    add_stock_quantity_label = CTkLabel(inventory_frame, text="Add Stock Quantity:")
    add_stock_quantity_label.pack(pady=5)
    add_stock_quantity_entry = CTkEntry(inventory_frame)
    add_stock_quantity_entry.pack(pady=5)

    def add_stock():
        item_name = add_item_name_entry.get()
        stock_quantity = add_stock_quantity_entry.get()
        try:
            stock_quantity = int(stock_quantity)
            current_stock = database.get_inventory(item_name) or 0  # Get current stock or 0 if not found
            new_stock = current_stock + stock_quantity
            database.insert_inventory(item_name, new_stock)
            populate_treeview()
            messagebox.showinfo("Success", f"{stock_quantity} added to {item_name}.")
        except ValueError:
            messagebox.showerror("Error", "Stock Quantity must be a number.")
        add_item_name_entry.delete(0, END)
        add_stock_quantity_entry.delete(0, END)

    add_stock_button = CTkButton(inventory_frame, text="Add Stock", command=add_stock)
    add_stock_button.pack(pady=10)

    return inventory_frame

def switch_to_inventory():
    sales_dashboard.CategoryFrame.grid_remove() # changed to grid_remove
    inventory_frame.pack(fill=BOTH, expand=True)

def switch_to_sales():
    inventory_frame.pack_forget()
    sales_dashboard.CategoryFrame.grid(row=0, column=0, sticky="nsew") # changed to grid

if __name__ == "__main__":
    window = CTk()
    window.geometry("800x600")
    database.connect_database()

    inventory_frame = inventory_page(window)
    sales_dashboard = SalesDashboard(window)

    inventory_frame.grid_remove() #start with sales page

    inventory_button = CTkButton(window, text="Inventory", command=switch_to_inventory)
    inventory_button.grid(row=1, column=0, pady=10)

    sales_button = CTkButton(window, text="Sales", command=switch_to_sales)
    sales_button.grid(row=2, column=0, pady=10)

    window.mainloop()