import threading
import time
import json
import sys
from camera import Camera
from hand import Hand
from engine import Engine

class Backend(threading.Thread):
    """
    Backend processing thread that coordinates data flow between camera, hand detection, and gesture engine.
    This class serves as the central coordinator for real-time processing of camera input,
    hand landmark detection, and gesture recognition for interactive whiteboard functionality.
    """
    def __init__(self, shared_data):
        super().__init__()
        # Store reference to shared data structure for inter-thread communication
        self.shared_data = shared_data  # Shared dictionary of variables
        
        # Initialize references to core processing modules
        self.camera = shared_data["classes"]["camera"]
        self.hand = shared_data["classes"]["hand"]
        self.engine = shared_data["classes"]["engine"]

        # Access synchronization conditions for thread coordination
        self.conditions = self.shared_data["conditions"]

        # Load timing configuration to control processing frequency
        self.config = self.load_config()
        self.interval = self.config["BACKEND_TIMER_INTERVAL"] / 1000.0  # Convert ms to seconds

    def run(self):
        """
        Main processing loop that executes at configured intervals.
        Maintains consistent timing while processing camera frames and updating hand landmarks.
        This loop is the heartbeat of the real-time gesture recognition system.
        """
        start_time = time.time()
        while 1:
            # Implement precise timing control to maintain consistent frame processing rate
            elapsed_time = time.time() - start_time
            time_to_sleep = max(0, self.interval - elapsed_time)
            time.sleep(time_to_sleep)
            start_time = time.time()

            # Capture fresh frame data from camera module
            self.camera.get_frame()

            # Process the captured frame to extract hand landmark coordinates
            self.hand.update_landmarks()
            
            # TODO: Engine should analyze landmarks and determine current gesture
            #asking engine to determine the gestue
            

    def load_config(self):
        """
        Load application configuration from JSON file.
        Centralizes configuration management for timing intervals and other parameters.
        
        Returns:
            dict: Configuration parameters loaded from config.json
            
        Raises:
            ValueError: If configuration file is empty or contains invalid JSON
        """
        with open("config.json", "r") as f:
            config = json.load(f)
            if config is None:
                raise ValueError("Configuration file is empty or invalid.")
        return config
