import datetime
from customtkinter import *
from tkinter import messagebox, simpledialog, Label, Button
from tkinter import ttk
from PIL import Image, ImageTk
import os
import subprocess
import database  # Import database functions

class Mazi_Flow:
    DATABASE_NAME = "Mazi_Store.db"

    def __init__(self):
        self.root = CTk()
        self.root.title("Dashboard")
        self.root.geometry("1400x700+0+0")
        self.root.configure(bg="#1A5276")
        database.connect_database()  # Setup database and tables
        self.init_styles()
        self.create_frames()
        self.create_top_frame()
        self.create_sidebar_buttons()
        self.create_category_buttons()
        self.create_bill_section()
        self.cart = []
        self.current_category = None
        self.show_items("Beers")
        self.root.mainloop()

    def gather_cart_data(self):
        cart_data = []
        for row_id in self.tree.get_children():
            values = self.tree.item(row_id)["values"]
            item_name = values[1]
            quantity = values[2]
            price = float(values[3][1:].replace(',', ''))
            total_price = quantity * price
            cart_data.append((item_name, quantity, price, total_price))
        print(cart_data)
        return cart_data

    def pay_bill(self):
        cart_data = self.gather_cart_data()
        if not cart_data:
            messagebox.showwarning("No Items", "The cart is empty.")
            return

        current_datetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        for item_name, quantity, price, total_price in cart_data:
            database.insert_sale(item_name, quantity, price, total_price, current_datetime)

        self.tree.delete(*self.tree.get_children())
        self.update_total()
        messagebox.showinfo("Payment Success", "Bill paid and data saved to database.")

    def export_to_csv(self, Sales):
        database.export_sales_to_csv()

    def restock_item(self):
        item_name = simpledialog.askstring("Restock", "Enter item name:")
        if not item_name:
            return
        quantity = simpledialog.askinteger("Restock", "Enter quantity to restock:")
        if quantity and quantity > 0:
            print(f"Restocking {quantity} units of {item_name}")
            messagebox.showinfo("Restocked", f"{item_name} restocked with {quantity} units.")
        else:
            messagebox.showerror("Invalid Input", "Please enter a valid quantity.")

    def init_styles(self):
        # Tkinter styles
        style = ttk.Style()
        style.configure("Top.TFrame", background="#000000", font=("Arial", 24, "bold"))
        style.configure("Sidebar.TFrame", background="#000000")
        style.configure("Item.TFrame", background="#000000")
        style.configure("Bill.TFrame", background="#161C30")
        style.configure("Sidebar.TButton", font=("Arial", 14, "bold"), foreground="black", background="#2C3E50", padding=10)
        style.configure("Category.TButton", font=("Arial", 14, "bold"), foreground="black", background="#85C1E9", padding=10)
        style.configure("Item.TButton", font=("Arial", 14, "bold"), foreground="black", background="#85C1E9", padding=5)
        style.configure('Treeview.Heading', font=('Arial', 16, 'bold'), foreground="#000000")
        style.configure('Treeview', font=('Arial', 16, 'bold'), rowheight=20, background='#161C30', foreground="Red")

    def create_frames(self):
        self.Topframe = ttk.Frame(self.root, style="Top.TFrame", height=150)
        self.Topframe.grid(row=0, column=0, columnspan=6, sticky="nsew")
        self.Topframe.grid_propagate(False)

        self.sideBarFrame = ttk.Frame(self.root, style="Sidebar.TFrame")
        self.sideBarFrame.grid(row=1, column=0, sticky="ns", rowspan=2)

        self.CategoryFrame = ttk.Frame(self.root, style="Category.TFrame")
        self.CategoryFrame.grid(row=1, column=1, columnspan=2, sticky="nsew")

        self.BillFrame = ttk.Frame(self.root, style="Bill.TFrame")
        self.BillFrame.grid(row=2, column=2, sticky="nsew", columnspan=2)

        self.itemFrames = {}

        self.root.grid_rowconfigure(0, weight=0)
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_rowconfigure(2, weight=1)
        self.root.grid_columnconfigure(1, weight=2)
        self.root.grid_columnconfigure(2, weight=2)

    def create_top_frame(self):
        image_path = "images/inventory-management.png"
        abs_path = os.path.abspath(image_path)

        if os.path.exists(abs_path):
            try:
                img = Image.open(abs_path)
                img = img.resize((50, 50))
                self.bgImage = ImageTk.PhotoImage(img)
            except Exception as e:
                messagebox.showerror("Image Error", f"Error loading image: {e}")
                self.bgImage = None
        else:
            messagebox.showwarning("Missing Image", f"Image not found: {abs_path}")
            self.bgImage = None

        topframelbl = ttk.Label(
            self.Topframe,
            image=self.bgImage if self.bgImage else "",
            text="                       ***Mazi~Flow System*** ",
            font=("Goudy Old Style", 30, "bold"),
            compound="left",
            background="#000000",
            foreground="white"
        )
        topframelbl.pack(side="top", pady=5, padx=5)
        subtitlelbl = ttk.Label(
            self.Topframe,
            text="Welcome Gareth    Date: 08-07-2024    Time: 12:02:24 pm",
            font=("Goudy Old Style", 20, "bold"),
            compound="left",
            background="#000000",
            foreground="white",
        )
        subtitlelbl.pack(side="top", pady=5)
        logoutBtn = CTkButton(
            self.Topframe,
            text="Logout",
            font=("times new roman", 20, "bold"),
            text_color="white",
            fg_color="#00008B",
            hover_color="#FF0000"
        )
        logoutBtn.pack(side="right", padx=(10, 65), pady=10)

    def create_sidebar_buttons(self):
        image_path = "images/2011.jpg"
        img = Image.open(image_path)
        img = img.resize((200, 200))
        photo = ImageTk.PhotoImage(img)
        sidebar_image = ttk.Label(self.sideBarFrame, image=photo)
        sidebar_image.grid(row=0, column=0)
        sidebar_image.photo = photo
        sidebar_buttons = [
            ("P.O.S", None), ("Management", None), ("Statistics", None),
            ("Settings", None), ("Orders", None),
            ("Log Out", self.logout)
        ]
        for i, (text, command) in enumerate(sidebar_buttons):
            ttk.Button(
                self.sideBarFrame,
                text=text,
                style="Sidebar.TButton",
                command=command
            ).grid(row=i + 1, column=0, pady=2, padx=2, sticky="ew")

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
        ttk.Label(self.BillFrame, text="Order Summary", font=("Arial", 14, "bold"), background="#0b8318").pack(anchor="w", padx=10, pady=5)
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
        pay_button = Button(self.BillFrame, text="Pay Bill", width=20, font=("Arial", 18, "bold"), bg="#58D68D", command=self.pay_bill)
        pay_button.pack(pady=10)

    def add_to_cart(self, item, price):
        for row_id in self.tree.get_children():
            values = self.tree.item(row_id)["values"]
            if values[1] == item:
                new_quantity = values[2] + 1
                new_price = new_quantity * price
                self.tree.item(row_id, values=(values[0], item, new_quantity, f"R{new_price:.2f}"))
                self.update_total()
                return
        item_id = len(self.cart) + 1
        self.tree.insert("", "end", values=(item_id, item, 1, f"R{price:.2f}"))
        self.cart.append((item_id, item, 1, price))
        self.update_total()

    def update_total(self):
        total = 0.0
        for row_id in self.tree.get_children():
            values = self.tree.item(row_id)["values"]
            price = float(values[3][1:])
            total += price
        self.total_label.config(text=f"TOTAL: R{total:.2f}")

    def show_items(self, category):
        for frame in self.itemFrames.values():
            frame.grid_remove()
        self.itemFrames[category].grid()
        for widget in self.itemFrames[category].winfo_children():
            widget.destroy()
        max_columns = 5
        for index, item in enumerate(self.categories[category]):
            name, image_path, price = item
            if os.path.exists(image_path):
                img = Image.open(image_path)
                img = img.resize((100, 100))
                photo = ImageTk.PhotoImage(img)
                img_label = Label(self.itemFrames[category], image=photo, bg="#2C3E50")
                img_label.photo = photo
                img_label.grid(row=index // max_columns * 2, column=index % max_columns, padx=10, pady=10)
            button = ttk.Button(
                self.itemFrames[category],
                text=f"{name}\nR{price}",
                style="Item.TButton",
                command=lambda n=name, p=price: self.add_to_cart(n, p)
            )
            button.grid(row=index // max_columns * 2 + 1, column=index % max_columns, padx=10, pady=10)

    def logout(self):
        self.root.destroy()
        subprocess.run(["python", "Login.py"])

if __name__ == "__main__":
    Mazi_Flow()