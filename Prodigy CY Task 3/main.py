import tkinter as tk
from tkinter import ttk, messagebox

from PIL import Image, ImageTk
from ttkthemes import ThemedStyle


# Function to analyze password complexity
def analyze_password():
    password = password_entry.get()
    length = len(password)

    # Check length of password
    if length < 6:
        complexity_label.config(text="Complexity: Bad", fg="red")
        crack_time_label.config(text="Time to Crack: Seconds", fg="red")
        messagebox.showwarning("Warning", "Password is too short! Must be at least 6 characters long.")
        return
    elif length < 10:
        complexity_label.config(text="Complexity: Average", fg="orange")
        crack_time_label.config(text="Time to Crack: Hours", fg="orange")
    elif length < 14:
        complexity_label.config(text="Complexity: Good", fg="green")
        crack_time_label.config(text="Time to Crack: Days", fg="green")
    else:
        complexity_label.config(text="Complexity: Excellent", fg="blue")
        crack_time = estimate_crack_time(length)
        crack_time_label.config(text=f"Time to Crack: {crack_time}", fg="blue")

    # Update progress bar
    progress_value = min(length / 14 * 100, 100)  # Normalize length to a percentage between 0 and 100
    progress_bar["value"] = progress_value


# Function to estimate time to crack in years, months, and days
def estimate_crack_time(length):
    time_to_crack_seconds = 0.0000000005 * (94 ** length)
    time_to_crack_days = time_to_crack_seconds / (3600 * 24)  # Convert seconds to days
    years = int(time_to_crack_days / 365)
    months = int((time_to_crack_days % 365) / 30)
    days = int((time_to_crack_days % 365) % 30)
    return f"{years} Years, {months} Months, {days} Days"


# Create GUI
root = tk.Tk()
root.title("Password Complexity Analyzer")

# Load the icon file using PIL
icon_image = Image.open("/Prodigy CY Task 3/app_icon.ico")

# Convert the PIL image to a Tkinter-compatible format
icon = ImageTk.PhotoImage(icon_image)

# Set the window icon
root.iconphoto(True, icon)


# Styling
style = ThemedStyle(root)
style.set_theme("arc")  # Choose the theme - you can try different themes

# Password Entry
password_label = tk.Label(root, text="Enter Password:", fg="black")
password_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")
password_entry = tk.Entry(root, show="*")
password_entry.grid(row=0, column=1, padx=5, pady=5)

# Analyze Button
analyze_button = tk.Button(root, text="Analyze", command=analyze_password, bg="light blue", fg="black")
analyze_button.grid(row=1, column=0, columnspan=2, pady=5)

# Progress Bar
progress_bar = ttk.Progressbar(root, orient="horizontal", length=200, mode="determinate")
progress_bar.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

# Complexity Label
complexity_label = tk.Label(root, text="Complexity:", fg="black")
complexity_label.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

# Crack Time Label
crack_time_label = tk.Label(root, text="Time to Crack:", fg="black")
crack_time_label.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

root.mainloop()
