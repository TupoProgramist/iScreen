# iScreen

> Transform any whiteboard into an interactive smart board using computer vision and hand gesture recognition.

## Motivation

Interactive whiteboards are expensive, inflexible, and often require specialized hardware setups. This project was created as a personal solution to transform any regular whiteboard or projection surface into an interactive smart board using just a laptop camera and hand gesture recognition. By leveraging computer vision technology, iScreen provides an affordable and flexible alternative to traditional interactive whiteboard systems.

## Key Features
- **Real-time hand tracking**: Uses computer vision to detect and track hand movements in 3D space
- **Gesture recognition**: Interprets specific hand gestures (e.g., "only forefinger opened") as mouse interactions
- **Whiteboard calibration**: Simple 4-point calibration system to map any rectangular surface as an interactive area
- **Multi-threaded architecture**: Concurrent processing of camera input, hand detection, and gesture interpretation for optimal performance
- **Configurable timing**: Adjustable processing intervals for different hardware capabilities

## Tech Stack
- **Language:** Python
- **Key Libraries:** 
  - OpenCV (cv2) - Computer vision and hand landmark detection
  - PyAutoGUI - Mouse cursor control and screen interaction
  - PySide6 - Modern GUI framework for calibration interface
  - Threading - Multi-threaded real-time processing
- **Architecture:** Modular design with separate components for camera, hand detection, gesture engine, and backend coordination

## Installation & Usage

1. Clone the repository:
```bash
git clone https://github.com/your-username/iScreen.git
cd iScreen
```

2. Install dependencies:
```bash
pip install opencv-python pyautogui PySide6 mediapipe
```

3. Configure your camera and processing settings in `config.json`

4. Run the main application:
```bash
python main.py
```

5. Calibration Process:
   - Press the "Select" button in the interface
   - Click on the 4 corners of your whiteboard/projection area in order
   - Confirm the calibration
   - Use hand gestures (forefinger extended) to interact with the calibrated area

## Project Architecture

The application follows a modular, multi-threaded architecture:

- **main.py**: Application entry point and coordination hub
- **camera.py**: Camera input handling and frame capture
- **hand.py**: Hand landmark detection and tracking using MediaPipe
- **engine.py**: Gesture interpretation and coordinate transformation logic
- **backend.py**: Real-time data pipeline coordination between modules
- **calibrate.py**: Interactive calibration interface for whiteboard mapping
- **ui.py**: User interface components and controls

## Project Status & Note

This project was developed as a personal tool to create an affordable alternative to expensive interactive whiteboard solutions. The code demonstrates practical application of computer vision, real-time processing, and human-computer interaction concepts. While currently configured for specific use cases, it serves as a portfolio piece showcasing skills in:

- **Computer Vision**: Real-time hand tracking and gesture recognition
- **Multi-threading**: Concurrent processing for responsive real-time applications  
- **API Integration**: OpenCV and MediaPipe for advanced computer vision capabilities
- **GUI Development**: Cross-platform interface design with PySide6
- **System Integration**: Bridging computer vision with system-level mouse control

The project represents a practical solution to a real-world problem while demonstrating technical proficiency across multiple domains of software development.
