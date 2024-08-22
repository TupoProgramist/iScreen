import cv2

from cmd_logger import log_function

@log_function
def get_phone_video_stream(ip_address):
    """Opens the video stream from the IP Webcam on the phone."""
    stream_url = f"http://{ip_address}:8080/video"
    return cv2.VideoCapture(stream_url)

@log_function
def release_video_stream(cap):
    """Releases the video stream."""
    if cap is not None and cap.isOpened():
        cap.release()