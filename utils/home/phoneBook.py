import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from PIL import Image, ImageTk

from .utils import *

class PhoneBookPanel:
    def __init__(self, content_frame):
        self.content_frame = content_frame
        self.left_phone_book = None
        self.right_phone_book = None
        self.contacts_list = None

        conn = sqlite3.connect("phonebook.db")
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS contacts
                        (name TEXT, number TEXT)''')
        conn.close()

    def create_left_frame(self):
        # Create sender and receiver frames
        width_ = self.content_frame.winfo_width() / 2 - 20;
        height_ = self.content_frame.winfo_height() / 2 - 10;

        left_panel_bg = "#c1dbcf"
        font=("Comic Sans MS", 12, "bold")
        fg = "#fc6603"
        light_black = "#383532"

        if self.left_phone_book == None:
            self.left_phone_book = tk.Frame(self.content_frame, bg=left_panel_bg, borderwidth=1, relief="solid", width=width_, height=height_)
            self.left_phone_book.pack(side="left", expand=True, fill="both")
        if self.left_phone_book != None:
            left_phone_book_header = tk.Label(self.left_phone_book, text="Phone Book", font=("Arial", 18))
            left_phone_book_header.pack(fill="x")

        # Create input fields for name and number
        name_label = tk.Label( self.left_phone_book, text="Name:", font=("Helvetica", 14))
        name_label.pack(side="top", pady=10)
        name_entry = tk.Entry( self.left_phone_book, font=("Helvetica", 14))
        name_entry.pack(side="top", pady=10)

        number_label = tk.Label( self.left_phone_book, text="Number:", font=("Helvetica", 14))
        number_label.pack(side="top", pady=10)
        number_entry = tk.Entry( self.left_phone_book, font=("Helvetica", 14))
        number_entry.pack(side="top", pady=10)



        # Create buttons for adding and deleting contacts
        add_button = tk.Button( self.left_phone_book, text="Add Contact", command=lambda: add_contact(name_entry, number_entry, self.contacts_list), font=("Helvetica", 14))
        add_button.pack(side="top", pady=10)

    def create_right_frame(self):
        # Create sender and receiver frames
        width_ = self.content_frame.winfo_width() / 2 - 20;
        height_ = self.content_frame.winfo_height() / 2 - 10;

        right_panel_bg = "#d5e8f7"
        font=("Comic Sans MS", 12, "bold")
        fg = "#fc6603"
        light_black = "#383532"

        if self.right_phone_book == None:
            self.right_phone_book = tk.Frame(self.content_frame, bg=right_panel_bg, borderwidth=1, relief="solid", width=width_, height=height_)
            self.right_phone_book.pack(side="left", expand=True, fill="both")
        if self.right_phone_book != None:
            right_phone_book_header = tk.Label(self.right_phone_book, text="Phone Book", font=("Arial", 18))
            right_phone_book_header.pack(fill="x")

        # Create a Listbox to display contacts
        if self.contacts_list == None:
            self.contacts_list = tk.Listbox(self.right_phone_book, selectmode=tk.MULTIPLE, width=40, font=("Helvetica", 14), bd=0, relief="flat", highlightthickness=1, highlightbackground="#ccc", highlightcolor="#ccc")
            self.contacts_list.pack(side="top", pady=10)
            display_contacts(self.contacts_list)

        # Style for the Delete Contact button
        delete_button_style = ttk.Style()
        delete_button_style.configure("DeleteButton.TButton", foreground="red", background="#fff", font=("Helvetica", 14), relief="flat", padx=15, pady=8)

        delete_button = ttk.Button(self.right_phone_book, text="Delete Contact", command=lambda: delete_contact(self.contacts_list), style="DeleteButton.TButton")
        delete_button.pack(side="top", pady=10)




    def create_both_frames(self):
        self.create_left_frame()
        self.create_right_frame()