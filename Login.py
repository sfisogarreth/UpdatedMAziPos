from customtkinter import *
from PIL import Image
import os
from tkinter import messagebox

# Initialize the main window
root = CTk()
root.resizable(False, False)
root.title("Mazi Inventory System Login")
root.geometry("1350x700")
# Get the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the relative path to the image
image_path = os.path.join(script_dir, "images", "bgImage.jpg")

# Load the image
bgImage = CTkImage(Image.open(image_path), size=(1350,700))

# Create and place the image label
Image_label = CTkLabel(root, image=bgImage, text="")
Image_label.place(x=0, y=0)

heading_Label = CTkLabel(root, text="Mazi P.O.S System", bg_color="#232426", font=('Goudy Old Style', 30, 'bold'), text_color="#EC3A22")
heading_Label.place(x=60, y=370)

userNameEntry = CTkEntry(root, placeholder_text="Enter your UserName", width=240)
userNameEntry.place(x=60, y=420)

passwordEntry = CTkEntry(root, placeholder_text="Enter your Password", width=240, show="*")
passwordEntry.place(x=60, y=460)

def login():
    username = userNameEntry.get()
    password = passwordEntry.get()

    if username == "" or password == "":
        messagebox.showerror("Error", "All fields must be filled")
    elif username == "admin" and password == "1234":
        messagebox.showinfo("Success", "Login was successful")
        root.destroy()
        import ems  # Ensure this module exists
    else:
        messagebox.showerror("Error", "Wrong details entered")

# Create and place the login button
loginButton = CTkButton(root, text="Login", bg_color="#232426", font=('Goudy Old Style', 30, 'bold'), command=login)
loginButton.place(x=110, y=495)

# Run the main loop
root.mainloop()
