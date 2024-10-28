import numpy as np
import json
import logging
import math

class Engine:
    #+
    def __init__(self, shared_data):
        self.shared_data = shared_data
        
        self.opened = [2,2,2,2,2]
        self.aligned = [2,2,2,2,2]
        
        self.prev_ben_list = [0,0,0,0,0]
        self.prev_dot_list = [0,0,0,0,0]
        
        self.fin_landmarks = [
            [1,2,3,4],
            [5,6,7,8],
            [9,10,11,12],
            [13,14,15,16],
            [17,18,19,20]
        ]
        
        self.conditions = self.shared_data["conditions"]
        
        
        self.load_config()
    
    #+ returns the bend of a finger (float)
    def find_ben(self, fin_n):
        if not self.shared_data["hand_is_visible"]:
                return
            
        landmarks = self.shared_data["hands_landmarks_pixel"].copy()
        
        unit = math.dist(landmarks[0],landmarks[9])
        bend = math.dist(landmarks[self.fin_landmarks[fin_n][0]],landmarks[self.fin_landmarks[fin_n][3]])*math.dist(landmarks[self.fin_landmarks[fin_n][1]],landmarks[self.fin_landmarks[fin_n][2]])
        rel_bend = bend/(unit**2)
        
        return rel_bend
    
    #+ returns the dot of a finger (float)
    def find_dot (self,fin_n):
        landmarks = self.shared_data["hands_landmarks_pixel"].copy()
        
        v1 = [landmarks[self.fin_landmarks[fin_n][0]], landmarks[self.fin_landmarks[fin_n][3]]]
        v2 = [landmarks[5], landmarks[6]]
        
        v1 = [v1[1][0]-v1[0][0], v1[1][1]-v1[0][1]]
        v2 = [v2[1][0]-v2[0][0], v2[1][1]-v2[0][1]]
        
        v1 = np.array(v1)
        v2 = np.array(v2)
        
        v1 = v1 / np.linalg.norm(v1)
        v2 = v2 / np.linalg.norm(v2)
        
        dot_product = np.dot(v1, v2)
        return dot_product
    
    #+ returns the bend overfluctuation (True/False)
    def overfluct_ben(self, fin_n, fin_ben):
        
        #determine the fluctuation itself
        fluctuation = abs(self.prev_ben_list[fin_n] - fin_ben)
        
        #if the finger was closed
        if self.opened[fin_n] == -1:
            
            #if the fluctuation is too big
            if fluctuation <= self.limits_ben[fin_n][2]:
                return False
            else:
                return True
            
        #if the finger was straited
        elif self.opened[fin_n] == 1:
            
            #if the fluctuation is too big
            if fluctuation <= self.limits_ben[fin_n][3]:
                return False
            else:
                return True
    
    #+ returns the dot product overfluctuation (True/False)
    def overfluct_dot(self,fin_n, fin_dot):
        
        #determine the fluctuation itself
        fluctuation = abs(self.prev_dot_list[fin_n] - fin_dot)
        
        #if the finger was perpedicular
        if self.aligned[fin_n] == -1:
            
            #if the fluctuation is too big
            if fluctuation <= self.limits_dot[fin_n][2]:
                return False
            else:
                return True
            
        #if the finger was aligned
        elif self.aligned[fin_n] == 1:
            
            #if the fluctuation is too big
            if fluctuation <= self.limits_dot[fin_n][3]:
                return False
            else:
                return True
    
    #+ determines the openess of a finger
    def det_opened(self,fin_n,ben_list):
        #cheking is it opened
        if ben_list[fin_n] >= self.limits_ben[fin_n][1]:
            #-1 closed |0 free | 1 opened
            self.opened[fin_n] = 1
            
        #cheking is it closed
        elif ben_list[0] <= self.limits_ben[fin_n][0]:
            self.opened[fin_n] = -1
            
        #if is it free
        else:
            self.opened[fin_n] = 0
        
        #print(f"opened {self.opened[fin_n]} | fin {fin_n+1} | ")
        
        
        
    #+ determines the alignment of a finger
    def det_aligned(self,fin_n,dot_list):
        #cheking is it paralel
        if dot_list[fin_n] >= self.limits_dot[fin_n][1]:
            #-1 perpedicular |0 free | 1 paralel
            self.aligned[fin_n] = 1
            
            
        #cheking is it perpendicular
        elif dot_list[fin_n] <= self.limits_dot[fin_n][0]:
            self.aligned[fin_n] = -1
            
        #if it is free
        else:
            self.aligned[fin_n] = 0
            
        #print(f"aligned {self.aligned[fin_n]} | fin {fin_n+1} | ")
        #print(f"{dot_list[fin_n]}")
    #+ determines the scale gestue
    def ges_scale(self, dot_list, ben_list):
        #1. THUMB
        #already found to not be correct
        if self.aligned[0] == 2:
            self.det_aligned(0,dot_list)
        if self.aligned[0] == 1 or self.aligned[0] == 0:
            self.conditions["scale_hold"] = False
            return
        
        #2. forefinger
        if self.opened[1] == 2:
            self.det_opened(1,ben_list)
        if self.opened[1] == -1 or self.opened[1] == 0:
            self.conditions["scale_hold"] = False
            return
        
        #3 middle
        if self.opened[2] == 2:
            self.det_opened(2,ben_list)
        if self.opened[2] == 1 or self.opened[2] == 0:
            self.conditions["scale_hold"] = False
            return
        
        #4. ring
        if self.opened[3] == 2:
            self.det_opened(3,ben_list)
        if self.opened[3] == 1 or self.opened[3] == 0:
            self.conditions["scale_hold"] = False
            return
            
        self.conditions["scale_hold"] = True
    
    #+ determines the rmb gestue
    def ges_rmb (self, dot_list, ben_list):
        #1. THUMB
        #already found to not be correct
        if self.aligned[0] == -1 or self.aligned[0] == 0:
            self.conditions["RMB_hold"] = False
            return
        
        #2. forefinger
        if self.opened[1] == -1 or self.opened[1] == 0:
            self.conditions["RMB_hold"] = False
            return
        
        #3 middle
        if self.opened[2] == 2:
            self.det_opened(2,ben_list)
        if self.opened[2] == 1 or self.opened[2] == 0:
            self.conditions["RMB_hold"] = False
            return
        
        #4. ring
        if self.opened[3] == 2:
            self.det_opened(3,ben_list)
        if self.opened[3] == 1 or self.opened[3] == 0:
            self.conditions["RMB_hold"] = False
            return
            
        self.conditions["RMB_hold"] = True
        
        
        #B) THUMB OPENESS
        #cheking is it opened
        if ben_list[0] >= self.limits_ben[0][3]:
            #-1 closed |0 free | 1 opened
            self.opened[0] = 1
            return
        #cheking is it closed
        elif ben_list[0] <= self.limits_ben[0][2]:
            self.opened[0] = -1
        #if it is free
        else:
            self.opened[0] = 0
            return
            
        #2. FOREFINGER
        ben_list[1] = self.find_ben(1)
        
        #A) FOREFINGER OPENESS        
        #cheking is it opened
        if ben_list[1] >= self.limits_ben[1][3]:
            #-1 closed |0 free | 1 opened
            self.opened[1] = 1
        #cheking is it closed
        elif ben_list[1] <= self.limits_ben[1][2]:
            self.opened[1] = -1
            return
        #if it is free
        else:
            self.opened[1] = 0
            return
        
        #2. Middle finger
        ben_list[2] = self.find_ben(2)
        #A) Middle OPENESS
        
        
        #cheking is it opened
        if ben_list[2] >= self.limits_ben[2][3]:
            #-1 closed |0 free | 1 opened
            self.opened[2] = 1
            return
        #cheking is it closed
        elif ben_list[2] <= self.limits_ben[2][2]:
            self.opened[2] = -1
        #if it is free
        else:
            self.opened[2] = 0
            return
        
        #2. Ring finger
        ben_list[3] = self.find_ben(3)
        #A) Middle OPENESS
        
        
        #cheking is it opened
        if ben_list[3] >= self.limits_ben[3][3]:
            #-1 closed |0 free | 1 opened
            self.opened[3] = 1
            return
        #cheking is it closed
        elif ben_list[3] <= self.limits_ben[3][2]:
            self.opened[3] = -1
        #if it is free
        else:
            self.opened[2] = 0
            return
        
        self.conditions["RMB_hold"] = True
    
    #+ determines the lmb gestue
    def ges_lmb (self, dot_list, ben_list):

        #1. THUMB
        #already found to not be correct
        if self.aligned[0] == 2:
            self.det_aligned(0,dot_list)
        if self.aligned[0] == -1 or self.aligned[0] == 0:
            self.conditions["LMB_hold"] = False
            return
        
        #2. forefinger
        if self.opened[1] == 2:
            self.det_opened(1,ben_list)
        if self.opened[1] == -1 or self.opened[1] == 0:
            self.conditions["LMB_hold"] = False
            return
        
        #3 middle
        if self.opened[2] == 2:
            self.det_opened(2,ben_list)
        if self.opened[2] == -1 or self.opened[2] == 0:
            self.conditions["LMB_hold"] = False
            return
        
        #4. ring
        if self.opened[3] == 2:
            self.det_opened(3,ben_list)
        if self.opened[3] == -1 or self.opened[3] == 0:
            self.conditions["LMB_hold"] = False
            return
            
        self.conditions["LMB_hold"] = True
        
    def det_ges(self):
        #0. Checking whether all the conditions are fine
        if not self.shared_data["hand_is_visible"] :
            return
        
        #1. Confgurting variables --------------------------------
        self.opened = [2,2,2,2,2]
        self.aligned = [2,2,2,2,2]
        
        ben_list = [0,0,0,0,0]
        dot_list = [0,0,0,0,0]
        
        overfluct_ben = [0, 0, 0, 0, 0]
        overfluct_dot = [0, 0, 0, 0, 0]        
        
        #2. finding info about the fingers
        #A) DOT
        dot_list[0] = self.find_dot(0)
        
        #B) BEND
        for i in range(1,4):
            ben_list[i] = self.find_ben(i)
        
        
        #C) Aligned
        self.det_aligned(0, dot_list)
        
        #D) Opened
        for i in range(1,4):
            self.det_opened(i, ben_list)
        
        print(f"a: {self.aligned[0]}")
        for i, o in enumerate(self.opened[1:]):
            print(f"o {i+1}: {o}")
        
        print("--------------------------------")
        #2.5 check
        '''
        
        print("----------------------------------------------------------------")
        
        
        print("----------------------------------------------------------------")
        '''
        '''
        #3. Checking hold fluctuations --------------------------------
        
        #A) scale_hold dot fluctuation ---------------
        if self.conditions["scale_hold"]:
            #i. thumb dot
            overfluct_dot[0] = self.overfluct_dot(0,dot_list)
            
            if overfluct_dot[0]:
                self.conditions["scale_hold"] = False
                print("OVER | SCALE")
                return
                
        #B) All other bend fluctuations
        elif self.conditions["RMB_hold"] or self.conditions["LMB_hold"] or self.conditions["LMB_hold"]:
            #are fingers overfluctuated?
            for i, ben_ove in enumerate(ben_list):
                overfluct_ben[i] = self.overfluct_ben(0, ben_ove)
                
                if overfluct_ben[i]:
                    self.conditions["RMB_hold"] = False
                    self.conditions["LMB_hold"] = False
                    self.conditions["scale_hold"] = False
                    print("OVER | GESTUE")
                    return
        '''
        #4. Check gestues --------------------------------
        self.prev_ben_list = ben_list
        self.prev_dot_list = dot_list
        
        #A) RMB GESTUE
        self.ges_rmb(dot_list,ben_list)
        
        #if the rmb was not found
        if not self.conditions["RMB_hold"]:
            
            self.ges_lmb(dot_list,ben_list)
            
            #if the lmb was not found
            if not self.conditions["LMB_hold"]:
                
                print("NOTHING")
                return
            
            print("NEW | LMB")
            return
        
        print("NEW | RMB")
        
    
    def load_config(self):
        
        try:
            with open("config.json", "r") as f:
                j = json.load(f)
        except FileNotFoundError:
            logging.info("config.json file not found. Using default configuration.")
            return {}
        
        self.limits_ben = j["limits_ben"]
        self.limits_dot = j["limits_dot"]
        
        self.dot_90 = j.get("dot_90")
        self.dot_0 = j.get("dot_0")
        
        
'''
    def det_gestue(self):
        #checking whether there is already a gestue
        if self.shared_data["hand_is_visible"] == False:
            pass
        if self.conditions["scale_hold"] == True:
            pass
        elif self.conditions["RMB_hold"] == True:
            pass
        elif self.conditions["LMB_hold"] == True:
            pass
        
        #checking the possible gestues
        
        
        self.liniarity[0] = self.find_dot(2,4,5,8)
        self.liniarity[1] = self.find_dot(9,12,5,8)
        self.liniarity[2] = self.find_dot(13,16,5,8)
        self.liniarity[3] = self.find_dot(17,20,5,8)
        
        for i, lin in enumerate(self.liniarity):
            self.liniarity[i] = self.extremizing(lin)
            
    def extremizing(self, dot):
        if dot < self.dot_90:
            return 0
        if dot > self.dot_0:
            return 1
        else:
            return dot
    '''