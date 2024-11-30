"""TASK 02- IMAGE PIXEL MANIPULATION"""

import os
from tkinter import Tk, Button, Label, Entry, filedialog, messagebox
from PIL import Image
import random



"""Presents a Key to decrypt and encrypt files consistently, function returns a random object that shuffle items"""
def getrandomanseedvalue(seed):
    return random.Random(seed)

"""Function to Encrypt an Image after it has been loaded"""
def encryptimage(inputimagepath, outputimagepath, seed):
    """Encrypts the image by manipulating the image's pixel values."""
    image_to_encrypt = Image.open(inputimagepath)
    width_of_image, height_of_image = image_to_encrypt.size
    # Get pixel data as a list
    pixels_of_image = list(image_to_encrypt.getdata())
    random_generation = getrandomanseedvalue(seed)

    # Create a list of pixel indices
    indices = list(range(len(pixels_of_image)))
    # Shuffle the indices using the seeded random generator
    random_generation.shuffle(indices)

    # Reorder pixels based on shuffled indices
    encrypted_pixels = [pixels_of_image[i] for i in indices]

    # Create new image with the shuffled pixel values
    encrypted_image = Image.new(image_to_encrypt.mode, (width_of_image, height_of_image))
    # Apply encrypted pixels to the new image
    encrypted_image.putdata(encrypted_pixels)
    # Save the encrypted image
    encrypted_image.save(outputimagepath)
    return True

"Function to decrypt the images, reversing the encryption process"
def decrypt_image(inputimagepath, outputimagepath, seed):
    """Decrypts the image by reversing the encryption process."""
    image_to_decrypt = Image.open(inputimagepath)
    width, height = image_to_decrypt.size
    # Get encrypted pixel data 
    encrypted_pixels = list(image_to_decrypt.getdata())
    random_generation = getrandomanseedvalue(seed)

    # Create a new list to hold the original state of pixel indices 
    indices = list(range(len(encrypted_pixels)))
    # Shuffle the indices again to get the original state
    random_generation.shuffle(indices)

    # Create a new image to hold the decrypted data
    decrypted_pixels = [None] * len(encrypted_pixels)

    # Restore original pixels using the shuffled indices
    for original_index, shuffled_index in enumerate(indices):
        decrypted_pixels[shuffled_index] = encrypted_pixels[original_index]

    # Save the decrypted image
    decrypted_image = Image.new(image_to_decrypt.mode, (width, height))
    decrypted_image.putdata(decrypted_pixels)
    decrypted_image.save(outputimagepath)
    return True

"""Helper Functions to Select Images"""
def select_image_as_Input():
    """Opens a file dialog to select an input image."""
    input_image_path = filedialog.askopenfilename(title="Select Image")
    input_image_label.config(text=input_image_path)

def select_image_as_Output():
    """Opens a file dialog to select an output image path."""
    output_image_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"),("JPEG files", "*.jpg;*.jpeg"),("All files", "*.*")], title="Save Encrypted/Decrypted Image")

    output_image_label.config(text=output_image_path)

"""Helper Functions for the encrypt and decrypt buttons"""
def encrypt():
    input_image_path = input_image_label.cget("text")
    output_image_path = output_image_label.cget("text")
    seed = seed_entry.get()

    if not input_image_path or not output_image_path:
        messagebox.showerror("Error", "Please select input and output images.")
        return

    if encryptimage(input_image_path, output_image_path, seed):
        messagebox.showinfo("Success", "Image encrypted successfully!")

def decrypt():
    input_image_path = input_image_label.cget("text")
    output_image_path = output_image_label.cget("text")
    seed = seed_entry.get()

    if not input_image_path or not output_image_path:
        messagebox.showerror("Error", "Please select input and output images.")
        return

    if decrypt_image(input_image_path, output_image_path, seed):
        messagebox.showinfo("Success", "Image decrypted successfully!")




"""Setting up the GUI"""
root = Tk()
root.title("Image Pixel Manipulation For Encryption and Decryption")
root.configure(bg="black")

# Create and place  GUI Elements
Label(root, text="Select Image to Encrypt/Decrypt:").pack(pady=5)
input_image_label = Label(root, text="No image selected")
input_image_label.pack(pady=5)

Button(root, text="Browse Local System", command=select_image_as_Input).pack(pady=5)

Label(root, text="Output Image Path:").pack(pady=5)
output_image_label = Label(root, text="No output path selected")
output_image_label.pack(pady=5)

Button(root, text="Save As", command=select_image_as_Output).pack(pady=5)

Label(root, text="Enter Seed Key:").pack(pady=5)
seed_entry = Entry(root)
seed_entry.pack(pady=5)

Button(root, text="Encrypt Selected Image", command=encrypt).pack(pady=5)
Button(root, text="Decrypt Selected Image", command=decrypt).pack(pady=5)

root.mainloop()