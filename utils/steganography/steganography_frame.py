import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

from .utils import LSBSteganography, generate_random_string, extract_filename_and_extension, get_wireless_ipv4, get_all_contacts

class SteganographyPannel:
    def __init__(self, content_frame):
        self.content_frame = content_frame
        self.steganography_panel = None
        self.steganography_extraction_panel = None
        self.steganography_image_path = ""
        self.directory_path = ""
        self.selected_contact = None
    
    def select_directory(self):
        self.directory_path = filedialog.askdirectory()
        self.directory_label.config(text=f"Directory: {self.directory_path}")

    def create_stego_image(self):
        lsb_stego = LSBSteganography(image_path=self.steganography_image_path)
        text = self.text_entry.get("1.0", "end-1c")
        # private_key = self.ip_address_entry.get("1.0", "end-1c")
        contacts = get_all_contacts()
        print(contacts)
        private_key = str(contacts[self.selected_contact.get()])
        lsb_stego.hide_text(text_to_hide=text, private_key=private_key)
        file_name, extension = extract_filename_and_extension(self.steganography_image_path)
        output_path = self.directory_path + "/" + generate_random_string(size=6) + "-" + file_name + extension
        lsb_stego.save_stego_image(output_path=output_path)

    def show_sereat_message(self):
        lsb_stego = LSBSteganography(image_path=self.steganography_image_path)

        ip_address = get_wireless_ipv4()
        print(ip_address)
        if len(ip_address)==2:
            private_key = ip_address[1]

        message = lsb_stego.extract_text(private_key=str(private_key))

        # Clear existing text
        self.secreat_text_entry.delete("1.0", tk.END)
        # Insert new text
        self.secreat_text_entry.insert(tk.END, message)


    def open_image(self, image_label):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.steganography_image_path = file_path
            image = Image.open(file_path)
            img_width, img_height = image.size
            
            # Calculate new dimensions while maintaining aspect ratio
            new_width = 200
            aspect_ratio = img_width / img_height
            new_height = int(new_width / aspect_ratio)
            
            # Resize the image
            image_resized = image.resize((new_width, new_height))
            
            photo = ImageTk.PhotoImage(image_resized)
            image_label.config(image=photo)
            image_label.config(width=new_width, height=new_height)
            image_label.image = photo  # to prevent garbage collection

    def build_steganography_panel(self):
        # Create sender and receiver frames
        width_ = self.content_frame.winfo_width() / 2 - 20;
        height_ = self.content_frame.winfo_height() / 2 - 10;

        left_panel_bg = "#c1dbcf"
        font=("Comic Sans MS", 12, "bold")
        fg = "#fc6603"
        light_black = "#383532"

        if self.steganography_panel == None:
            self.steganography_panel = tk.Frame(self.content_frame, bg=left_panel_bg, borderwidth=1, relief="solid", width=width_, height=height_)
            self.steganography_panel.pack(side="left", expand=True, fill="both")
        if self.steganography_panel != None:
            steganography_header = tk.Label(self.steganography_panel, text="Steganography", font=("Arial", 18))
            steganography_header.pack(fill="x")


        directory = tk.Button(self.steganography_panel, text="Select Directory", bg=left_panel_bg, fg="#1c1a1a", font=font, command=self.select_directory)
        directory.pack(side="top", pady=(10, 10))

        self.directory_label = tk.Label(self.steganography_panel, text="Directory: ", font=font, bg=left_panel_bg)
        self.directory_label.pack(side="top")

        # - Image Label and Open Image
        # Create a label to display the image
        image_label = tk.Label(self.steganography_panel, bg="lightgray", bd=2, relief=tk.RIDGE)
        image_label.pack(padx=10, pady=10)

        # Create a button to open the file dialog
        open_button = tk.Button(self.steganography_panel, text="Open Image", bg=left_panel_bg, font=font, fg=light_black, command=lambda: self.open_image(image_label))
        open_button.pack()

        # - Creating contact menu to select corresponding IP
        contacts = get_all_contacts()
        # Create a StringVar to hold the selected contact name
        self.selected_contact = tk.StringVar()
        self.selected_contact.set("Select Contact")
        # Create a dropdown list (OptionMenu) with the keys of the contacts dictionary
        contact_dropdown = tk.OptionMenu(self.steganography_panel, self.selected_contact, *contacts.keys())
        contact_dropdown.pack(side="top", pady=10)
        contact_dropdown.config(bg=left_panel_bg, fg=fg, bd=1, relief="solid", font=font)

        # - Stego Image Text

        # Create a frame to contain the label and entry widgets
        text_frame = tk.Frame(self.steganography_panel, bg=left_panel_bg)
        text_frame.pack(side="top", pady=(10, 10))



        # Create a label for IP address
        # ip_label = tk.Label(text_frame, text="Enter Receiver IP address:", bg=left_panel_bg, fg=fg, font=font)
        # ip_label.pack(side="top", padx=(10, 5))

        # Create an entry widget for IP address
        # self.ip_address_entry = tk.Text(text_frame, width=50, height=2, bg=left_panel_bg, fg=light_black, font=font)
        # self.ip_address_entry.pack(side="top", pady=(5, 10))

        text_label = tk.Label(text_frame, text="Enter Message:", bg=left_panel_bg, fg=fg, font=font)
        text_label.pack(side="top", padx=(10, 5))
        self.text_entry = tk.Text(text_frame, width=50, height=5, bg=left_panel_bg, fg=light_black, font=font)
        self.text_entry.pack(side="left", padx=(5, 10))


        # - Create Stego Image Button
        send_button = tk.Button(self.steganography_panel, text="Create Stego Image", bg=left_panel_bg, font=font, fg="green", command=self.create_stego_image)
        send_button.pack(side="top")

    def build_steganography_extraction_panel(self):
        # Create sender and receiver frames
        width_ = self.content_frame.winfo_width() / 2 - 20;
        height_ = self.content_frame.winfo_height() / 2 - 10;

        right_panel_bg = "#d5e8f7"
        font=("Comic Sans MS", 12, "bold")
        fg = "#fc6603"
        light_black = "#383532"

        if self.steganography_extraction_panel == None:
            self.steganography_extraction_panel = tk.Frame(self.content_frame, bg=right_panel_bg, borderwidth=1, relief="solid", width=width_, height=height_)
            self.steganography_extraction_panel.pack(side="left", expand=True, fill="both")
        if self.steganography_extraction_panel != None:
            steganography_extraction_header = tk.Label(self.steganography_extraction_panel, text="Steganography Extraction", font=("Arial", 18))
            steganography_extraction_header.pack(fill="x")

        # - Image Label and Open Image
        # Create a label to display the image
        image_label = tk.Label(self.steganography_extraction_panel, bg="lightgray", bd=2, relief=tk.RIDGE)
        image_label.pack(padx=10, pady=10)

        # Create a button to open the file dialog
        open_button = tk.Button(self.steganography_extraction_panel, text="Open Image", bg=right_panel_bg, font=font, fg="black", command=lambda: self.open_image(image_label))
        open_button.pack(side="top", pady=10)

        # - Send Button
        show_message = tk.Button(self.steganography_extraction_panel, text="Show Message", bg=right_panel_bg, font=font, fg="green", command=self.show_sereat_message)
        show_message.pack(side="top")

        # - Screate Message

        # Create an entry widget for IP address
        self.secreat_text_entry = tk.Text(self.steganography_extraction_panel, border=2, width=70, height=10, bg=right_panel_bg, fg="#fff", font=font, wrap=tk.WORD)
        self.secreat_text_entry.pack(side="top", pady=10)

    def stegganography_page(self):
        self.build_steganography_panel()
        self.build_steganography_extraction_panel()

    

