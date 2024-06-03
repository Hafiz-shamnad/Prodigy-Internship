import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
import pyshark
import psutil
import threading
from PIL import Image, ImageTk

class NetworkTrafficAnalyzer:
    def __init__(self, root):
        self.root = root
        self.root.title("Network Traffic Analyzer")

        # Load the icon file using PIL
        icon_image = Image.open("/Prodigy CY Task 5/app_icon.ico")

        # Convert the PIL image to a Tkinter-compatible format
        icon = ImageTk.PhotoImage(icon_image)

        # Set the window icon
        root.iconphoto(True, icon)

        # Configure custom styles
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("TFrame", background="#f0f0f0")
        self.style.configure("TLabel", background="#f0f0f0", font=("Helvetica", 10))
        self.style.configure("TButton", background="#4CAF50", foreground="white", font=("Helvetica", 10, "bold"))

        # Main frame
        self.main_frame = ttk.Frame(root)
        self.main_frame.grid(row=0, column=0, padx=20, pady=20)

        # Interface dropdown
        self.interface_label = ttk.Label(self.main_frame, text="Interface:")
        self.interface_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.interface_var = tk.StringVar(root)
        self.interface_dropdown = ttk.Combobox(self.main_frame, textvariable=self.interface_var, state="readonly")
        self.interface_dropdown.grid(row=0, column=1, padx=5, pady=5)

        # Buttons
        self.refresh_button = ttk.Button(self.main_frame, text="Refresh Interfaces", command=self.update_interfaces)
        self.refresh_button.grid(row=0, column=2, padx=5, pady=5)
        self.start_button = ttk.Button(self.main_frame, text="Start Capture", command=self.start_capture)
        self.start_button.grid(row=0, column=3, padx=5, pady=5)
        self.stop_button = ttk.Button(self.main_frame, text="Stop Capture", command=self.stop_capture)
        self.stop_button.grid(row=0, column=4, padx=5, pady=5)

        # Information text area
        self.info_frame = ttk.Frame(root)
        self.info_frame.grid(row=1, column=0, pady=20)
        self.info_text = scrolledtext.ScrolledText(self.info_frame, width=100, height=20, wrap="word")
        self.info_text.pack(expand=True, fill="both")

        # Initialize and update interfaces
        self.update_interfaces()

    def update_interfaces(self):
        interfaces = list(psutil.net_if_addrs().keys())
        if interfaces:
            self.interface_dropdown['values'] = interfaces
            self.interface_var.set(interfaces[0])
        else:
            self.interface_dropdown['values'] = []

    def start_capture(self):
        interface = self.interface_var.get()
        self.info_text.delete(1.0, tk.END)
        self.info_text.insert(tk.END, f"Starting packet capture on interface {interface}...\n")
        self.packet_capture_thread = threading.Thread(target=self.capture_packets, args=(interface,))
        self.packet_capture_thread.start()

    def capture_packets(self, interface):
        try:
            self.packet_capture = pyshark.LiveCapture(interface=interface)
            for packet in self.packet_capture.sniff_continuously():
                self.display_packet_info(packet)
        except Exception as e:
            self.info_text.insert(tk.END, f"Error starting packet capture: {e}\n")

    def stop_capture(self):
        self.start_button.config(state="normal")
        self.info_text.insert(tk.END, "Packet capture stopped.\n")

    def display_packet_info(self, packet):
        try:
            info = f"Source IP: {packet.ip.src}\n"
            info += f"Destination IP: {packet.ip.dst}\n"
            info += f"Protocol: {packet.transport_layer}\n"
            info += f"Length: {packet.length}\n"
            info += "-" * 50 + "\n"
            self.info_text.insert(tk.END, info)
        except AttributeError:
            pass


if __name__ == "__main__":
    root = tk.Tk()
    app = NetworkTrafficAnalyzer(root)
    root.mainloop()
