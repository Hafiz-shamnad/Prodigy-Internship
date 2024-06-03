from tkinter import Tk, Button, Label, filedialog, Frame
from PIL import Image, ImageTk
from ttkthemes import ThemedStyle

# Global variables for storing images
input_image = None
encrypted_image = None
decrypted_image = None

# Function to encrypt image using XOR operation with a key
def encrypt_image(image_path, key):
    global encrypted_image
    # Open the image
    try:
        img = Image.open(image_path)
    except Exception as e:
        print("Error opening image:", e)
        return None

    width, height = img.size

    # Convert image to RGB mode
    img = img.convert("RGB")

    # Resize image to reduce processing time
    try:
        img.thumbnail((width // 10, height // 10))  # Reduce image dimensions for faster processing
    except Exception as e:
        print("Error resizing image:", e)
        return None

    resized_width, resized_height = img.size

    # Encrypt each pixel
    for y in range(resized_height):
        for x in range(resized_width):
            # Get pixel value
            try:
                pixel = img.getpixel((x, y))
            except Exception as e:
                print("Error getting pixel at (", x, ",", y, "):", e)
                continue
            # Encrypt pixel using XOR operation with key
            encrypted_pixel = tuple([(p ^ k) % 256 for p, k in zip(pixel, key)])
            # Update pixel value
            img.putpixel((x, y), encrypted_pixel)

    # Save encrypted image
    encrypted_image = img
    print("Image encrypted successfully!")
    return img

# Function to decrypt image using XOR operation with a key
def decrypt_image(encrypted_img, key):
    global decrypted_image
    if encrypted_img:
        decrypted_img = encrypted_img.copy()
        width, height = decrypted_img.size
        # Decrypt each pixel
        for y in range(height):
            for x in range(width):
                # Get pixel value
                pixel = decrypted_img.getpixel((x, y))
                # Decrypt pixel using XOR operation with key
                decrypted_pixel = tuple([(p ^ k) % 256 for p, k in zip(pixel, key)])
                # Update pixel value
                decrypted_img.putpixel((x, y), decrypted_pixel)
        decrypted_image = decrypted_img
        print("Image decrypted successfully!")
        return decrypted_img
    else:
        print("No encrypted image to decrypt!")
        return None

# Function to save images
def save_images():
    global encrypted_image
    global decrypted_image

    if encrypted_image:
        save_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("All files", "*.*")])
        if save_path:
            try:
                encrypted_image.save(save_path)
                print("Encrypted image saved successfully!")
            except Exception as e:
                print("Error saving encrypted image:", e)
    else:
        print("No encrypted image to save!")

    if decrypted_image:
        save_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("All files", "*.*")])
        if save_path:
            try:
                decrypted_image.save(save_path)
                print("Decrypted image saved successfully!")
            except Exception as e:
                print("Error saving decrypted image:", e)
    else:
        print("No decrypted image to save!")

# Callback function for "Decrypt" button
def decrypt_button_clicked():
    key = (10, 20, 30)  # Example key
    global encrypted_image
    global decrypted_image
    global output_label
    if encrypted_image:
        print("Decrypting image...")
        decrypted_image = decrypt_image(encrypted_image, key)
        if decrypted_image:
            print("Image decrypted.")
            decrypted_image.thumbnail((200, 200))
            decrypted_photo = ImageTk.PhotoImage(decrypted_image)
            output_label.config(image=decrypted_photo)
            output_label.image = decrypted_photo
        else:
            print("Error decrypting image.")
    else:
        print("No encrypted image available!")

# Callback function for "Encrypt" button
def encrypt_button_clicked():
    key = (10, 20, 30)  # Example key
    global input_image
    global encrypted_image
    global output_label
    if input_image:
        print("Encrypting image...")
        encrypted_image = encrypt_image(input_image, key)
        if encrypted_image:
            print("Image encrypted.")
            encrypted_image.thumbnail((200, 200))
            encrypted_photo = ImageTk.PhotoImage(encrypted_image)
            output_label.config(image=encrypted_photo)
            output_label.image = encrypted_photo
        else:
            print("Error encrypting image.")
    else:
        print("No input image selected!")

# Callback function for selecting input image file
def select_input_file():
    global input_image
    file_path = filedialog.askopenfilename()
    if file_path:
        input_image = file_path
        input_image_display = Image.open(file_path)
        input_image_display.thumbnail((200, 200))
        input_photo = ImageTk.PhotoImage(input_image_display)
        input_label.config(image=input_photo)
        input_label.image = input_photo
from tkinter import Tk, Button, Label, filedialog, Frame
from PIL import Image, ImageTk
from ttkthemes import ThemedStyle

# Create UI
root = Tk()
root.title("Image Encryption/Decryption")
root.configure(bg="#f0f0f0")  # Set background color

# Load the icon file using PIL
icon_image = Image.open("/Prodigy CY Task 2/app_icon.ico")

# Convert the PIL image to a Tkinter-compatible format
icon = ImageTk.PhotoImage(icon_image)

# Set the window icon
root.iconphoto(True, icon)

style = ThemedStyle(root)
style.set_theme("arc")  # Choose the theme - you can try different themes

# Create frames
frame_input = Frame(root, bg="#f0f0f0")  # Set background color for frames
frame_input.pack(pady=10)
frame_output = Frame(root, bg="#f0f0f0")
frame_output.pack(pady=10)
frame_buttons = Frame(root, bg="#f0f0f0")
frame_buttons.pack(pady=10)

input_label = Label(frame_input, text="Input Image:", bg="#f0f0f0", fg="#333333", font=("Arial", 12, "bold"))  # Set label colors and font
input_label.pack(side="left", padx=10)
output_label = Label(frame_output, text="Output Image:", bg="#f0f0f0", fg="#333333", font=("Arial", 12, "bold"))
output_label.pack(side="left", padx=10)

select_input_button = Button(frame_buttons, text="Select Input Image", command=select_input_file, bg="#4CAF50", fg="white", font=("Arial", 10, "bold"))  # Set button colors and font
select_input_button.pack(side="left", padx=10)
encrypt_button = Button(frame_buttons, text="Encrypt Image", command=encrypt_button_clicked, bg="#008CBA", fg="white", font=("Arial", 10, "bold"))
encrypt_button.pack(side="left", padx=10)
decrypt_button = Button(frame_buttons, text="Decrypt Image", command=decrypt_button_clicked, bg="#f44336", fg="white", font=("Arial", 10, "bold"))
decrypt_button.pack(side="left", padx=10)
save_button = Button(frame_buttons, text="Save Images", command=save_images, bg="#555555", fg="white", font=("Arial", 10, "bold"))
save_button.pack(side="left", padx=10)

root.mainloop()
