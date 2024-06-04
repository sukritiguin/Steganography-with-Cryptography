import tkinter as tk
import socket
import os
from tkinter import filedialog
from PIL import Image, ImageTk
import threading

from .utils import AnimatedGifLabel, get_all_contacts


class SocketCommunicationPanel:
    def __init__(self, content_frame):
        self.content_frame = content_frame
        self.sender_frame = None
        self.receiver_frame = None
        self.sender_image_path = ""
        self.receiver_directory_path = ""
        self.path_label = None
        self.success_message = None
        self.error_message = None
        self.listening = None

    def select_directory(self):
        self.receiver_directory_path = filedialog.askdirectory()
        
    
    def check_listing(self):
        if self.listeing_checkbox_var.get() == False:
            self.listening.config_image("./utils/socketio/stop.gif")
            self.listening_checkbox.config(text="Listen")
        else:
            self.listening.config_image("./utils/socketio/giphy.gif")
            self.listening_checkbox.config(text="Stop Listening")
            # Start a new thread for receiving files
            threading.Thread(target=self.receive_file).start()


    def send_file(self):
        # Get the IP address and port from the entry fields
        # ip_address = self.ip_address_entry.get()
        contacts = get_all_contacts()
        ip_address = str(contacts[self.selected_contact.get()])
        try:
            # port = int(self.port_entry.get())
            port = 12345
        except:
            port = 0
        
        # Create a socket object
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        try:
            # Connect to the receiver
            s.connect((ip_address, port))
            
            # Send the file name and size
            filename = os.path.basename(self.sender_image_path)
            filesize = os.path.getsize(self.sender_image_path)
            s.send(f"{filename}::{filesize}".encode())
            
            # Send the file data
            with open(self.sender_image_path, "rb") as f:
                data = f.read(1024)
                while data:
                    s.send(data)
                    data = f.read(1024)
            if self.success_message:
                self.success_message.config(text="File sent successfully!")
            else:
                self.success_message = tk.Label(self.sender_frame, text="File sent successfully!", bg="green", fg="black", font=("Comic Sans MS", 12, "bold"))
                self.success_message.pack(side="top", pady=(10, 5))
            print("File sent successfully!")
        except Exception as e:
            if self.error_message:
                self.error_message.config(text="Something went wrong!")
            else:
                self.error_message = tk.Label(self.sender_frame, text="Something Went Wrong!", bg="red", fg="black", font=("Comic Sans MS", 12, "bold"))
                self.error_message.pack(side="top", pady=(10, 5))
            print(f"Error: {e}")
        finally:
            s.close()


    def receive_file(self):
        # Create a TCP/IP socket
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Bind the socket to the address and port
        server_address = ('', 12345)  # Update with your desired address and port
        server.bind(server_address)

        # Listen for incoming connections
        server.listen(1)

        print("Waiting for incoming connection...")

        # Accept incoming connection
        conn, addr = server.accept()
        print(f"Connection established with {addr}")

        # Receive file info (assuming it's a string)
        file_info = conn.recv(1024).decode()
        print("Received file info:", file_info)
        file_name = file_info.split("::")[0]

        # Receive the file data and write it to a file
        save_file_name = self.receiver_directory_path + "/" + file_name
        with open(save_file_name, "wb") as f:  # Update with your desired file name and extension
            while True:
                chunk = conn.recv(1024)
                if not chunk:
                    break
                f.write(chunk)
        label = tk.Label(text=f"{file_name} received", master=self.receiver_frame)
        label.pack(side="top", pady=10)
        print("File received successfully")


        # Close the connection
        conn.close()

        self.listening.config_image("./utils/socketio/stop.gif")
        self.listening_checkbox.config(text="Listen")
        self.listeing_checkbox_var.set(False)



    def open_image(self, image_label):
        if self.success_message:
            self.success_message.config(text="")
        if self.error_message:
            self.error_message.config(text="")
        file_path = filedialog.askopenfilename()
        if file_path:
            self.sender_image_path = file_path
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

    def build_sender_panel(self):
        # Create sender and receiver frames
        width_ = self.content_frame.winfo_width() / 2 - 20;
        height_ = self.content_frame.winfo_height() / 2 - 10;

        left_panel_bg = "#c1dbcf"
        font=("Comic Sans MS", 12, "bold")
        fg = "#fc6603"
        light_black = "#383532"

        if self.sender_frame == None:
            self.sender_frame = tk.Frame(self.content_frame, bg=left_panel_bg, borderwidth=1, relief="solid", width=width_, height=height_)
            self.sender_frame.pack(side="left", expand=True, fill="both")
        if self.sender_frame != None:
            sender_header = tk.Label(self.sender_frame, text="Sender", font=("Arial", 18))
            sender_header.pack(fill="x")

            # - Image Label and Open Image
            # Create a label to display the image
            image_label = tk.Label(self.sender_frame, bg="lightgray", bd=2, relief=tk.RIDGE)
            image_label.pack(padx=10, pady=10)

            # Create a button to open the file dialog
            open_button = tk.Button(self.sender_frame, text="Open Image", bg=left_panel_bg, font=font, fg=light_black, command=lambda: self.open_image(image_label))
            open_button.pack()

            # - IP Address Frame
            contacts = get_all_contacts()
            # Create a StringVar to hold the selected contact name
            self.selected_contact = tk.StringVar()
            self.selected_contact.set("Select Contact")
            # Create a dropdown list (OptionMenu) with the keys of the contacts dictionary
            contact_dropdown = tk.OptionMenu(self.sender_frame, self.selected_contact, *contacts.keys())
            contact_dropdown.pack(side="top", pady=10)
            contact_dropdown.config(bg=left_panel_bg, fg=fg, bd=1, relief="solid", font=font)

            # Create a frame to contain the label and entry widgets
            ip_frame = tk.Frame(self.sender_frame, bg=left_panel_bg)
            ip_frame.pack(side="top", pady=(10, 10))

            # Create a label for IP address
            # ip_label = tk.Label(ip_frame, text="Enter IP Address:", bg=left_panel_bg, fg=fg, font=font)
            # ip_label.pack(side="left", padx=(10, 5))

            # Create an entry widget for IP address
            # self.ip_address_entry = tk.Entry(ip_frame, width=30, bg=left_panel_bg, fg=light_black, font=font)
            # self.ip_address_entry.pack(side="left", padx=(5, 10))

            # - Port Frame
            # Create a frame to contain the label and entry widgets
            # port_frame = tk.Frame(self.sender_frame, bg=left_panel_bg)
            # port_frame.pack(side="top", pady=(10, 10))

            # Create a label for Port Number
            # port_label = tk.Label(port_frame, text="Enter Port Number:", bg=left_panel_bg, fg=fg, font=font)
            # port_label.pack(side="left", padx=(10, 5))

            # Create an entry widget for IP address
            # self.port_entry = tk.Entry(port_frame, width=30, bg=left_panel_bg, fg=light_black, font=font)
            # self.port_entry.pack(side="left", padx=(5, 10))

            # - Send Button
            send_button = tk.Button(self.sender_frame, text="Send", bg=left_panel_bg, font=font, fg="green", command=self.send_file)
            send_button.pack(side="top")

    def build_receiver_panel(self):

        # Create sender and receiver frames
        width_ = self.content_frame.winfo_width() / 2 - 20;
        height_ = self.content_frame.winfo_height() / 2 - 10;

        right_panel_bg = "#d5e8f7"
        font=("Comic Sans MS", 12, "bold")
        fg = "#fc6603"
        light_black = "#383532"
        
        self.receiver_frame = tk.Frame(self.content_frame, bg=right_panel_bg, borderwidth=1, relief="solid", width=width_, height=height_)
        self.receiver_frame.pack(side="right", expand=True, fill="both")


        receiver_header = tk.Label(self.receiver_frame, text="Receiver", font=("Arial", 18))
        receiver_header.pack(fill="x")

        # Create a label for Port Number
        directory = tk.Button(self.receiver_frame, text="Select Directory", bg=right_panel_bg, fg="black", font=font, command=self.select_directory)
        directory.pack(side="top", pady=(10, 10))

        # Create a Tkinter variable to store the checkbox state
        self.listeing_checkbox_var = tk.BooleanVar()

        # Create the checkbox widget
        self.listening_checkbox = tk.Checkbutton(self.receiver_frame, text="Listen", variable=self.listeing_checkbox_var, command=self.check_listing, bg=right_panel_bg, fg="black", font=font)

        # Place the checkbox widget in the window
        self.listening_checkbox.pack(side="top", pady=10)


        gif_path = "./utils/socketio/stop.gif"
        self.listening = AnimatedGifLabel(self.receiver_frame, gif_path, size=(150,150))
        self.listening.pack(side="top", pady=(10,10))

        self.listening.animate()




    def socket_communication_page(self):
        self.build_sender_panel()
        self.build_receiver_panel()
