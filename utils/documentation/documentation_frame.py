import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import fitz


class DocumentationPage:
    def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(master, bg="white")
        self.frame.pack(fill="both", expand=True)
        self.frame.focus_set()  # Ensure the frame has focus

        self.canvas = tk.Canvas(self.frame, bg="white")
        self.scrollbar = ttk.Scrollbar(self.frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        self.current_page = 0
        self.images = []

        self.photo_frame = tk.Label(self.scrollable_frame, bg="white")
        self.photo_frame.pack(pady=10)

        self.create_widgets()
        self.bind_events()

    def create_widgets(self):
        header_label = tk.Label(self.scrollable_frame, text="Documentation", font=("Arial", 18, "bold"), bg="white")
        header_label.pack(pady=10)

        self.load_pdf()

    def bind_events(self):
        self.frame.bind("<Left>", lambda event: self.prev_page())
        self.frame.bind("<Right>", lambda event: self.next_page())

    def load_pdf(self):
        file_path = "D://Image Steganography and Encryption//000-Application-Desktop//group21_doc.pdf"
        if file_path:
            self.images = self.extract_images_from_pdf(file_path)
            if self.images:
                self.show_current_page()

    def extract_images_from_pdf(self, file_path):
        images = []
        try:
            document = fitz.open(file_path)
            for page_number in range(document.page_count):
                page = document.load_page(page_number)
                pix = page.get_pixmap()
                image = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                images.append(image)
        except Exception as e:
            print("Error:", e)
        return images

    def show_current_page(self):
        if self.images:
            image = self.images[self.current_page]
            photo = ImageTk.PhotoImage(image)
            self.photo_frame.config(image=photo)
            self.photo_frame.image = photo

    def prev_page(self):
        print("Previous button clicked", self.current_page)
        if self.current_page > 0:
            self.current_page -= 1
            self.show_current_page()

    def next_page(self):
        print("Next button clicked", self.current_page)
        if self.current_page < len(self.images) - 1:
            self.current_page += 1
            self.show_current_page()