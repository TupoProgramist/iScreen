import cv2
import mediapipe as mp
import math

class Hand:
    def __init__(self, shared_data):
        
        self.shared_data = shared_data  # Shared dictionary of variables (e.g., 'raw_frame', 'frame')
        
        self.hands_landmarks = []  # List to hold the landmarks for multiple hands
        
        self.is_visible = False  # Flag to indicate if any hand is visible

        # Initialize MediaPipe Hand model
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.5)
        self.mp_drawing = mp.solutions.drawing_utils

    def update_landmarks(self):
        """Process the frame and update the landmarks for the right hand only."""
        # Retrieve the current frame from shared data
        raw_frame = self.shared_data['raw_frame']
        frame_with_hand = raw_frame.copy()

        # Convert the BGR image to RGB before processing
        rgb_frame = cv2.cvtColor(raw_frame, cv2.COLOR_BGR2RGB)

        # Process the frame with MediaPipe to detect hand landmarks
        results = self.hands.process(rgb_frame)

        # Reset previous landmarks
        self.reset()

        if results.multi_hand_landmarks and results.multi_handedness:
            self.is_visible = True

            for hand_landmarks, handedness in zip(results.multi_hand_landmarks, results.multi_handedness):
                # Check if the detected hand is the right hand
                if handedness.classification[0].label == "Left":
                    # Convert landmarks to pixel coordinates
                    landmarks_pixel = [(int(lm.x * raw_frame.shape[1]), int(lm.y * raw_frame.shape[0])) for lm in hand_landmarks.landmark]
                    
                    if len(landmarks_pixel) == 21:
                        self.shared_data["hand_is_visible"] = True
                    else:
                        self.shared_data["hand_is_visible"] = False
                        return
                    
                    self.shared_data["hands_landmarks_pixel"] = landmarks_pixel

                    # Extract the forefinger coordinates (index 8 in landmarks_pixel)
                    forefinger_coords = landmarks_pixel[8]
                    self.shared_data["forefinger_coords"] = forefinger_coords
                    
                    # Draw landmarks and connections on the frame for the right hand
                    self.mp_drawing.draw_landmarks(frame_with_hand, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)
                    
                    
        # Update the shared data with the processed frame
        else:
            self.shared_data["hand_is_visible"] = False
            
        self.shared_data['frame'] = frame_with_hand
    
    def reset(self):
        """Reset the hand data."""
        self.hands_landmarks = []
        self.shared_data["hands_landmarks_pixel"]
        self.is_visible = False
