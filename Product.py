from customtkinter import *
from PIL import Image, ImageTk
import os
import subprocess
from tkinter import messagebox, Label, Button
from tkinter import ttk

class LiquorStorePOS:
    def __init__(self):
        # Initialize main window
        self.root = CTk()
        self.root.title("Volume II Liquor Store - POS System")
        self.root.geometry("1350x750")
        self.root.configure(bg="#2C3E50")

        # Initialize styles
        self.init_styles()

        # Create frames
        self.create_frames()

        # Create UI components
        self.create_top_frame()
        self.create_sidebar_buttons()
        self.create_category_buttons()
        self.create_bill_section()

        # Initialize default category view
        self.cart = []
        self.current_category = None
        self.show_items("Beers")  # Display Beers by default
        self.show_items("Ciders")
        self.show_items("Tots")
        self.show_items("Drinks")
        self.show_items("Specials")
        self.show_items("Food")

        # Start the application
        self.root.mainloop()

    def init_styles(self):
        # Tkinter styles
        style = ttk.Style()
        style.configure("Top.TFrame", background="#000000")
        style.configure("Sidebar.TFrame", background="#000000")
        style.configure("Item.TFrame", background="#000000")
        style.configure("Bill.TFrame", background="#161C30")
        style.configure("Sidebar.TButton", font=("Arial", 14, "bold"), foreground="black", background="#2C3E50", padding=10)
        style.configure("Category.TButton", font=("Arial", 14, "bold"), foreground="black", background="#85C1E9", padding=10)
        style.configure("Item.TButton", font=("Arial", 14, "bold"), foreground="black", background="#85C1E9", padding=5)
        style.configure('Treeview.Heading', font=('Arial', 16, 'bold'), foreground="#000000")
        style.configure('Treeview', font=('Arial', 16, 'bold'), rowheight=20, background='#161C30', foreground="Red")

    def create_frames(self):
        self.Topframe = ttk.Frame(self.root, style="Top.TFrame")
        self.Topframe.grid(row=0, column=0, columnspan=6, sticky="nsew")

        self.sideBarFrame = ttk.Frame(self.root, style="Sidebar.TFrame")
        self.sideBarFrame.grid(row=1, column=0, sticky="ns", rowspan=2)

        self.CategoryFrame = ttk.Frame(self.root, style="Category.TFrame")
        self.CategoryFrame.grid(row=1, column=1, columnspan=2, sticky="nsew")

        self.BillFrame = ttk.Frame(self.root, style="Bill.TFrame")
        self.BillFrame.grid(row=2, column=2, sticky="nsew", columnspan=2)

        self.itemFrames = {}

        # Make the window responsive to resizing
        self.root.grid_rowconfigure(0, weight=1)  # Top frame
        self.root.grid_rowconfigure(1, weight=2)  # Categories and items
        self.root.grid_rowconfigure(2, weight=1)  # Bill section
        self.root.grid_columnconfigure(1, weight=3)  # Categories and items
        self.root.grid_columnconfigure(2, weight=2)  # Bill section
        self.root.grid_rowconfigure(1, weight=0)  # Adjust category frame weight
    def create_top_frame(self):
        # Title Label
        topframelbl = ttk.Label(self.Topframe, text="Volume II Liquor Store", font=("Arial", 26, "bold"),
                                background="#1A5276", foreground="white")
        topframelbl.pack(pady=15)

    def create_sidebar_buttons(self):
        sidebar_buttons = ["P.O.S", "Management", "Statistics", "Settings", "Orders", "Inventory", "Log Out"]

        for i, text in enumerate(sidebar_buttons):
            if text == "Log Out":
                ttk.Button(self.sideBarFrame, text=text, style="Sidebar.TButton", command=self.logout).grid(row=i, column=0, pady=10, padx=10, sticky="ew")
            else:
                ttk.Button(self.sideBarFrame, text=text, style="Sidebar.TButton").grid(row=i, column=0, pady=10, padx=10, sticky="ew")

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
            frame.grid(row=2, column=1, sticky="nsew")
            frame.grid_remove()

        for i, text in enumerate(self.categories.keys()):
            ttk.Button(
                self.CategoryFrame,
                text=text,
                style="Category.TButton",
                command=lambda text=text: self.show_items(text)
            ).grid(row=0, column=i, padx=5, pady=5)
    def create_bill_section(self):
        # Treeview as a Cart
        ttk.Label(self.BillFrame, text="Order Summary", font=("Arial", 14, "bold"), background="#0b8318").pack(
            anchor="w", padx=10, pady=5)

        self.tree = ttk.Treeview(self.BillFrame, columns=("ID", "Item", "Quantity", "Price"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Item", text="Item")
        self.tree.heading("Quantity", text="Quantity")
        self.tree.heading("Price", text="(R)Price")
        self.tree.column("ID", anchor="center", width=50)
        self.tree.column("Item", anchor="center", width=50)
        self.tree.column("Quantity", anchor="center", width=50)
        self.tree.column("Price", anchor="center", width=50)
        self.tree.pack(fill="both", expand=True)

        self.total_label = Label(self.BillFrame, text="TOTAL: R0.00", font=("Arial", 20, "bold"), bg="red", fg="black")
        self.total_label.pack(anchor="e", padx=10, pady=10)

        Button(self.BillFrame, text="Pay Bill", width=20, font=("Arial", 18, "bold"), bg="#58D68D").pack(pady=10)

    def add_to_cart(self, item, price):
        # Check if item already exists in cart
        for row_id in self.tree.get_children():
            values = self.tree.item(row_id)["values"]
            if values[1] == item:
                # Update quantity and price
                new_quantity = values[2] + 1
                new_price = new_quantity * price
                self.tree.item(row_id, values=(values[0], item, new_quantity, f"R{new_price:.2f}"))
                self.update_total()
                return

        # Add new item to Treeview
        item_id = len(self.cart) + 1
        self.tree.insert("", "end", values=(item_id, item, 1, f"R{price:.2f}"))
        self.cart.append((item_id, item, 1, price))
        self.update_total()

    def update_total(self):
        total = 0.0
        for row_id in self.tree.get_children():
            values = self.tree.item(row_id)["values"]
            price = float(values[3][1:])  # Remove "R" from price and convert to float
            total += price
        self.total_label.config(text=f"TOTAL: R{total:.2f}")

    def show_items(self, category):
        for frame in self.itemFrames.values():
            frame.grid_remove()
        self.itemFrames[category].grid()
        for widget in self.itemFrames[category].winfo_children():
            widget.destroy()

        max_columns = 5  # Maximum of 3 items per row
        for index, item in enumerate(self.categories[category]):
            name, image_path, price = item  # Unpack item details

            # Load and resize the image
            if os.path.exists(image_path):
                img = Image.open(image_path)
                img = img.resize((100, 100))  # Resize the image to fit
                photo = ImageTk.PhotoImage(img)

                # Create image label
                img_label = Label(self.itemFrames[category], image=photo, bg="#2C3E50")
                img_label.photo = photo  # Keep reference to avoid garbage collection
                img_label.grid(row=index // max_columns * 2, column=index % max_columns, padx=10, pady=10)

            # Create a button underneath the image
            button = ttk.Button(
                self.itemFrames[category],
                text=f"{name}\nR{price}",
                style="Item.TButton",
                command=lambda n=name, p=price: self.add_to_cart(n, p),
            )
            button.grid(row=index // max_columns * 2 + 1, column=index % max_columns, padx=10, pady=10)

    def logout(self):
        self.root.destroy()
        subprocess.run(["python", "Volume II POS.py"])


# Run the application
if __name__ == "__main__":
    LiquorStorePOS()