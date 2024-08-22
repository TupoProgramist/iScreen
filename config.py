import json

from cmd_logger import log_function

@log_function
def load_config(config_file="conf.json"):
    """Loads configuration settings from a JSON file."""
    with open(config_file, "r") as f:
        return json.load(f)

# Example usage:
# config = load_config()
# timeout = config.get("phone_camera_timeout", 10)
