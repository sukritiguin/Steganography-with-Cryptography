import tkinter as tk
from tkinter import messagebox
import sqlite3

def add_contact(name_entry, number_entry, contacts_list):
    name = name_entry.get()
    number = number_entry.get()
    if name and number:
        conn = sqlite3.connect("phonebook.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO contacts (name, number) VALUES (?, ?)", (name, number))
        conn.commit()
        conn.close()
        display_contacts(contacts_list)
        name_entry.delete(0, tk.END)
        number_entry.delete(0, tk.END)
    else:
        messagebox.showwarning("Missing Information", "Please enter both name and number.")

def delete_contact(contacts_list):
    selected_indices = contacts_list.curselection()
    if selected_indices:
        conn = sqlite3.connect("phonebook.db")
        cursor = conn.cursor()
        for index in selected_indices:
            selected_contact = contacts_list.get(index)
            name, number = selected_contact.split(": ")
            cursor.execute("DELETE FROM contacts WHERE name = ? AND number = ?", (name, number))
        conn.commit()
        conn.close()
        display_contacts(contacts_list)
    else:
        messagebox.showwarning("No Selection", "Please select a contact to delete.")


def display_contacts(contacts_list):
    contacts_list.delete(0, tk.END)
    conn = sqlite3.connect("phonebook.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM contacts")
    rows = cursor.fetchall()
    for row in rows:
        contacts_list.insert(tk.END, f"{row[0]}: {row[1]}")
    conn.close()