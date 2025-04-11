import tkinter as tk
from tkinter import ttk
from customtkinter import *
import database  # Assuming your database.py is in the same directory
from tkinter import messagebox

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

    # --- Section for Editing Stock ---
    edit_frame = CTkFrame(inventory_frame)
    edit_frame.pack(pady=10, padx=20, fill="x")

    item_name_label_edit = CTkLabel(edit_frame, text="Item Name:")
    item_name_label_edit.grid(row=0, column=0, padx=5, pady=5, sticky="w")
    item_name_entry_edit = CTkEntry(edit_frame, state="readonly") # Make it readonly
    item_name_entry_edit.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

    stock_quantity_label_edit = CTkLabel(edit_frame, text="New Stock Quantity:")
    stock_quantity_label_edit.grid(row=1, column=0, padx=5, pady=5, sticky="w")
    stock_quantity_entry_edit = CTkEntry(edit_frame)
    stock_quantity_entry_edit.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

    def update_stock():
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select an item to update.")
            return
        item_id = selected_item[0]
        item_name = tree.item(item_id, 'values')[0]
        new_stock_str = stock_quantity_entry_edit.get()
        try:
            new_stock = int(new_stock_str)
            if new_stock >= 0:
                database.update_inventory_stock(item_name, new_stock) # Call new database function
                populate_treeview()
                messagebox.showinfo("Success", f"Stock for '{item_name}' updated to {new_stock}.")
                # Clear the entry fields after successful update
                item_name_entry_edit.configure(state="normal")
                item_name_entry_edit.delete(0, END)
                item_name_entry_edit.configure(state="readonly")
                stock_quantity_entry_edit.delete(0, END)
            else:
                messagebox.showerror("Error", "Stock quantity cannot be negative.")
        except ValueError:
            messagebox.showerror("Error", "Invalid stock quantity. Please enter a number.")

    def populate_edit_fields(event):
        selected_item = tree.selection()
        if selected_item:
            item_id = selected_item[0]
            item_details = tree.item(item_id, 'values')
            item_name = item_details[0]
            stock_quantity = item_details[1]
            item_name_entry_edit.configure(state="normal")
            item_name_entry_edit.delete(0, END)
            item_name_entry_edit.insert(0, item_name)
            item_name_entry_edit.configure(state="readonly")
            stock_quantity_entry_edit.delete(0, END)
            stock_quantity_entry_edit.insert(0, stock_quantity)

    tree.bind("<ButtonRelease-1>", populate_edit_fields) # Select item to populate fields

    update_stock_button = CTkButton(edit_frame, text="Update Stock", command=update_stock)
    update_stock_button.grid(row=2, column=0, columnspan=2, padx=5, pady=10)

    # --- Section for Adding New Items (Keep this for now) ---
    add_frame = CTkFrame(inventory_frame)
    add_frame.pack(pady=10, padx=20, fill="x")

    item_name_label_add = CTkLabel(add_frame, text="Item Name:")
    item_name_label_add.pack(pady=5)
    item_name_entry_add = CTkEntry(add_frame)
    item_name_entry_add.pack(pady=5)

    stock_quantity_label_add = CTkLabel(add_frame, text="Stock Quantity:")
    stock_quantity_label_add.pack(pady=5)
    stock_quantity_entry_add = CTkEntry(add_frame)
    stock_quantity_entry_add.pack(pady=5)

    def add_new_item():
        item_name = item_name_entry_add.get()
        stock_quantity = stock_quantity_entry_add.get()
        try:
            stock_quantity = int(stock_quantity)
            if stock_quantity >= 0:
                database.insert_inventory(item_name, stock_quantity)
                populate_treeview()
                item_name_entry_add.delete(0, END)
                stock_quantity_entry_add.delete(0, END)
            else:
                messagebox.showerror("Error", "Stock quantity cannot be negative.")
        except ValueError:
            messagebox.showerror("Error", "Stock Quantity must be a number.")

    add_update_button = CTkButton(add_frame, text="Add New Item", command=add_new_item)
    add_update_button.pack(pady=10)

    return inventory_frame

# You can remove the SalesDashboard class definition from this file
# unless you have other uses for it within inventory_manager.py
# class SalesDashboard:
#     def __init__(self, root):
#         self.root = root
#         self.itemFrames = {}
#         self.CategoryFrame = ttk.Frame(root)
#         self.CategoryFrame.grid(row=0, column=0, sticky="nsew")  # Use grid here