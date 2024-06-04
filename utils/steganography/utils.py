# Step 1: Import necessary libraries
from PIL import Image
import random
import string
import os

# Encryption Algorithm
import base64
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
import subprocess
import re

import sqlite3

def get_all_contacts():
    conn = sqlite3.connect("phonebook.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM contacts")
    rows = cursor.fetchall()
    conn.close()
    
    contacts_dict = {}
    for row in rows:
        contacts_dict[row[0]] = row[1]
    
    return contacts_dict

def get_wireless_ipv4():
    # Run the ipconfig command
    result = subprocess.run(['ipconfig'], capture_output=True, text=True)

    # Extract IPv4 addresses from the output
    matches = []
    if result.returncode == 0:
        output = result.stdout
        # Use regular expression to find the IPv4 addresses
        matches = re.findall(r"IPv4 Address[.\s]+: ([0-9]+(?:\.[0-9]+){3})", output)
    return matches


def encrypt_text(plaintext, private_key):
    # Key expansion
    key = PBKDF2(private_key.encode('utf-8'), b'salt', 32)  # 256-bit key for AES-256

    # Padding
    padding_length = AES.block_size - (len(plaintext) % AES.block_size)
    padded_plaintext = plaintext.encode('utf-8') + bytes([padding_length]) * padding_length

    # Encryption
    cipher = AES.new(key, AES.MODE_ECB)  # Using ECB mode for simplicity, use CBC or CTR for better security
    ciphertext = cipher.encrypt(padded_plaintext)

    return ciphertext

def decrypt_text(ciphertext, private_key):
    # Key expansion
    key = PBKDF2(private_key.encode('utf-8'), b'salt', 32)

    # Decryption
    cipher = AES.new(key, AES.MODE_ECB)
    decrypted_padded_plaintext = cipher.decrypt(ciphertext)

    # Padding removal
    padding_length = decrypted_padded_plaintext[-1]
    plaintext = decrypted_padded_plaintext[:-padding_length]

    return plaintext.decode('utf-8')

# ======================

def extract_filename_and_extension(image_path):
    filename_with_extension = os.path.basename(image_path)
    filename, extension = os.path.splitext(filename_with_extension)
    return filename, extension

def generate_random_string(size=6):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(size))

# Step 2: Define the LSBSteganography class
class LSBSteganography:
    def __init__(self, image_path):
        self.image_path = image_path
        self.image = Image.open(image_path)
        self.width, self.height = self.image.size
        self.text = ""

    def generate_seed(self):
        # Step 3: Generate seed based on the first pixel of the image
        first_pixel = self.image.getpixel((0, 0))
        red_bits = first_pixel[0] & 0b00000111
        green_bits = (first_pixel[1] & 0b00000111) << 3
        blue_bits = (first_pixel[2] & 0b00000011) << 6
        seed = red_bits | green_bits | blue_bits
        return seed

    def put_int_in_pixels(self, pixels, current_char_ascii):
        # Step 4: Put integer value in pixels
        x, y = pixels
        print(self.image.getpixel((x, y)))
        try:
            r, g, b, alpha = self.image.getpixel((x, y))
        except:
            r, g, b = self.image.getpixel((x, y))
        red = format(r, '08b')
        green = format(g, '08b')
        blue = format(b, '08b')
        current_char_ascii_bin_str = format(current_char_ascii, '08b')
        bit_for_red = current_char_ascii_bin_str[0:3]
        bit_for_green = current_char_ascii_bin_str[3:6]
        bit_for_blue = current_char_ascii_bin_str[6:8]
        red = red[0:-3] + bit_for_red
        green = green[0:-3] + bit_for_green
        blue = blue[0:-2] + bit_for_blue
        r, g, b = int(red, 2), int(green, 2), int(blue, 2)
        self.image.putpixel((x, y), (r, g, b))

    def create_shuffled_array(self, seed):
        # Step 5: Create shuffled array for pixel indices
        total_pixels = self.height * self.width
        index_array = list(range(1, total_pixels))
        for i in range(total_pixels - 2, 0, -1):
            random.seed(seed + i)
            pseudo_random_index = random.randint(0, i)
            index_array[i], index_array[pseudo_random_index] = index_array[pseudo_random_index], index_array[i]
        return index_array

    def predict_row_col(self, shuffled_element):
        # Step 6: Predict row and column from shuffled element
        if 0 <= shuffled_element < self.height * self.width:
            row = shuffled_element // self.width
            col = shuffled_element % self.width
            return row, col
        else:
            return None

    def hide_text(self, text_to_hide, private_key="sukriti-default"):
        # Encrypt Text
        encrypted_text = encrypt_text(text_to_hide, private_key)
        encrypted_text_base64 = base64.b64encode(encrypted_text).decode('utf-8')
        text_to_hide = str(encrypted_text_base64)


        # Step 7: Hide text in the image using LSB
        seed_value = self.generate_seed()
        shuffled_array = self.create_shuffled_array(seed_value)
        current_ind = 0
        for shuffled_element in shuffled_array:
            row, col = self.predict_row_col(shuffled_element)
            if current_ind == len(text_to_hide):
                current_char_ascii = 8  # Backspace ASCII
                self.put_int_in_pixels((col, row), current_char_ascii)
            else:
                current_char_ascii = ord(text_to_hide[current_ind])
                self.put_int_in_pixels((col, row), current_char_ascii)
            if current_char_ascii == 8:
                break
            current_ind += 1

    def save_stego_image(self, output_path):
        # Step 8: Save the stego image
        self.image.save(output_path)
        print(f"Stego image saved at: {output_path}")

    def extract_text(self, private_key="sukriti-default"):
        # Step 9: Extract hidden text from the stego image
        seed_value = self.generate_seed()
        shuffled_array = self.create_shuffled_array(seed_value)
        extracted_text = ""
        for shuffled_element in shuffled_array:
            row, col = self.predict_row_col(shuffled_element)
            try:
                r, g, b, alpha = self.image.getpixel((col, row))
            except:
                r, g, b = self.image.getpixel((col, row))
            red = format(r, '08b')
            green = format(g, '08b')
            blue = format(b, '08b')
            data = red[-3:] + green[-3:] + blue[-2:]
            data = int(data, 2)
            if data == 8:
                break
            data = chr(data)
            extracted_text += data
            if data == 8:
                break
        
        private_key = str(private_key)
        print("Private key: " + private_key)
        print("Extracted text: " + extracted_text)
        encrypted_text_base64 = base64.b64decode(extracted_text)
        decrypted_text = decrypt_text(encrypted_text_base64, private_key)
        extracted_text = decrypted_text
        return extracted_text