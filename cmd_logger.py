import inspect
import os
from functools import wraps

function_call_counts = {}
last_called_function = None

def log_function(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        global last_called_function
        
        # Get the current frame
        current_frame = inspect.currentframe()
        
        if current_frame is None:
            return func(*args, **kwargs)
        
        # Get the caller's frame (the frame that called this function)
        caller_frame = current_frame.f_back
        
        # Safeguard: Ensure caller_frame is valid
        if caller_frame is None:
            return func(*args, **kwargs)
        
        function_name = caller_frame.f_code.co_name
        
        if function_name == "display_video":
            return func(*args, **kwargs)
        
        # Get the function name and file name
        
        key = (function_name)
        # Check if this function was the last one called
        if key == last_called_function:
            # Increment the consecutive call count
            function_call_counts[key] += 1
        else:
            # Reset the count if this function was not called consecutively
            function_call_counts[key] = 1
            last_called_function = key
            
        # Determine what to do based on the consecutive call count
        call_count = function_call_counts[key]
        
        if call_count > 2:
            # More than twice consecutively, skip execution
            return None
        
        # Get the caller's frame (the frame that called this function)
        caller_frame = current_frame.f_back
        
        # Get the function name and file name
        
        file_name = os.path.basename(caller_frame.f_code.co_filename)
        
        # Get the class name, if it exists
        class_name = None
        if 'self' in caller_frame.f_locals:
            class_name = caller_frame.f_locals['self'].__class__.__name__        
        
        if call_count == 1:
            # First time, log and execute the function
            if class_name:
                print(f"Execute: fil [{file_name}] > cla [{class_name}] > fun [{function_name}]")
            else:
                print(f"Execute: fil [{file_name}] > fun [{function_name}]")
            return func(*args, **kwargs)
        else:
            # Second time, just print "again" and execute the function
            print("again")
            return func(*args, **kwargs)
        
    
    return wrapper