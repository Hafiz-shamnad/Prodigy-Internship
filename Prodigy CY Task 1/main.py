import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
import hashlib
from PIL import Image, ImageTk

# Caesar Cipher Functions
def caesar_cipher_encrypt(text, shift):
    encrypted_text = ""
    for char in text:
        if char.isalpha():
            shift_amount = 65 if char.isupper() else 97
            encrypted_text += chr((ord(char) + shift - shift_amount) % 26 + shift_amount)
        else:
            encrypted_text += char
    return encrypted_text

def caesar_cipher_decrypt(text, shift):
    return caesar_cipher_encrypt(text, -shift)

# Hashing Functions
def md5_hash(text):
    return hashlib.md5(text.encode()).hexdigest()

def sha256_hash(text):
    return hashlib.sha256(text.encode()).hexdigest()

def load_file():
    file_path = filedialog.askopenfilename()
    if file_path:
        with open(file_path, 'r') as file:
            file_content.set(file.read())
            selected_file.set(file_path)

def save_file(text):
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
    if file_path:
        with open(file_path, 'w') as file:
            file.write(text)
        messagebox.showinfo("Success", "File saved successfully")

def encrypt_file():
    encryption_method = encryption_option.get()
    text = file_content.get()

    if encryption_method == "Caesar Cipher":
        try:
            shift = int(shift_key.get())
            encrypted_text = caesar_cipher_encrypt(text, shift)
        except ValueError:
            messagebox.showerror("Invalid Input", "Shift key must be an integer")
            return
    elif encryption_method == "MD5":
        encrypted_text = md5_hash(text)
    elif encryption_method == "SHA-256":
        encrypted_text = sha256_hash(text)
    else:
        messagebox.showerror("Invalid Input", "Unknown encryption method")
        return

    save_file(encrypted_text)

def decrypt_file():
    encryption_method = encryption_option.get()
    text = file_content.get()

    if encryption_method == "Caesar Cipher":
        try:
            shift = int(shift_key.get())
            decrypted_text = caesar_cipher_decrypt(text, shift)
        except ValueError:
            messagebox.showerror("Invalid Input", "Shift key must be an integer")
            return
    else:
        messagebox.showerror("Invalid Operation", "Decryption is only supported for Caesar Cipher")
        return

    save_file(decrypted_text)


# Setting up the main window
root = tk.Tk()
root.title("EncFile - The secure file storage")
root.geometry("500x300")
root.resizable(True, True)  # Allow the window to be resizable

# Load the icon file using PIL
icon_image = Image.open("/Prodigy CY Task 1/app_icon.ico")

# Convert the PIL image to a Tkinter-compatible format
icon = ImageTk.PhotoImage(icon_image)

# Set the window icon
root.iconphoto(True, icon)

# Applying a custom theme
style = ttk.Style()
style.theme_use('clam')  # Use 'clam', 'alt', 'default', or 'classic'

# Configure styles for various elements
style.configure('TLabel', background='#F0F0F0', foreground='#333333')  # Background and foreground colors for labels
style.configure('TFrame', background='#F0F0F0')  # Background color for frames
style.configure('TButton', background='#4CAF50', foreground='white')  # Background and foreground colors for buttons
style.configure('TEntry', fieldbackground='#FFFFFF')  # Background color for entry fields
style.configure('TCombobox', fieldbackground='#FFFFFF')  # Background color for combo boxes
style.configure('TMenubutton', background='#4CAF50', foreground='white')  # Background and foreground colors for menu buttons

# Variables to store file content and file path
file_content = tk.StringVar()
selected_file = tk.StringVar()
shift_key = tk.StringVar()
encryption_option = tk.StringVar(value="Caesar Cipher")

# Main frame
main_frame = ttk.Frame(root, padding="10 10 10 10")
main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

# Adjust column and row weights
root.grid_columnconfigure(0, weight=1)
root.grid_rowconfigure(0, weight=1)
main_frame.grid_columnconfigure(0, weight=1)
main_frame.grid_columnconfigure(1, weight=1)
main_frame.grid_rowconfigure(0, weight=1)
main_frame.grid_rowconfigure(1, weight=1)
main_frame.grid_rowconfigure(2, weight=1)
main_frame.grid_rowconfigure(3, weight=1)

# File frame
file_frame = ttk.LabelFrame(main_frame, text="File", padding="10 10 10 10")
file_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
file_frame.grid_columnconfigure(0, weight=1)
file_frame.grid_columnconfigure(1, weight=1)
file_frame.grid_columnconfigure(2, weight=1)

ttk.Label(file_frame, text="Selected File:").grid(row=0, column=0, sticky=tk.W)
ttk.Entry(file_frame, textvariable=selected_file, state='readonly').grid(row=0, column=1, padx=5, sticky=(tk.W, tk.E))
ttk.Button(file_frame, text="Load File", command=load_file).grid(row=0, column=2, padx=5, sticky=tk.E)

# Options frame
options_frame = ttk.LabelFrame(main_frame, text="Options", padding="10 10 10 10")
options_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
options_frame.grid_columnconfigure(0, weight=1)
options_frame.grid_columnconfigure(1, weight=1)

ttk.Label(options_frame, text="Encryption Method:").grid(row=0, column=0, sticky=tk.W)
method_menu = ttk.OptionMenu(options_frame, encryption_option, "Caesar Cipher", "MD5", "SHA-256")
method_menu.grid(row=0, column=1, padx=5, pady=10, sticky=(tk.W, tk.E))

ttk.Label(options_frame, text="Shift Key (for Caesar Cipher):").grid(row=1, column=0, sticky=tk.W)
ttk.Entry(options_frame, textvariable=shift_key).grid(row=1, column=1, padx=5, sticky=(tk.W, tk.E))

# Buttons
ttk.Button(main_frame, text="Encrypt File", command=encrypt_file).grid(row=2, column=0, padx=5, pady=10, sticky=tk.E)
ttk.Button(main_frame, text="Decrypt File", command=decrypt_file).grid(row=2, column=1, padx=5, pady=10, sticky=tk.W)

# Running the Tkinter event loop
root.mainloop()
