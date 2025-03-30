from customtkinter import *
from PIL import Image
import os
from tkinter import messagebox
from tkinter import ttk
import database  # Import your database.py module

def treeview_data():
    """Refresh TreeView with employee data from the database."""
    print("Refreshing TreeView...")  # Debugging
    for record in tree.get_children():
        tree.delete(record)  # Clear existing TreeView data

    employee_list = database.fetch_employees()  # Fetch employees from database
    print("Employee List from Database:", employee_list)  # Debugging
    for employee in employee_list:
        print("Inserting:", employee)  # Debugging
        tree.insert('', 'end', values=(employee['id'], employee['name'],
                                       employee['surname'], employee['phone'],
                                       employee['position'], employee['gender'],
                                       employee['salary']))
    print("Treeview Refresh Complete")

# Function to add employee
def add_employee():
    print("Adding Employee...")
    if Id_entry.get() == '' or nameEntry.get() == '' or snameEntry.get() == '' or phoneEntry.get() == '' or salaryEntry.get() == '':
        messagebox.showerror('Error', 'All fields should be entered')
    elif database.id_exist("employees", "id", Id_entry.get()):
        messagebox.showerror('Error', "ID Has Already Been Allocated")
    else:
        id = Id_entry.get()
        name = nameEntry.get()
        surname = snameEntry.get()
        phone = phoneEntry.get()
        position = roleOptBox.get()
        gender = genderDropBox.get()
        salary = salaryEntry.get()
        print(f"Data to insert: id={id}, name={name}, surname={surname}, phone={phone}, position={position}, gender={gender}, salary={salary}")
        database.insert_employee(id, name, surname, phone, position, gender, salary)
        treeview_data()  # Refresh TreeView
        print("Treeview refreshed after add")
        messagebox.showinfo('Success', 'Employee added successfully')
        clear_entries()

# Function to clear entry fields
def clear_entries():
    Id_entry.delete(0, END)
    nameEntry.delete(0, END)
    snameEntry.delete(0, END)
    phoneEntry.delete(0, END)
    roleOptBox.set(role_option[0])
    genderDropBox.set(gender_option[0])
    salaryEntry.delete(0, END)

# Initialize the main window
window = CTk()
window.geometry("1350x700+0+0")
window.configure(fg_color="#161C30")
window.resizable(False, False)
window.title("Employee Management System")

# Get the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the relative path to the image
emsImage = os.path.join(script_dir, "images", "emsImage.webp")

# Load the image
TopImage = CTkImage(Image.open(emsImage), size=(1350, 150))

# Create and place the image label
Image_label = CTkLabel(window, image=TopImage, text="", text_color="white")
Image_label.grid(row=0, column=0, columnspan=2)

left_frame = CTkFrame(window, fg_color="#161C30")
left_frame.grid(row=1, column=0)

# ID Entry
Id_label = CTkLabel(left_frame, text="ID", font=('arial', 20, 'bold'), text_color="white")
Id_label.grid(row=0, column=0, padx=25, pady=20, sticky="w")
Id_entry = CTkEntry(left_frame, font=('arial', 20, 'bold'), width=200)
Id_entry.grid(row=0, column=1)

# Name Entry
nameLabel = CTkLabel(left_frame, text="Name", font=('arial', 20, 'bold'), text_color="white")
nameLabel.grid(row=1, column=0, padx=25, pady=20, sticky="w")
nameEntry = CTkEntry(left_frame, font=('arial', 20, 'bold'), width=200)
nameEntry.grid(row=1, column=1)

# Surname Entry
snameLabel = CTkLabel(left_frame, text="Surname", font=('arial', 20, 'bold'), text_color="white")
snameLabel.grid(row=2, column=0, padx=25, pady=20, sticky="w")
snameEntry = CTkEntry(left_frame, font=('arial', 20, 'bold'), width=200)
snameEntry.grid(row=2, column=1)

# Phone Number Entry
phoneLabel = CTkLabel(left_frame, text="Phone Number", font=('arial', 20, 'bold'), text_color="white")
phoneLabel.grid(row=3, column=0, padx=25, pady=20, sticky="w")
phoneEntry = CTkEntry(left_frame, font=('arial', 20, 'bold'), width=200)
phoneEntry.grid(row=3, column=1)

# Position Entry
roleLabel = CTkLabel(left_frame, text="Position", font=('arial', 20, 'bold'), text_color="white")
roleLabel.grid(row=4, column=0, padx=25, pady=20, sticky="w")
role_option = ["Owner", "Manager", "Operator", "Bartender", "Waitron"]
roleOptBox = CTkComboBox(left_frame, values=role_option, width=200, font=('arial', 20, 'bold'), state="readonly")
roleOptBox.grid(row=4, column=1)
roleOptBox.set(role_option[1])

# Gender Entry
genderLabel = CTkLabel(left_frame, text="Gender", font=('arial', 20, 'bold'), text_color="white")
genderLabel.grid(row=5, column=0, padx=25, pady=20, sticky="w")
gender_option = ["Man", "Woman", "Gay", "Lesbian"]
genderDropBox = CTkComboBox(left_frame, values=gender_option, width=200, font=('arial', 20, 'bold'), state="readonly")
genderDropBox.grid(row=5, column=1)
genderDropBox.set(gender_option[0])

# Salary Entry
salaryLabel = CTkLabel(left_frame, text="Salary", font=('arial', 20, 'bold'), text_color="white")
salaryLabel.grid(row=6, column=0, padx=20, pady=20, sticky="w")
salaryEntry = CTkEntry(left_frame, font=('arial', 20, 'bold'), width=200)
salaryEntry.grid(row=6, column=1)

# Right frame
right_frame = CTkFrame(window)
right_frame.grid(row=1, column=1)

Search_option = ["Name", "ID", "Position", "Surname"]
searchByDropBox = CTkComboBox(right_frame, values=Search_option, width=150, font=('arial', 20, 'bold'), state="readonly")
searchByDropBox.grid(row=0, column=0)
searchByDropBox.set("Search By")

searchEntry = CTkEntry(right_frame, font=('arial', 20, 'bold'), width=200)
searchEntry.grid(row=0, column=1)

searchBtn = CTkButton(right_frame, text="Search", font=('arial', 20, 'bold'), text_color="white")
searchBtn.grid(row=0, column=2, pady=5)

ShowAllBtn = CTkButton(right_frame, text="Show All", font=('arial', 20, 'bold'), text_color="white", command=treeview_data)
ShowAllBtn.grid(row=0, column=3, pady=5)

tree = ttk.Treeview(right_frame, height=20)
tree.grid(row=1, column=0, columnspan=4)
tree["columns"] = ("ID", "Name", "Surname", "Phone", "Position", "Gender", "Salary")
tree.heading('ID', text="ID")
tree.heading('Name', text="Name")
tree.heading('Surname', text="Surname")
tree.heading('Phone', text="Phone")
tree.heading('Position', text="Position")
tree.heading('Gender', text="Gender")
tree.heading('Salary', text="Salary")
tree.config(show="headings")
tree.column('ID', anchor=CENTER, width=50)
tree.column('Name', anchor=CENTER, width=140)
tree.column('Surname', anchor=CENTER, width=140)
tree.column('Phone', anchor=CENTER, width=90)
tree.column('Position', anchor=CENTER, width=90)
tree.column('Gender', anchor=CENTER, width=50)
tree.column('Salary', anchor=CENTER, width=80)

style = ttk.Style()
style.configure('Treeview.Heading', font=('arial', 16, 'bold'), text_color="white")
style.configure('Treeview', font=('arial', 16, 'bold'), rowheight=20, background='#161C30', foreground="Red")
scrollbar = ttk.Scrollbar(right_frame, orient=VERTICAL)
scrollbar.grid(row=0, column=4, stick='ns')

btnFrame = CTkFrame(window, fg_color="#161C30")
btnFrame.grid(row=2, column=0, columnspan=2)

newBtn = CTkButton(btnFrame, text="New Employee", font=('arial', 20, 'bold'), text_color="white", width=160, corner_radius=15)
newBtn.grid(row=0, column=0, pady=5)

addBtn = CTkButton(btnFrame, text="Add Employee", font=('arial', 20, 'bold'), text_color="white", width=160, corner_radius=15, command=add_employee)
addBtn.grid(row=0, column=1, pady=5, padx=5)

updateBtn = CTkButton(btnFrame, text="Update Employee", font=('arial', 20, 'bold'), text_color="white", width=160, corner_radius=15)
updateBtn.grid(row=0, column=2, pady=5, padx=5)

deleteBtn = CTkButton(btnFrame, text="Delete Employee", font=('arial', 20, 'bold'), text_color="white", width=160, corner_radius=15)
deleteBtn.grid(row=0, column=3, pady=5, padx=5)

deleteAllBtn = CTkButton(btnFrame, text="Delete All", font=('arial', 20, 'bold'), text_color="white", width=160, corner_radius=15)
deleteAllBtn.grid(row=0, column=4, pady=5, padx=5)

treeview_data()

window.mainloop()