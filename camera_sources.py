from camera_laptop import get_laptop_video_stream
from camera_phone import get_phone_video_stream

from cmd_logger import log_function

class CameraSource:
    """Base class for different camera sources."""
    @log_function
    def get_stream(self):
        raise NotImplementedError("Subclasses should implement this method.")

class LaptopCameraSource(CameraSource):
    """Handles the laptop camera stream."""
    @log_function
    def get_stream(self):
        return get_laptop_video_stream()

class PhoneCameraSource(CameraSource):
    """Handles the phone camera stream."""
    @log_function
    def __init__(self, ip_address):
        self.ip_address = ip_address

    @log_function
    def get_stream(self):
        return get_phone_video_stream(self.ip_address)
