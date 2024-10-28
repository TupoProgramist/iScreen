import threading
import logging
import time
import json
import pyautogui
from screeninfo import get_monitors 
pyautogui.FAILSAFE = False

#EEEEEEE
import numpy as np
import math

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(message)s')

class Mouse(threading.Thread):
    def __init__(self, shared_data):
        super().__init__()
        self.shared_data = shared_data # Shared data structure for
        
        self.engine = self.shared_data["classes"]["engine"]
        
        self.monitor_size = [get_monitors()[-1].width, get_monitors()[-1].height]
        
        self.mouse_conditions = {
                    "RMB_hold": False,
                    "LMB_hold": False,
                    "scale_hold": False
                }
        
        self.forefinger_pos = [0,0]
        
        self.conditions = self.shared_data["conditions"]
        
        self.load_config()
    
    def new_screen(self):
        screen_coords = [self.shared_data["screen_coords"][i] for i in [0, 2]]
        self.screen_size = [screen_coords[1][0]-screen_coords[0][0], screen_coords[1][1]-screen_coords[0][1]]
        self.s_m_ratio = [self.monitor_size[0]/self.screen_size[0], self.monitor_size[1]/self.screen_size[1]]
        print("MOUSE UPDATE")
    
    def update_for_pos(self):
        if not self.shared_data["hand_is_visible"] or self.shared_data["is_stopped"]:
            return
        
        forefinger_coords = self.shared_data["forefinger_coords"]
        screen_coords = self.shared_data["screen_coords"]
        
        for_abs_pos = [ forefinger_coords[0]-screen_coords[0][0], forefinger_coords[1]-screen_coords[0][1] ]
        for_rel_pos = [for_abs_pos[0]*self.s_m_ratio[0], for_abs_pos[1]*self.s_m_ratio[1] ]
        
        self.forefinger_pos = [for_rel_pos[0], for_rel_pos[1]]
    
    
    
    
    def run(self):
        start_time = time.time()
        
        while 1:
            elapsed_time = time.time() - start_time
            time_to_sleep = max(0, self.mouse_timer_interval - elapsed_time)
            time.sleep(time_to_sleep)
            start_time = time.time()
            
            self.engine.det_ges()
            
            self.update_for_pos()
            
            key = self.find_difference(self.shared_data["conditions"], self.mouse_conditions)
            
            if key != None:
                '''
                if key == "LMB_hold":
                    if self.mouse_conditions[key] == True:
                        pyautogui.mouseUp(button='right')
                    else:
                        pyautogui.mouseDown(button='right')
                        '''
                if key == "RMB_hold":
                    if self.mouse_conditions[key] == True:
                        pyautogui.mouseUp(button='left')
                    else:
                        pyautogui.mouseDown(button='left') 
                        
                self.mouse_conditions[key] = not self.mouse_conditions[key]
                        
              
                                        
            if self.shared_data["hand_is_visible"]:
                pyautogui.moveTo(self.forefinger_pos[0],self.forefinger_pos[1],duration=self.mouse_timer_interval)
            
            
    def find_difference(self, dict1, dict2):
        for key in dict1:
            if dict1[key] != dict2[key]:
                return key 
        return None  # Return None if no difference is found
            
    def load_config(self):
        
        
        try:
            with open("config.json", "r") as f:
                j = json.load(f)
        except FileNotFoundError:
            logging.info("config.json file not found. Using default configuration.")
            return {}
        
        self.mouse_timer_interval = j.get("MOUSE_TIMER_INTERVAL", 40) / 1000.0
         
         
        '''
            changed = self.find_difference(self.mouse_conditions, self.conditions)
            
            if changed == "RMB_hold":
                if self.mouse_conditions["RMB_hold"] == True:
                    pyautogui.mouseUp(button='right')
                else:
                    pyautogui.mouseDown(button='right')
            if changed == "LMB_hold":
                if self.mouse_conditions["LMB_hold"] == True:
                    pyautogui.mouseUp(button='left')
                else:
                    pyautogui.mouseDown(button='left')
            '''