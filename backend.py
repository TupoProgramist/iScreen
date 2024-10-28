import threading
import time
import json
import sys
from camera import Camera
from hand import Hand
from engine import Engine

class Backend(threading.Thread):
    def __init__(self, shared_data):
        super().__init__()
        self.shared_data = shared_data  # Shared dictionary of variables
        
        self.camera = shared_data["classes"]["camera"]
        self.hand = shared_data["classes"]["hand"]
        self.engine = shared_data["classes"]["engine"]

        self.conditions = self.shared_data["conditions"]

        # Load configuration from config.json
        self.config = self.load_config()
        self.interval = self.config["BACKEND_TIMER_INTERVAL"] / 1000.0  # Convert ms to seconds

    def run(self):
        """Main loop of the backend thread."""
        start_time = time.time()
        while 1:
            # Calculate the time taken for processing
            elapsed_time = time.time() - start_time
            time_to_sleep = max(0, self.interval - elapsed_time)
            time.sleep(time_to_sleep)
            start_time = time.time()

            # Capture the raw frame from the camera
            self.camera.get_frame()

            # Update the hand landmarks based on the current raw frame
            self.hand.update_landmarks()
            
            #asking engine to determine the gestue
            

    def load_config(self):
        """Load configuration from the config.json file."""
        with open("config.json", "r") as f:
            config = json.load(f)
            if config is None:
                raise ValueError("Configuration file is empty or invalid.")
        return config
    
    