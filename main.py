from PySide6.QtWidgets import QApplication
import sys
from backend import Backend
from ui import UI
from mouse import Mouse
from engine import Engine
from hand import Hand
from camera import Camera

def run_app(custom_functions=None):
    app = QApplication(sys.argv)

    # Initialize a thread-safe queue for communication
    shared_data = {
                    "raw_frame" : None,
                    "frame": None,
                    "is_calibrated" : False,
                    "is_stopped" : True,
                    "conditions" : 
                    {
                        "RMB_hold": False,
                        "LMB_hold": False,
                        "scale_hold": False
                    },
                    "hands_landmarks_pixel": None,
                    "forefinger_coords": None,
                    "screen_coords": [],
                    "QPixmap": None,
                    
                    "classes":{
                        "hand": None,
                        "engine": None,
                        "camera": None,
                        "UI": None,
                        "mouse": None,
                        "backend": None,
                    },
                    "hand_is_visible": False                    
                  }
    
    #Creating the classes
    hand = Hand(shared_data)
    shared_data["classes"]["hand"] = hand
    engine = Engine(shared_data)
    shared_data["classes"]["engine"] = engine
    camera = Camera(shared_data)
    camera.open_camera()
    shared_data["classes"]["camera"] = camera
    
    ui = UI(shared_data,custom_functions)
    shared_data["classes"]["UI"] = ui
    
    
    
    mouse = Mouse(shared_data)
    shared_data["classes"]["mouse"] = mouse
    backend = Backend(shared_data)
    shared_data["classes"]["backend"] = backend
    
    
    
    
    
    
    mouse.start()  # Start the Mouse thread
    backend.start()  # Start the backend thread
    ui.show() # Start the ui thread

    sys.exit(app.exec())

if __name__ == "__main__":
    custom_functions = {
        'calibrate': [lambda: print("Custom calibration step 1")],
        'start_pause': [lambda: print("Custom start/pause action")],
        'quit': [lambda: print("Custom quit action")]
    }
    run_app(custom_functions)
