import tkinter as tk

from utils.utils.navbar import build_navbar

root = tk.Tk()
root.title("Secure Image Steganography")

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

root.geometry(f"{screen_width}x{screen_height}")
root.configure(bg="#c1dbcf")

# root.resizable(False, False)

# - Creating Navbar

# List of navigation items
navbar_items = ["Home", "Image Steganography", "Socket Communication", "Documentation", "Summary"]

# Create a frame for the navigation bar
navbar_frame = tk.Frame(root, bg="#c1dbcf")
navbar_frame.pack(expand=0)

# Create a frame for the content
content_frame = tk.Frame(root, bg="#c1dbcf")

# Function to create a heading label
def create_heading(text):
    heading_label = tk.Label(content_frame, text=text, font=("Helvetica", 24, "bold"), bg="#c1dbcf", fg="#38199e")
    heading_label.pack(pady=20)

def create_label(text, foreground="black"):
    label = tk.Label(content_frame, text=text, font=("Helvetica", 18, "bold"), bg="#c1dbcf", fg=foreground)
    label.pack(pady=8)

build_navbar(root, content_frame)


content_frame.pack(expand=1, fill="both")

# Create heading
create_heading("Secure Data Transmission using Steganography")
create_label("Bachelor of Technology")
create_label("In")
create_label("Electronics and Communication Engineering Department")
create_label("of")
create_label("Maulana Abul Kalam Azad University of Technology, West Bengal")
create_label("By")
create_label("ABHISEK BOSE, 10900321060", foreground="#1f0e59")
create_label("BHAVIKA BHATTACHARJEE, 10900320041", foreground="#1f0e59")
create_label("SUKRITI GUIN, 10900320033", foreground="#1f0e59")
create_label("SUYETA CHOWDHURY, 10900320017", foreground="#1f0e59")
create_label("Under the guidance of")
create_label("ATREYEE MAJUMDAR ROY", foreground="#1f0e59")



root.mainloop()
