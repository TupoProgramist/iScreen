import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import threading
from backend import CameraBackend
import cv2
import sys

class CameraApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Camera Source Selection")

        # Initialize the backend
        self.backend = CameraBackend()

        self.selected_source = tk.StringVar()

        # Create ComboBox for camera selection
        self.combo = ttk.Combobox(root, textvariable=self.selected_source)
        self.combo['values'] = ('Laptop Camera', 'Phone Camera')
        self.combo.current(0)  # Set default to Laptop Camera
        self.combo.pack(pady=10)

        # Create Change button
        self.change_button = tk.Button(root, text="Change", command=self.change_camera_threaded)
        self.change_button.pack(pady=10)

        # Status Label
        self.status_label = tk.Label(root, text="Camera Ready", fg="green")
        self.status_label.pack(pady=10)

        self.imgtk = None  # Initialize the image reference

        # Start with the laptop camera
        self.backend.start_camera('Laptop Camera')
        self.start_video_display()

        # Handle the window close event
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def change_camera_threaded(self):
        """Starts the camera change process in a new thread to keep the UI responsive."""
        selected_camera = self.selected_source.get()

        # Check if the selected camera is the current one
        if selected_camera == self.backend.current_camera_type:
            self.status_label.config(text="Already this type", fg="blue")
            self.root.after(3000, lambda: self.status_label.config(text="Camera Ready", fg="green"))
            return

        # Stop any ongoing camera change
        if self.backend.video_thread and self.backend.video_thread.is_alive():
            self.backend.stop_event.set()  # Signal to stop the ongoing thread
            self.backend.video_thread.join()

        self.backend.stop_event.clear()  # Reset the stop event for the new thread
        self.status_label.config(text="In Progress...", fg="orange")  # Update status to "In Progress"
        self.backend.video_thread = threading.Thread(target=self.change_source)
        self.backend.video_thread.start()

    def change_source(self):
        source = self.selected_source.get()

        if source == 'Laptop Camera':
            self.backend.start_camera('Laptop Camera')
            self.start_video_display()
            self.status_label.config(text="Camera Ready", fg="green")
        elif source == 'Phone Camera':
            ip_webcam_ip = self.ask_for_ip_on_main_thread()
            if ip_webcam_ip is None:
                self.status_label.config(text="Camera Ready", fg="green")
                return

            phone_camera_thread = threading.Thread(target=self.connect_phone_camera_threaded, args=(ip_webcam_ip,))
            phone_camera_thread.start()

    def connect_phone_camera_threaded(self, ip_webcam_ip):
        """Handles the phone camera connection in a separate thread."""
        if not self.backend.connect_phone_camera(ip_webcam_ip):
            self.backend.fallback_to_laptop_camera()
            self.start_video_display()
            self.status_label.config(text="Error", fg="red")
        else:
            self.start_video_display()
            self.status_label.config(text="Camera Ready", fg="green")

    def ask_for_ip_on_main_thread(self):
        ip_address = None
        def get_ip():
            nonlocal ip_address
            ip_address = simpledialog.askstring("IP Webcam", "Enter the IP address of your phone running IP Webcam:", parent=self.root)
        self.root.after(0, get_ip)
        self.root.wait_window()
        return ip_address

    def start_video_display(self):
        """Starts the video display in a separate thread."""
        self.backend.video_thread = threading.Thread(target=self.backend.display_video, args=(self.root, self.update_ui))
        self.backend.video_thread.start()

    def update_ui(self, root, frame):
        """Update only the video label with the new frame."""
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame_rgb)
        self.imgtk = ImageTk.PhotoImage(image=img)  # Keep reference to the image

        # Update only the video label, not the whole root window
        if not hasattr(self, 'video_label'):
            self.video_label = tk.Label(root)
            self.video_label.pack()
        self.video_label.imgtk = self.imgtk  # Store reference to avoid garbage collection
        self.video_label.configure(image=self.imgtk)

        # Only update the video label instead of the entire root window
        self.video_label.update_idletasks()

    def on_closing(self):
        """Handles the application exit by ensuring all threads and resources are properly closed."""
        sys.exit("Forcing exit to terminate all threads")


    def start(self):
        """Starts the Tkinter main loop."""
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            self.on_closing()

def run_app():
    root = tk.Tk()
    app = CameraApp(root)
    app.start()
