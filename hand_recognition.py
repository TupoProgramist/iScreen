# hand_recognition.py
import cv2
import mediapipe as mp

from cmd_logger import log_function

# Initialize MediaPipe Hand Detection
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(static_image_mode=False,
                       max_num_hands=2,
                       min_detection_confidence=0.5,
                       min_tracking_confidence=0.5)

@log_function
def process_frame(frame):
    """Process the frame and return the results with detected hand landmarks."""
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb_frame)
    return result

@log_function
def annotate_frame(frame, result):
    """Annotate the frame with hand landmarks and labels."""
    if result.multi_hand_landmarks:
        for hand_landmarks, hand_info in zip(result.multi_hand_landmarks, result.multi_handedness):
            hand_label = hand_info.classification[0].label
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            cv2.putText(frame, f'{hand_label} Hand', 
                        (int(hand_landmarks.landmark[0].x * frame.shape[1]), 
                         int(hand_landmarks.landmark[0].y * frame.shape[0]) - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 
                        1, (0, 255, 0), 2, cv2.LINE_AA)
    return frame
