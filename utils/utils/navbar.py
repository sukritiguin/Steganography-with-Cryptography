import tkinter as tk
from .naviagtion import navigate_to

def build_navbar(root, content_frame):

    # List of navigation items
    navbar_items = ["Home", "Image Steganography", "Socket Communication", "Documentation", "Summary"]

    # Create a frame for the navigation bar
    navbar_frame = tk.Frame(root, bg="#c1dbcf")
    navbar_frame.pack(side="top")

    # Create buttons for navigation dynamically
    for item in navbar_items:
        button_width = root.winfo_screenmmwidth() // (len(navbar_items)*2)
        button = tk.Button(navbar_frame, text=item,bg="#a9afb8", command=lambda item=item: navigate_to(item, content_frame), width=button_width, height=2)
        button.pack(side="left")