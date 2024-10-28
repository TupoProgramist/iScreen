from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QSizePolicy
from PySide6.QtCore import Qt, QTimer
import sys
import os
import json
import logging
from calibrate import start_calibration, add_calibration_point
from engine import Engine
from camera import Camera
from backend import Backend

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(message)s')

class UI(QMainWindow):
    def __init__(self, shared_data, custom_functions=None):
        super().__init__()
        
        self.is_calibrating = False
        self.calibration_points = []
        
        self.shared_data = shared_data
        self.camera = self.shared_data["classes"]["camera"]

        self.custom_functions = custom_functions if custom_functions else {}

        # Set window properties
        self.setWindowTitle("Hand Tracking Application")
        self.setGeometry(100, 100, 1920, 1080)  # Initial size of the window

        # Camera label for displaying video feed
        self.camera_label = QLabel(self)
        self.camera_label.setAlignment(Qt.AlignCenter)
        self.camera_label.setStyleSheet("background-color: black;")
        self.camera_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.camera_label.setMinimumSize(self.camera.width, self.camera.height)  # Set minimum size
        
        self.camera_label.mousePressEvent = self.record_calibration_point
        
        # Initialize camera size based on the label size
        self.camera_size = self.camera_label.size()  # <<--- Here

        # Bottom bar layout for buttons and labels
        self.bottom_bar = QHBoxLayout()

        self.cal_lab = QLabel("Calibration Process")
        self.cal_lab.setAlignment(Qt.AlignCenter)
        self.cal_lab.setStyleSheet("background-color: gray;")
        self.cal_lab.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.bottom_bar.addWidget(self.cal_lab)

        self.calibrate_button = QPushButton("Calibrate")
        self.calibrate_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.calibrate_button.clicked.connect(self.start_calibration)
        self.bottom_bar.addWidget(self.calibrate_button)

        self.start_pause_button = QPushButton("Start/Pause")
        self.start_pause_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.start_pause_button.clicked.connect(self.start_pause)
        self.bottom_bar.addWidget(self.start_pause_button)

        self.quit_button = QPushButton("Quit")
        self.quit_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.quit_button.clicked.connect(self.quit_app)
        self.bottom_bar.addWidget(self.quit_button)

        self.sta_lab = QLabel("Status: Paused")
        self.sta_lab.setAlignment(Qt.AlignCenter)
        self.sta_lab.setStyleSheet("background-color: gray;")
        self.sta_lab.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.bottom_bar.addWidget(self.sta_lab)

        self.ges_lab = QLabel("Current Gesture: None")
        self.ges_lab.setAlignment(Qt.AlignCenter)
        self.ges_lab.setStyleSheet("background-color: gray;")
        self.ges_lab.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.bottom_bar.addWidget(self.ges_lab)

        # Main layout
        self.main_layout = QVBoxLayout()
        self.main_layout.addWidget(self.camera_label, stretch=6)  # High stretch factor
        self.main_layout.addLayout(self.bottom_bar, stretch=1)  # Low stretch factor

        central_widget = QWidget(self)
        central_widget.setLayout(self.main_layout)
        self.setCentralWidget(central_widget)

        self.main_layout.activate()
        self.camera_label.updateGeometry()
        
        # Load configuration (if any)
        self.config = self.load_config()

        # Timer to update the UI with new frames
        self.timer = QTimer()
        ui_timer_interval = self.config.get("UI_TIMER_INTERVAL", 40) / 1000  # Default to 40ms if not found in config
        self.timer.timeout.connect(self.update_video_feed)
        self.timer.start(ui_timer_interval)

    def update_video_feed(self):
        """Fetch the latest frame from the shared data and update the camera feed."""
        # Update the camera size dynamically
        self.camera_size = self.camera_label.size()
        if not self.camera_size.isEmpty():
            self.camera.frame_to_pixmap(self.camera_size)

        pixmap = self.shared_data.get("QPixmap")
        if pixmap:
            self.camera_label.setPixmap(pixmap)
            self.camera_label.setAlignment(Qt.AlignCenter)
        else:
            logging.warning("No QPixmap found in shared_data.")

    def start_calibration(self):
        """Start the calibration process."""
        self.is_calibrating = True
        self.calibration_points.clear()
        self.cal_lab.setText("Calibration: Click the top-left corner")

    def record_calibration_point(self, event):
        """Record a calibration point during the calibration process."""
        if self.is_calibrating:
            x = event.pos().x()
            y = event.pos().y()
            
            #checking the eligibility
            min_size = self.camera_label.minimumSize()
            
            wx = x - (self.camera_label.width()-min_size.width())/2
            wy = y - (self.camera_label.height()-min_size.height())/2
            
            if wx <= 0 or wy <= 0 or wx >= min_size.width() or wy >= min_size.height():
                print("OUT OF ZONE")
                return     
            
            self.calibration_points.append([wx, wy])
            logging.info(f"Calibration point recorded: {wx}, {wy}")

            if len(self.calibration_points) == 1:
                self.cal_lab.setText("Calibration: Click the top-right corner")
            elif len(self.calibration_points) == 2:
                self.cal_lab.setText("Calibration: Click the bottom-right corner")
            elif len(self.calibration_points) == 3:
                self.cal_lab.setText("Calibration: Click the bottom-left corner")
            elif len(self.calibration_points) == 4:
                self.cal_lab.setText("Calibration complete")
                self.is_calibrating = False
                
                self.perform_calibration()

    def perform_calibration(self):
        self.shared_data["is_calibrated"] = True
        self.shared_data["screen_coords"] = self.calibration_points.copy()
        logging.info("Calibration points: " + str(self.calibration_points))
        self.shared_data["classes"]["mouse"].new_screen()
        # Implement your calibration logic here

    def start_pause(self):
        """Handle start/pause button click."""
        logging.info("Start/Pause button pressed.")
        if 'start_pause' in self.custom_functions:
            for func in self.custom_functions['start_pause']:
                func()
        self.shared_data["is_stopped"] = not self.shared_data["is_stopped"]

    def quit_app(self):
        """Handle quit button click or window close event."""
        logging.info("Quitting application...")
        if 'quit' in self.custom_functions:
            for func in self.custom_functions['quit']:
                func()
        os._exit(0)

    def update_video_feed(self):
        """Fetch the latest frame from the shared data and update the camera feed."""
        self.camera.frame_to_pixmap(self.camera_size)
        
        self.camera_label.setPixmap(self.shared_data["QPixmap"])
        self.camera_label.setAlignment(Qt.AlignCenter)

    def closeEvent(self, event):
        """Handle the close event (window close button)."""
        self.quit_app()

    def keyPressEvent(self, event):
        """Handle keypress events."""
        if event.key() == Qt.Key_S:
            # Toggle shared_data["is_stopped"]
            self.start_pause()
            logging.info(f"Toggle is_stopped: {self.shared_data['is_stopped']}")
        elif event.key() == Qt.Key_Q:
            # Quit the application
            self.quit_app()

    def load_config(self):
        """Load configuration from a config.json file (optional)."""
        try:
            with open("config.json", "r") as f:
                return json.load(f)
        except FileNotFoundError:
            logging.info("config.json file not found. Using default configuration.")
            return {}
