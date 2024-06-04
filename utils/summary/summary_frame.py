import tkinter as tk
from tkinter import ttk

class SummaryPage:
    def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(master, bg="white")
        self.frame.pack(fill="both", expand=True)

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

        self.create_widgets()

    def create_widgets(self):
        title = tk.Label(self.scrollable_frame, text="Secure LSB Steganography with AES Encryption", font=("Arial", 18, "bold"), bg="white")
        title.pack(pady=10)

        summary = (
            "The 'Secure LSB Steganography with AES Encryption' project is a comprehensive solution "
            "designed to enhance the security of digital communication. In response to the growing prevalence "
            "of cyber threats and data breaches, our project integrates Least Significant Bit (LSB) steganography "
            "with Advanced Encryption Standard (AES) encryption to provide both data concealment and robust protection. "
            "This dual approach ensures that sensitive information is not only hidden but also securely encrypted, mitigating "
            "the risk of unauthorized access and interception."
        )
        summary_label = tk.Label(self.scrollable_frame, text=summary, wraplength=800, justify="left", bg="white", font=("Arial", 12))
        summary_label.pack(pady=10)

        features_label = tk.Label(self.scrollable_frame, text="Key Features and Components", font=("Arial", 16, "bold"), bg="white")
        features_label.pack(pady=10)

        features_frame = tk.Frame(self.scrollable_frame, bg="white")
        features_frame.pack(pady=10)

        features = [
            ("LSB Steganography:", "Data Concealment and Shuffling Algorithm.", 
             "This technique hides sensitive information within the least significant bits of image pixels, making it difficult for unauthorized parties to detect the hidden data. "
             "Enhances security by randomizing pixel access based on a seed derived from the image itself, adding an extra layer of complexity to the data concealment process."),
            
            ("AES Encryption:", "Robust Encryption and Key Management.",
             "Before embedding the data into the image, the information is encrypted using AES, a widely recognized standard known for its strength and reliability. "
             "Efficient key management practices are implemented, including secure generation, storage, and utilization of cryptographic keys derived from the recipient's IP address."),
            
            ("User Interface:", "Developed with Tkinter, Functional Pages.",
             "The application features a user-friendly interface created with Python's Tkinter library, ensuring that the platform is intuitive and accessible for users. "
             "The application includes various functional pages such as home, sending and receiving files, encrypting messages within images, and extracting hidden messages from images."),
            
            ("Network Communication:", "TCP/IP Sockets for secure transmission.",
             "Facilitates the secure transmission of stego images over a network connection, enabling efficient and secure communication between the sender and receiver."),
            
            ("Performance Metrics:", "MSE, PSNR, SSIM, MAE.",
             "Mean Squared Error (MSE) measures the average squared difference between the original and stego images. "
             "Peak Signal-to-Noise Ratio (PSNR) assesses the quality of the stego image. "
             "Structural Similarity Index (SSIM) evaluates the similarity between the original and stego images. "
             "Mean Absolute Error (MAE) indicates the average absolute difference between corresponding pixel values.")
        ]
        for feature in features:
            feature_label = tk.Label(features_frame, text=feature[0], bg="white", font=("Arial", 12, "bold"), anchor="w")
            feature_label.pack(fill="x", padx=20, pady=(5, 0))
            feature_desc_label = tk.Label(features_frame, text=feature[1], bg="white", font=("Arial", 12, "bold"), anchor="w")
            feature_desc_label.pack(fill="x", padx=40, pady=(0, 5))
            feature_details_label = tk.Label(features_frame, text=feature[2], bg="white", font=("Arial", 12), wraplength=800, justify="left")
            feature_details_label.pack(fill="x", padx=60, pady=(0, 5))

        objectives_label = tk.Label(self.scrollable_frame, text="Objectives", font=("Arial", 16, "bold"), bg="white")
        objectives_label.pack(pady=10)

        objectives = (
            "The primary aim of this project is to create a robust and user-friendly platform that provides "
            "a secure environment for digital communication. By addressing the limitations of traditional encryption methods, "
            "our solution ensures the confidentiality and integrity of sensitive information. The integration of LSB steganography "
            "and AES encryption offers a comprehensive approach to data protection, while the shuffling algorithm and efficient key "
            "management practices enhance the overall security of the system."
        )
        objectives_label = tk.Label(self.scrollable_frame, text=objectives, wraplength=800, justify="left", bg="white", font=("Arial", 12))
        objectives_label.pack(pady=10)

        conclusion_label = tk.Label(self.scrollable_frame, text="Conclusion", font=("Arial", 16, "bold"), bg="white")
        conclusion_label.pack(pady=10)

        conclusion = (
            "The 'Secure LSB Steganography with AES Encryption' project is a significant step forward in the "
            "field of information security. By combining advanced techniques for data concealment and encryption, "
            "our solution provides a powerful tool for protecting sensitive information in an increasingly digital and interconnected world. "
            "The user-friendly interface and robust security measures make this platform an effective and accessible solution for individuals and organizations alike."
        )
        conclusion_label = tk.Label(self.scrollable_frame, text=conclusion, wraplength=800, justify="left", bg="white", font=("Arial", 12))
        conclusion_label.pack(pady=10)

        back_button = tk.Button(self.scrollable_frame, text="Back", command=self.go_back, font=("Arial", 12, "bold"), bg="#fc6603", fg="white")
        back_button.pack(pady=20)

    def go_back(self):
        self.master.destroy()
