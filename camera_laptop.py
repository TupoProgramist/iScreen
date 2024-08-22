import cv2

from cmd_logger import log_function

@log_function
def get_laptop_video_stream():
    """Opens the default laptop camera stream."""
    return cv2.VideoCapture(0)

@log_function
def release_video_stream(cap):
    """Releases the video stream."""
    if cap is not None and cap.isOpened():
        cap.release()