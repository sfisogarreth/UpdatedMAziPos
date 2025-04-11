# inventoryManager
import datetime
from customtkinter import *
from tkinter import messagebox, simpledialog, Label, Button, Toplevel
import tkinter as tk # Ensure this is here
from tkinter import ttk
from PIL import Image, ImageTk
import os
import subprocess
import database
import inventory_manager

print("DEBUG: dashboard.py script started") # <-- Add

class Mazi_Flow:
    def __init__(self):
        print("DEBUG: Mazi_Flow.__init__ started") # <-- Add
        self.root = CTk()
        print("DEBUG: CTk root window created") # <-- Add
        self.root.title("Mazi-Flow POS Dashboard")
        self.root.geometry("1400x750+0+0")
        self.root.configure(bg="#1A5276")

        # --- Database Initialization ---
        # Moved database connection check to __main__ block below
        # database.connect_database() # Ensure tables exist

        # --- Configuration ---
        self.low_stock_threshold = 3
        self.inventory_window = None # Initialize early

        print("DEBUG: Calling init_styles...") # <-- Add
        self.init_styles()
        print("DEBUG: Calling create_frames...") # <-- Add
        self.create_frames()
        print("DEBUG: Calling create_top_frame...") # <-- Add
        self.create_top_frame()
        print("DEBUG: Calling create_sidebar_buttons...") # <-- Add
        self.create_sidebar_buttons()
        print("DEBUG: Calling create_category_buttons...") # <-- Add
        self.create_category_buttons()
        print("DEBUG: Calling create_bill_section...") # <-- Add
        self.create_bill_section()
        print("DEBUG: UI Sections Created") # <-- Add

        self.cart = []
        self.current_category = None

        print("DEBUG: Calling show_items('Beers')...") # <-- Add
        # Wrap initial show_items in try-except to catch early errors
        try:
            self.show_items("Beers") # Show default category
        except Exception as e:
            print(f"ERROR during initial show_items: {e}") # <-- Add Error Catching
            messagebox.showerror("Initialization Error", f"Failed during initial item display: {e}")

        print("DEBUG: Mazi_Flow.__init__ finished, calling mainloop...") # <-- Add
        self.root.mainloop()
        print("DEBUG: mainloop finished (Window Closed)") # <-- Add

    # ... (rest of your methods: init_styles, create_frames, etc.) ...
    # Add prints inside complex methods if needed, e.g., inside create_frames
    # def create_frames(self):
    #     print("DEBUG: create_frames started")
    #     # ... frame creation ...
    #     print("DEBUG: create_frames finished")

    # ... (rest of the class methods)


# --- Main execution block ---
if __name__ == "__main__":
    print("DEBUG: __main__ block started") # <-- Add
    try:
        print("DEBUG: Attempting database connection/setup...") # <-- Add
        database.connect_database() # Check/create tables FIRST
        print("DEBUG: Database connection/setup finished.") # <-- Add

        print("DEBUG: Creating Mazi_Flow application instance...") # <-- Add
        app = Mazi_Flow()
        print("DEBUG: Mazi_Flow instance created (mainloop should be running)") # <-- Add

    except Exception as e:
        # Catch any unexpected error during startup
        print(f"FATAL ERROR during startup: {e}") # <-- Add
        import traceback
        traceback.print_exc() # Print detailed traceback
        messagebox.showerror("Fatal Error", f"Application failed to start:\n{e}")

    print("DEBUG: __main__ block finished (Should only see this after window closes)") # <-- Add