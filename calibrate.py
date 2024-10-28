# !!! CALIBRATION SHOULD BE RE-MADED

import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(message)s')

calibration_mode = False
calibration_points = []
point_labels = ["upper left", "upper right", "lower right", "lower left"]

def start_calibration(calibration_label):
    """Start the calibration process."""
    global calibration_mode, calibration_points
    if not calibration_mode:
        calibration_points = []
        calibration_mode = True
        calibration_label.setText(f"Select the {point_labels[0]} corner")
        logging.info("Calibration started. Select the upper left corner.")
    else:
        calibration_label.setText("Calibration already in progress")

def add_calibration_point(point, calibration_label, Engine):
    """Add a calibration point based on the current step in the calibration process."""
    global calibration_mode, calibration_points
    if calibration_mode and len(calibration_points) < 4:
        calibration_points.append(point)
        Engine.add_point(point)
        logging.info(f"Point {len(calibration_points)} ({point_labels[len(calibration_points) - 1]}) selected: {point}")

        if len(calibration_points) < 4:
            next_point_label = point_labels[len(calibration_points)]
            calibration_label.setText(f"Select the {next_point_label} corner")
            logging.info(f"Next, select the {next_point_label} corner.")
        else:
            calibration_label.setText("Calibration completed")
            logging.info("Calibration completed.")
            calibration_mode = False  # End calibration
            # Trigger button reset
            return True
    return False
