import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from pdf2image import convert_from_path

class PDFViewer:
    def __init__(self, master, pdf_path):
        self.master = master
        self.pdf_path = pdf_path
        
        self.page_index = 0
        self.images = self.get_images()
        self.total_pages = len(self.images)
        
        self.canvas = tk.Canvas(master)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.scrollbar = ttk.Scrollbar(master, orient=tk.VERTICAL, command=self.canvas.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.bind("<Configure>", self.on_canvas_configure)
        self.canvas.bind("<MouseWheel>", self.on_mousewheel)
        self.master.bind("<Left>", self.show_prev_page)
        self.master.bind("<Right>", self.show_next_page)
        
        # Call show_page after the canvas has been fully initialized
        self.master.after(100, self.show_page)

        
    def get_images(self):
        return convert_from_path(self.pdf_path, fmt='png')

    def show_page(self):
        self.canvas.delete("all")
        image = self.images[self.page_index]

        # Get the dimensions of the canvas
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()

        # Calculate the aspect ratio of the image and canvas
        image_ratio = image.width / image.height
        canvas_ratio = canvas_width / canvas_height

        # Resize the image to fit within the canvas while maintaining aspect ratio
        if image_ratio > canvas_ratio:
            # Image is wider than the canvas
            new_width = canvas_width
            new_height = int(canvas_width / image_ratio)
        else:
            # Image is taller than or equal to the canvas
            new_width = int(canvas_height * image_ratio)
            new_height = canvas_height

        resized_image = image.resize((new_width, new_height))
        photo = ImageTk.PhotoImage(resized_image)

        # Calculate the position to center the image on the canvas
        x_offset = (canvas_width - new_width) / 2
        y_offset = (canvas_height - new_height) / 2

        # Set the canvas scroll region to encompass the entire image
        self.canvas.config(scrollregion=(0, 0, canvas_width, new_height))

        self.canvas.create_image(x_offset, 0, anchor=tk.NW, image=photo)
        self.canvas.image = photo


    def on_canvas_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        
    def on_mousewheel(self, event):
        self.canvas.yview_scroll(-1*(event.delta//120), "units")
        
    def show_prev_page(self, event):
        if self.page_index > 0:
            self.page_index -= 1
            self.show_page()
        
    def show_next_page(self, event):
        if self.page_index < self.total_pages - 1:
            self.page_index += 1
            self.show_page()
        

root = tk.Tk()
root.title("PDF Viewer")
pdf_viewer = PDFViewer(root, r"D:\Image Steganography and Encryption\000-Application-Desktop\group21_doc.pdf")
root.mainloop()
