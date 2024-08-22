import cv2
import threading
from camera_sources import LaptopCameraSource, PhoneCameraSource
from error_handler import handle_error
from hand_recognition import process_frame, annotate_frame
import sys

class CameraBackend:
    def __init__(self):
        self.cap = None
        self.video_thread = None
        self.running = False
        self.stop_event = threading.Event()
        self.current_camera_type = None

    def start_camera(self, camera_type):
        """Starts the selected camera source."""
        if camera_type == 'Laptop Camera':
            self.cap = LaptopCameraSource().get_stream()
        elif camera_type == 'Phone Camera':
            self.cap = PhoneCameraSource().get_stream()

        self.running = True
        self.current_camera_type = camera_type
        return self.cap

    def connect_phone_camera(self, ip_webcam_ip):
        """Attempts to connect to the phone camera."""
        try:
            phone_camera_source = PhoneCameraSource(ip_webcam_ip)
            if self.start_camera(phone_camera_source):
                return True
        except Exception as e:
            handle_error(f"Failed to connect to the phone camera: {e}")
            return False
        return False

    def fallback_to_laptop_camera(self):
        """Fallback to the laptop camera if the phone camera fails."""
        self.start_camera('Laptop Camera')

    def display_video(self, root, update_ui_callback):
        try:
            while self.running and self.cap.isOpened():
                ret, frame = self.cap.read()
                if not ret or not self.running:  # Exit loop if not running or frame read fails
                    print("display_video: Exiting loop due to stop signal or read failure")
                    break

                # Process the frame for hand recognition
                hand_results = process_frame(frame)
                frame = annotate_frame(frame, hand_results)

                # Update the UI with the processed frame
                update_ui_callback(root, frame)
            print("display_video: Exiting video loop")
        except Exception as e:
            handle_error(f"An error occurred while displaying video: {e}")
            self.stop_video()
        finally:
            print("display_video: Loop ended")

    def stop_video(self):
        """Stops the video streaming and releases resources."""
        sys.exit("Forcing exit to terminate all threads.")

