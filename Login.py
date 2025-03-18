from customtkinter import CTk, CTkLabel, CTkEntry, CTkButton, CTkImage
from PIL import Image
import os
from tkinter import messagebox

class InventorySystemLogin:
    def __init__(self, root):
        self.root = root
        self.root.resizable(False, False)
        self.root.title("Mazi Inventory System Login")

        self.root.geometry("1400x700+0+0")

        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        self.image_path = os.path.join(self.script_dir, "images", "bgImage.jpg")

        self.bg_image = CTkImage(Image.open(self.image_path), size=(1350, 700))
        self.image_label = CTkLabel(self.root, image=self.bg_image, text="")
        self.image_label.place(x=0, y=0)

        self.heading_label = CTkLabel(self.root, text="Mazi P.O.S System", bg_color="#232426", font=('Goudy Old Style', 30, 'bold'), text_color="#EC3A22")
        self.heading_label.place(x=60, y=370)

        self.user_name_entry = CTkEntry(self.root, placeholder_text="Enter your UserName", width=240)
        self.user_name_entry.place(x=60, y=420)

        self.password_entry = CTkEntry(self.root, placeholder_text="Enter your Password", width=240, show="*")
        self.password_entry.place(x=60, y=460)

        self.login_button = CTkButton(self.root, text="Login", bg_color="#232426", font=('Goudy Old Style', 30, 'bold'), command=self.login)
        self.login_button.place(x=110, y=495)

    def login(self):
        username = self.user_name_entry.get()
        password = self.password_entry.get()

        if not username or not password:
            messagebox.showerror("Error", "All fields must be filled")
        elif self.authenticate(username, password):
            messagebox.showinfo("Success", "Login was successful")
            self.root.destroy()
            self.load_main_application()
        else:
            messagebox.showerror("Error", "Wrong details entered")

    def authenticate(self, username, password):
        # Replace this with actual authentication logic
        return username == "admin" and password == "1234"

    def load_main_application(self):
        try:
            import ems  # Ensure this module exists
        except ImportError:
            messagebox.showerror("Error", "Main application module not found")

if __name__ == "__main__":
    root = CTk()
    app = InventorySystemLogin(root)
    root.mainloop()