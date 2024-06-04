import tkinter as tk
from ..socketio.socket_communication_frame import SocketCommunicationPanel
from ..steganography.steganography_frame import SteganographyPannel
from ..home.phoneBook import PhoneBookPanel
from ..summary.summary_frame import SummaryPage
from ..documentation.documentation_frame import DocumentationPage

def navigate_to(page_name, content_frame):
    # Placeholder function for navigation
    print(f"Navigate to {page_name}")
    # Clear existing content
    clear_content(content_frame)
    # Display content based on page name
    if page_name == "Home":
        phonebook_panel = PhoneBookPanel(content_frame)
        phonebook_panel.create_both_frames()
    elif page_name == "Image Steganography":
        steganography_panel = SteganographyPannel(content_frame)
        steganography_panel.stegganography_page()
    elif page_name == "Socket Communication":
        socket_commmunication = SocketCommunicationPanel(content_frame)
        socket_commmunication.socket_communication_page()
    elif page_name == "Documentation":
        documentation_page = DocumentationPage(content_frame)
    elif page_name == "Summary":
        summary_page = SummaryPage(content_frame)

def clear_content(content_frame):
    # Clear existing content
    for widget in content_frame.winfo_children():
        widget.destroy()

def home_page(content_frame):
    # Display Home page content
    label = tk.Label(content_frame, text="Welcome to Home Page", font=("Arial", 18), bg="#34eb80")
    label.pack()

def image_steganography_page(content_frame):
    # Display Image Steganography page content
    label = tk.Label(content_frame, text="Image Steganography Content", font=("Arial", 18), bg="#34eb80")
    label.pack()



def documentation_page(content_frame):
    # Display Documentation page content
    label = tk.Label(content_frame, text="Documentation Content", font=("Arial", 18), bg="#34eb80")
    label.pack()

def about_us_page(content_frame):
    # Display About Us page content
    label = tk.Label(content_frame, text="About Us Content", font=("Arial", 18), bg="#34eb80")
    label.pack()


