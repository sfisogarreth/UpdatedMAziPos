import datetime
from customtkinter import *
# Make sure Toplevel is imported if not already
from tkinter import messagebox, simpledialog, Label, Button, Toplevel
from tkinter import ttk
from PIL import Image, ImageTk
import os
import subprocess
# Import YOUR database module
import database
# Import the inventory manager module (no changes needed here)
import inventory_manager
import tkinter as tk

class Mazi_Flow:
    DATABASE_NAME = "Mazi_Store.db"

    def __init__(self):
        self.root = CTk()
        self.root.title("Mazi-Flow POS Dashboard")
        self.root.geometry("1400x750+0+0")
        self.root.configure(bg="black") # Set root window background to black

        # --- Database Initialization (Uses your connect_database) ---
        database.connect_database() # Ensures tables exist

        # --- Configuration ---
        self.low_stock_threshold = 3 # Alert threshold

        self.init_styles()
        self.create_frames()
        self.create_top_frame()
        self.create_sidebar_buttons()
        self.create_category_buttons()
        self.create_bill_section()

        self.cart = [] # Internal tracking (less critical now)
        self.current_category = None
        self.show_items("Beers") # Show default category
        self.inventory_window = None # Track inventory window

        self.root.mainloop()

    def gather_cart_data(self):
        """Gathers data directly from the Treeview. Returns list of dicts or None on error."""
        cart_data = []
        if not self.tree.get_children():
            return cart_data

        for row_id in self.tree.get_children():
            values = self.tree.item(row_id)["values"]
            try:
                item_name = values[1]
                quantity = int(values[2])
                price_str = str(values[3]).replace('R', '').replace(',', '').strip()
                # Calculate price per item *before* appending
                # Ensure quantity is not zero to avoid division error
                if quantity == 0:
                    print(f"Warning: Item '{item_name}' in cart has quantity 0.")
                    continue # Skip item with zero quantity

                price_per_item = float(price_str) / quantity
                total_item_price = float(price_str) # Price string already represents total for the row

                cart_data.append({
                    "item_name": item_name,
                    "quantity": quantity,
                    "price_per_item": price_per_item, # Price for one unit
                    "total_price": total_item_price # Total price for the quantity in the row
                })
            except (IndexError, ValueError, TypeError, ZeroDivisionError) as e:
                print(f"Error processing cart row {row_id} with values {values}: {e}")
                messagebox.showerror("Cart Error", f"Error processing item: {values[1]}.\nCheck cart contents.\nError: {e}")
                return None # Indicate error

        return cart_data

    def pay_bill(self):
        """Processes payment, updates stock, records sales, checks low stock."""
        cart_data = self.gather_cart_data()

        if cart_data is None: return # Error during gathering
        if not cart_data:
            messagebox.showwarning("No Items", "The cart is empty.")
            return

        confirm = messagebox.askyesno("Confirm Payment", f"Proceed to pay R{self.calculate_total():.2f}?")
        if not confirm: return

        # Use the format expected by your database.py's 'date' column
        current_datetime_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        low_stock_alerts = []
        out_of_stock_alerts = []
        failed_items = []
        all_updates_successful = True

        for item_info in cart_data:
            item_name = item_info["item_name"]
            quantity_sold = item_info["quantity"]
            price_per_item = item_info["price_per_item"] # Use calculated price per item
            total_price = item_info["total_price"] # Use total price for the row

            # --- Critical Step: Update Stock using your database.update_stock ---
            # change_quantity is negative because we are selling
            stock_update_success = database.update_stock(item_name, -quantity_sold)

            if stock_update_success:
                # --- Record Sale using your database.insert_sale ---
                database.insert_sale(item_name, quantity_sold, price_per_item, total_price, current_datetime_str)

                # Check stock level *after* update for alerts
                # Use your database.get_inventory function
                new_stock = database.get_inventory(item_name)
                # Handle potential None return from get_inventory if error occurred, treat as 0
                if new_stock is None: new_stock = 0

                if 0 < new_stock <= self.low_stock_threshold:
                    low_stock_alerts.append(f"{item_name} ({new_stock} left)")
                elif new_stock == 0:
                    out_of_stock_alerts.append(f"{item_name}")
            else:
                # Stock update failed
                all_updates_successful = False
                current_stock_check = database.get_inventory(item_name) # Re-check actual stock
                failed_items.append(f"{item_name} (Requested: {quantity_sold}, Available: {current_stock_check})")
                print(f"Payment failed for {item_name} due to stock issue.")

        # --- Finalize ---
        if all_updates_successful:
            self.tree.delete(*self.tree.get_children()) # Clear cart
            self.update_total() # Reset total display
            messagebox.showinfo("Payment Success", "Bill paid and stock updated.")
            if low_stock_alerts:
                messagebox.showwarning("Low Stock Alert", "Low stock for:\n- " + "\n- ".join(low_stock_alerts))
            if out_of_stock_alerts:
                messagebox.showwarning("Out of Stock Alert", "Now out of stock:\n- " + "\n- ".join(out_of_stock_alerts))
        else:
            messagebox.showerror("Payment Failed", "Could not process payment for all items due to stock issues:\n- " + "\n- ".join(failed_items) + "\nPlease remove/adjust items and try again.")
            # Do NOT clear cart on failure

    def export_to_csv(self):
        """Exports sales data using the database function (no filename argument)."""
        print("Export Sales button clicked.")
        # Call your database function directly
        database.export_sales_to_csv()

    def init_styles(self):
            # (Keep your existing styles)
            style = ttk.Style()
            style.configure("Top.TFrame", background="#000000", font=("Arial", 24, "bold"))
            style.configure("Sidebar.TFrame", background="#000000")
            style.configure("Item.TFrame", background="#000000") # Keeping this for the item display background
            style.configure("Bill.TFrame", background="#000000")
            style.configure("Sidebar.TButton", font=("Arial", 14, "bold"), foreground="black", background="#000000", padding=10) # Black background for sidebar buttons, white text
            style.map("Sidebar.TButton", background=[('active', '#333333')]) # Darker black on active

            # --- Style for the Category Frame ---
            style.configure("CategoryFrame.TFrame", background="#000000") # Set CategoryFrame background to black

            # --- Style for the Category Buttons (Black, White, Red) ---
            style.configure("Category.TButton", font=("Arial", 14, "bold"), foreground="black", background="#000000", padding=10)
            style.map("Category.TButton",
                    foreground=[('active', '#000000')], # Red text on active
                    background=[('active', '#000000')]) # Darker black on active

            style.configure("Item.TButton", font=("Arial", 12), foreground="#000000", background="#000000", padding=5, width=15) # Dark gray/black for item buttons, white text
            style.map("Item.TButton", background=[('active', '#000000')]) # Slightly lighter gray/black on active

            style.configure('Treeview.Heading', font=('Arial', 12, 'bold'), foreground="black", background="black") # White heading text, black background
            style.configure('Treeview', font=('Arial', 11), rowheight=25, background="#000000", foreground="black", fieldackground="#000000") # White background for rows
            style.map('Treeview', background=[('selected', '#000000')], foreground=[('selected', 'black')]) # Red selection color
            
    def create_frames(self):
        # (Keep your existing frame creation - no changes needed here)
        self.Topframe = ttk.Frame(self.root, style="Top.TFrame", height=150)
        self.Topframe.grid(row=0, column=0, columnspan=4, sticky="nsew")
        self.Topframe.grid_propagate(False)

        self.sideBarFrame = ttk.Frame(self.root, style="Sidebar.TFrame", width=200)
        self.sideBarFrame.grid(row=1, column=0, sticky="ns", rowspan=3)
        self.sideBarFrame.grid_propagate(False)

        self.CategoryFrame = ttk.Frame(self.root, style="CategoryFrame.TFrame", height=60) # Corrected style name
        self.CategoryFrame.grid(row=1, column=1, columnspan=2, sticky="nsew")
        self.CategoryFrame.grid_propagate(False)

        self.ItemDisplayFrame = ttk.Frame(self.root, style="Item.TFrame") # Changed to ttk.Frame and using style
        self.ItemDisplayFrame.grid(row=2, column=1, columnspan=2, sticky="nsew") # Span 2 columns
        self.ItemDisplayFrame.grid_propagate(False) # Add this line

        self.BillFrame = ttk.Frame(self.root, style="Bill.TFrame", width=450)
        self.BillFrame.grid(row=1, column=3, sticky="nsew", rowspan=3)
        self.BillFrame.grid_propagate(False)

        self.root.grid_rowconfigure(0, weight=0)
        self.root.grid_rowconfigure(1, weight=0)
        self.root.grid_rowconfigure(2, weight=1) # Item display expands vertically
        self.root.grid_rowconfigure(3, weight=0) # Keep row 3 weight 0 unless needed

        self.root.grid_columnconfigure(0, weight=0) # Sidebar fixed
        self.root.grid_columnconfigure(1, weight=1) # Item display col 1 expands
        self.root.grid_columnconfigure(2, weight=1) # Item display col 2 expands
        self.root.grid_columnconfigure(3, weight=0) # Bill frame fixed

        self.itemFrames = {}

    def create_top_frame(self):
        # (Keep existing, ensure update_time uses a label created here)
        self.time_label = ttk.Label(
            self.Topframe, text="", font=("Goudy Old Style", 16),
            compound="left", background="#000000", foreground="white",
        )
        self.time_label.place(relx=0.98, rely=0.85, anchor='se')
        self.update_time()

        # --- Logo ---
        image_path = "images/inventory-management.png" # Ensure path is correct
        abs_path = os.path.abspath(image_path)
        if os.path.exists(abs_path):
            try:
                img = Image.open(abs_path); img = img.resize((50, 50))
                self.bgImage = ImageTk.PhotoImage(img)
            except Exception as e:
                messagebox.showerror("Image Error", f"Error loading image: {e}"); self.bgImage = None
        else:
            print(f"Warning: Logo image not found: {abs_path}"); self.bgImage = None

        topframelbl = ttk.Label(
            self.Topframe, image=self.bgImage if self.bgImage else None, text="   Mazi~Flow System   ",
            font=("Goudy Old Style", 30, "bold"), compound="left", background="#000000", foreground="white"
        )
        topframelbl.place(relx=0.5, rely=0.3, anchor='center')

        # --- Logout Button ---
        logoutBtn = CTkButton(
            self.Topframe, text="Logout", font=("times new roman", 16, "bold"), text_color="white",
            fg_color="#00008B", hover_color="#FF0000", width=100, command=self.logout
        )
        logoutBtn.place(relx=0.98, rely=0.2, anchor='ne')


    def update_time(self):
        """Updates the time label every second."""
        # NOTE: Assumes 'Gareth' is the user. This could be dynamic later.
        now = datetime.datetime.now()
        current_time = now.strftime("%Y-%m-%d %H:%M:%S")
        display_text = f"Welcome Gareth | {current_time}"
        try:
            self.time_label.config(text=display_text)
            # Schedule the next update
            self.root.after(1000, self.update_time)
        except tk.TclError:
            pass # Avoid error if window is closed while timer is running


    def create_sidebar_buttons(self):
        # (Keep existing sidebar structure, commands point to correct functions)
        # Optional: Add image if you have one
        # image_path = "images/your_sidebar_image.jpg" ...
        image_path = "images/2011.jpg"

        abs_path = os.path.abspath(image_path)   # Get absolute path



        if os.path.exists(abs_path):

            try:

                img = Image.open(abs_path)

                img = img.resize((200, 200))

                photo = ImageTk.PhotoImage(img)

                sidebar_image = ttk.Label(self.sideBarFrame, image=photo)

                sidebar_image.grid(row=0, column=0)

                sidebar_image.photo = photo

            except Exception as e:

                messagebox.showerror("Image Error", f"Error loading image: {e}")

                # Optionally, set a placeholder or handle the error gracefully

                sidebar_image = ttk.Label(self.sideBarFrame, text="Image Error")

                sidebar_image.grid(row=0, column=0)

        else:

            messagebox.showwarning("Missing Image", f"Image not found: {abs_path}")

            sidebar_image = ttk.Label(self.sideBarFrame, text="Image Missing")

            sidebar_image.grid(row=0, column=0)


        sidebar_buttons = [
            ("P.O.S", lambda: self.show_items(self.current_category or "Beers")),
            ("Inventory", self.open_inventory_manager),
            ("Export Sales", self.export_to_csv), # Command calls the updated export function
            # Add other buttons if needed
            ("Log Out", self.logout)
        ]
        start_row = 1 # Start from row 0 if no image
        for i, (text, command) in enumerate(sidebar_buttons):
            btn = ttk.Button(
                self.sideBarFrame, text=text, style="Sidebar.TButton", command=command
            )
            btn.grid(row=start_row + i, column=0, pady=5, padx=10, sticky="ew")




    def open_inventory_manager(self):
        if self.inventory_window is None or not self.inventory_window.winfo_exists():
            self.inventory_window = Toplevel(self.root)
            self.inventory_window.title("Manage Inventory") # More professional title
            self.inventory_window.geometry("500x600") # Slightly larger
            self.inventory_window.transient(self.root)
            self.inventory_window.grab_set()

            # --- Improved Styling ---
            self.inventory_window.config(bg="#2c3e50") # Darker background

            # Main frame for content
            main_frame = CTkFrame(self.inventory_window, fg_color="#34495e", corner_radius=10)
            main_frame.pack(padx=15, pady=15, fill="both", expand=True)

            # Title Label
            title_label = CTkLabel(main_frame, text="Inventory Management", font=("Arial", 20, "bold"), text_color="white")
            title_label.pack(pady=(10, 15))

            # --- Functionality Buttons ---
            button_frame = CTkFrame(main_frame, fg_color="transparent")
            button_frame.pack(fill="x", padx=10, pady=(5, 10))

            load_button = CTkButton(button_frame, text="Load Existing", command=self.load_existing_inventory,
                                     fg_color="darkblue", text_color="white", hover_color="blue")
            load_button.pack(side="left", padx=5)

            clear_all_button = CTkButton(button_frame, text="Clear All", command=self.clear_all_inventory_fields,
                                          fg_color="red", text_color="white", hover_color="darkred")
            clear_all_button.pack(side="left", padx=5)

            # Create a Canvas with Scrollbar
            inventory_canvas = tk.Canvas(main_frame, bg="#34495e", highlightthickness=0)
            inventory_canvas.pack(side="left", fill="both", expand=True, padx=10)

            inventory_scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=inventory_canvas.yview)
            inventory_scrollbar.pack(side="right", fill="y")

            inventory_canvas.configure(yscrollcommand=inventory_scrollbar.set)
            inventory_canvas.bind('<Configure>', lambda e: inventory_canvas.configure(scrollregion = inventory_canvas.bbox("all")))

            # Frame inside the Canvas for inventory items
            self.inventory_frame = CTkFrame(inventory_canvas, fg_color="#34495e")
            inventory_canvas.create_window((0, 0), window=self.inventory_frame, anchor="nw")

            self.inventory_entries = {} # To store entry fields for each item
            row_num = 0

            # Get all unique item names from your categories
            all_items = set()
            for category_items in self.categories.values():
                for item_name, _, _ in category_items:
                    all_items.add(item_name)

            self.sorted_items = sorted(list(all_items)) # Store sorted list for loading

            for item_name in self.sorted_items:
                item_label = CTkLabel(self.inventory_frame, text=item_name, text_color="lightblue")
                item_label.grid(row=row_num, column=0, padx=5, pady=5, sticky="w")

                stock_entry = CTkEntry(self.inventory_frame, width=70, border_color="red", text_color="white")
                stock_entry.grid(row=row_num, column=1, padx=5, pady=5, sticky="e")
                self.inventory_entries[item_name] = stock_entry
                row_num += 1

            save_button = CTkButton(main_frame, text="Save Inventory", command=self.save_initial_inventory,
                                     fg_color="darkblue", text_color="white", hover_color="blue")
            save_button.pack(pady=20)

            # Update scroll region after items are added
            self.inventory_frame.update_idletasks()
            inventory_canvas.config(scrollregion=inventory_canvas.bbox("all"))

            self.inventory_window.protocol("WM_DELETE_WINDOW", self._on_inventory_close)
        else:
            self.inventory_window.lift()
            self.inventory_window.focus_set()

    def save_initial_inventory(self):
        for item_name, entry in self.inventory_entries.items():
            stock_str = entry.get()
            try:
                stock_quantity = int(stock_str)
                database.insert_inventory(item_name, stock_quantity)
            except ValueError:
                messagebox.showerror("Input Error", f"Invalid quantity for {item_name}. Please enter a number.")
            except Exception as e:
                messagebox.showerror("Database Error", f"Error saving inventory for {item_name}: {e}")
        messagebox.showinfo("Success", "Inventory levels saved successfully!")
        if self.inventory_window:
            self.inventory_window.destroy()
            self.inventory_window = None

    def load_existing_inventory(self):
        """Loads the current inventory levels from the database into the entry fields."""
        current_inventory = database.fetch_all_inventory()
        if current_inventory:
            inventory_dict = {item['item_name']: item['stock_quantity'] for item in current_inventory}
            for item_name in self.sorted_items:
                if item_name in inventory_dict and item_name in self.inventory_entries:
                    self.inventory_entries[item_name].delete(0, END)
                    self.inventory_entries[item_name].insert(0, str(inventory_dict[item_name]))
                elif item_name in self.inventory_entries:
                    self.inventory_entries[item_name].delete(0, END)
                    self.inventory_entries[item_name].insert(0, "0") # Default to 0 if not found
        else:
            messagebox.showinfo("Info", "No existing inventory data found in the database.")

    def clear_all_inventory_fields(self):
        """Clears all the quantity entry fields in the inventory window."""
        confirm = messagebox.askyesno("Confirm Clear", "Are you sure you want to clear all inventory quantities?")
        if confirm:
            for entry in self.inventory_entries.values():
                entry.delete(0, END)
                entry.insert(0, "0")

    def _on_inventory_close(self):
        # (Keep existing - no changes needed here)
        if self.inventory_window:
            self.inventory_window.destroy()
        self.inventory_window = None
        # Ensure grab is released if the main window still exists
        if self.root.winfo_exists():
            try:
                self.root.grab_release()
            except tk.TclError:
                pass # Ignore error if grab wasn't set


    def create_category_buttons(self):
        # (Keep existing category data and button creation logic)
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
        # Create placeholder frames within ItemDisplayFrame
        for category in self.categories.keys():
            frame = CTkFrame(self.ItemDisplayFrame, fg_color="black") # Set fg_color to black
            self.itemFrames[category] = frame

        # Create category selection buttons in CategoryFrame
        num_categories = len(self.categories.keys())
        for i, text in enumerate(self.categories.keys()):
            btn = ttk.Button(
                self.CategoryFrame, text=text, style="Category.TButton",
                command=lambda t=text: self.show_items(t)
            )
            btn.grid(row=0, column=i, padx=5, pady=5, sticky="ew")
            self.CategoryFrame.grid_columnconfigure(i, weight=1) # Make buttons expand

    def create_bill_section(self):
        # (Import tkinter as tk at the top of your dashboard.py file if not already done)
        import tkinter as tk # Make sure this import exists

        # Create the Treeview within the BillFrame
        bill_title = CTkLabel(self.BillFrame, text="Order Summary", font=("Arial", 16, "bold"), text_color="white", fg_color="#0b8318")
        bill_title.pack(fill=tk.X, padx=0, pady=0) # Use tk.X

        tree_container = CTkFrame(self.BillFrame, fg_color="transparent") # Container for tree and scrollbar
        tree_container.pack(fill="both", expand=True, padx=5, pady=5)

        bill_scrollbar = ttk.Scrollbar(tree_container)
        bill_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Assign the Treeview to self.tree
        self.tree = ttk.Treeview(tree_container, columns=("ID", "Item", "Qty", "Price"), show="headings", style='Treeview', yscrollcommand=bill_scrollbar.set)
        self.tree.heading("ID", text="ID"); self.tree.column("ID", anchor="center", width=40, stretch=False)
        self.tree.heading("Item", text="Item"); self.tree.column("Item", anchor="w", width=180)
        self.tree.heading("Qty", text="Qty"); self.tree.column("Qty", anchor="center", width=50, stretch=False)
        self.tree.heading("Price", text="(R) Price"); self.tree.column("Price", anchor="e", width=100)

        self.tree.pack(side=tk.LEFT, fill="both", expand=True)

        # *** CORRECTED LINE HERE ***
        # Configure the scrollbar command to use the yview method of self.tree
        bill_scrollbar.config(command=self.tree.yview)

        # Add buttons for modifying cart items
        modify_frame = CTkFrame(self.BillFrame, fg_color="transparent")
        # Use fill='x' for CTkFrame if you want horizontal fill
        modify_frame.pack(fill='x', pady=5)

        remove_button = CTkButton(modify_frame, text="Remove Sel.", command=self.remove_selected_item, width=100)
        remove_button.pack(side=tk.LEFT, padx=10)

        clear_button = CTkButton(modify_frame, text="Clear All", command=self.clear_cart, width=100, fg_color="orange", hover_color="dark orange")
        clear_button.pack(side=tk.LEFT, padx=10)

        # Total Label and Pay Button
        self.total_label = CTkLabel(self.BillFrame, text="TOTAL: R 0.00", font=("Arial", 20, "bold"), text_color="black", fg_color="yellow", corner_radius=5)
        self.total_label.pack(fill='x', padx=10, pady=(10, 5)) # Use fill='x'

        pay_button = CTkButton(self.BillFrame, text="Pay Bill", font=("Arial", 18, "bold"), fg_color="#58D68D", hover_color="#4CAF50", command=self.pay_bill)
        pay_button.pack(fill='x', padx=10, pady=(5, 10)) # Use fill='x'

    def add_to_cart(self, item_name, price_per_item):
        """Adds an item to the cart, checking stock using database.get_inventory."""

        # 1. Check Available Stock using your database.get_inventory
        available_stock = database.get_inventory(item_name)
        # Handle None return as 0 stock
        if available_stock is None: available_stock = 0

        if available_stock <= 0:
            messagebox.showerror("Out of Stock", f"Sorry, '{item_name}' is out of stock or not in inventory.")
            return

        # 2. Check if item already in cart
        existing_row_id = None
        current_cart_quantity = 0
        for row_id in self.tree.get_children():
            values = self.tree.item(row_id)["values"]
            if values[1] == item_name:
                existing_row_id = row_id
                current_cart_quantity = int(values[2])
                break

        # 3. Check if adding one more exceeds stock
        if current_cart_quantity + 1 > available_stock:
            messagebox.showerror("Insufficient Stock", f"Cannot add more '{item_name}'.\nAvailable: {available_stock} | In Cart: {current_cart_quantity}")
            return

        # 4. Add or Update Treeview
        if existing_row_id:
            new_quantity = current_cart_quantity + 1
            new_total_price = new_quantity * price_per_item
            self.tree.item(existing_row_id, values=(values[0], item_name, new_quantity, f"R {new_total_price:.2f}"))
        else:
            item_id = len(self.tree.get_children()) + 1
            self.tree.insert("", "end", values=(item_id, item_name, 1, f"R {price_per_item:.2f}"))

        # 5. Update Total Display
        self.update_total()


    def remove_selected_item(self):
        # (Keep existing - no changes needed here)
        selected_items = self.tree.selection()
        if not selected_items:
            messagebox.showwarning("No Selection", "Please select an item to remove.")
            return
        confirm = messagebox.askyesno("Confirm Removal", f"Remove {len(selected_items)} selected item(s)?")
        if confirm:
            for item_id in selected_items: self.tree.delete(item_id)
            self.update_total()

    def clear_cart(self):
        # (Keep existing - no changes needed here)
        if not self.tree.get_children():
            messagebox.showinfo("Empty Cart", "The cart is already empty."); return
        confirm = messagebox.askyesno("Confirm Clear Cart", "Remove all items from the cart?")
        if confirm:
            self.tree.delete(*self.tree.get_children())
            self.update_total()


    def calculate_total(self):
        # (Keep existing - no changes needed here)
        total = 0.0
        for row_id in self.tree.get_children():
            try:
                values = self.tree.item(row_id)["values"]
                price_str = str(values[3]).replace('R', '').replace(',', '').strip()
                total += float(price_str)
            except (IndexError, ValueError, TypeError) as e:
                print(f"Error calculating total for row {row_id}, values {values}: {e}")
        return total

    def update_total(self):
        # (Keep existing - no changes needed here)
        total = self.calculate_total()
        self.total_label.configure(text=f"TOTAL: R {total:.2f}")


    def show_items(self, category):
        """Displays items for the category, checking stock via database.get_inventory."""
        if category not in self.itemFrames:
            print(f"Error: Category frame for '{category}' not found.")
            return
        self.current_category = category

        # Hide other category frames
        for cat, frame in self.itemFrames.items(): frame.grid_forget()

        category_item_frame = self.itemFrames[category]
        category_item_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.ItemDisplayFrame.grid_rowconfigure(0, weight=1)
        self.ItemDisplayFrame.grid_columnconfigure(0, weight=1)

        # Clear previous items
        for widget in category_item_frame.winfo_children(): widget.destroy()

        items_in_category = self.categories[category]
        max_columns = 4
        row_num, col_num = 0, 0

        for index, item_data in enumerate(items_in_category):
            name, image_path, price = item_data
            # --- Check stock using your database.get_inventory ---
            current_stock = database.get_inventory(name)
            # Handle None return as 0
            if current_stock is None: current_stock = 0

            item_container = CTkFrame(category_item_frame, fg_color="#2C3E50", corner_radius=5)
            item_container.grid(row=row_num, column=col_num, padx=10, pady=10, sticky="nsew")
            category_item_frame.grid_columnconfigure(col_num, weight=1)

            # Image (keep existing logic)
            abs_image_path = os.path.abspath(image_path)
            if os.path.exists(abs_image_path):
                try:
                    img = Image.open(abs_image_path); img = img.resize((80, 80))
                    photo = ImageTk.PhotoImage(img)
                    img_label = Label(item_container, image=photo, bg="#2C3E50")
                    img_label.photo = photo; img_label.pack(pady=(5, 0))
                except Exception as e:
                    print(f"Err loading img {abs_image_path}: {e}"); Label(item_container, text="Img Err", bg="#2C3E50", fg="red").pack(pady=(5,0))
            else: Label(item_container, text="No Img", bg="#2C3E50", fg="grey").pack(pady=(5,0))

            # Button Text/State based on stock
            button_text = f"{name}\nR {price:.2f}"
            button_state = tk.NORMAL
            button_fg_color, hover_color = "#85C1E9", "#AED6F1" # Defaults

            # Note: Your get_inventory returns 0 if not found, so no separate 'Not Added' state needed unless you want it explicitly
            if current_stock == 0:
                button_text += "\n(Out of Stock)"
                button_state = tk.DISABLED
                button_fg_color, hover_color = "#E74C3C", "#C0392B" # Red
            elif current_stock <= self.low_stock_threshold:
                button_text += f"\n(Low: {current_stock})"
                button_fg_color, hover_color = "#F39C12", "#E67E22" # Orange

            # Item Button
            button = CTkButton(
                item_container, text=button_text, font=("Arial", 11),
                fg_color=button_fg_color, hover_color=hover_color, text_color="black",
                command=lambda n=name, p=price: self.add_to_cart(n, p),
                state=button_state, width=130
            )
            button.pack(pady=5, padx=5, fill=tk.X)

            # Update grid position
            col_num += 1
            if col_num >= max_columns: col_num = 0; row_num += 1


    def logout(self):
        # (Keep existing logout logic)
        confirm = messagebox.askyesno("Logout", "Are you sure you want to logout?")
        if confirm:
            if self.inventory_window and self.inventory_window.winfo_exists():
                self.inventory_window.destroy()
            self.root.destroy()
            try:
                print("Attempting to run login.py...")
                subprocess.Popen(["python", "login.py"])
            except FileNotFoundError:
                messagebox.showerror("Error", "login.py not found!")
            except Exception as e:
                messagebox.showerror("Error", f"Could not run login.py: {e}")

if __name__ == "__main__":
    Mazi_Flow()