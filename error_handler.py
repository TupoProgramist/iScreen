import logging
from tkinter import messagebox

from cmd_logger import log_function

# Setup logging
logging.basicConfig(level=logging.INFO)

@log_function
def handle_error(message, user_message="An error occurred"):
    """Logs the error and shows a messagebox to the user."""
    logging.error(message)
    messagebox.showwarning("Error", user_message)
