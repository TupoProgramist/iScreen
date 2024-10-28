import cv2
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtCore import Qt

class Camera:
    def __init__(self, shared_data):
        self.cap = None
        self.shared_data = shared_data

    def open_camera(self):
        """Open the camera."""
        self.cap = cv2.VideoCapture(0)
        self.width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    def get_frame(self):
        """Capture a frame from the camera."""
        if self.cap.isOpened():
            ret, self.shared_data["raw_frame"] = self.cap.read()

    def release_camera(self):
        """Release the camera."""
        if self.cap:
            self.cap.release()

    def frame_to_pixmap(self, size):
        """Convert a frame to QPixmap for displaying in UI."""
        frame = self.shared_data["frame"]

        if frame is not None:
            # Convert the frame from BGR to RGB
            rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = rgb_image.shape
            bytes_per_line = ch * w

            # Convert RGB image to QImage
            qt_image = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(qt_image)

            # Scale the pixmap to fit the size of the label while keeping aspect ratio
            scaled_pixmap = pixmap.scaled(size, Qt.KeepAspectRatio, Qt.SmoothTransformation)

            # Update shared data with the scaled QPixmap
            self.shared_data["QPixmap"] = scaled_pixmap
        else:
            self.shared_data["QPixmap"] = QPixmap()


