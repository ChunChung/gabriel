import numpy as np
# DEBUG 1: on 
#       2: off
DEBUG = 0
RECORD = 0

# Our detects color base on BGR model
# http://www.rapidtables.com/web/color/RGB_Color.htm
# COLORS -> 0: BLACK, 1: WHITE, 2:BROWN
BLUE = 1
BLACK = 2
WHITE = 3
LIGHT_GREY = 4
DARK_GREY = 5
BROWN = 6

COLOR_BLACK = np.uint8([[[18,9,5]]])
COLOR_WHITE = np.uint8([[[252,254,253]]])   
COLOR_BROWN = np.uint8([[[35,39,88]]])
COLOR_BLUE = np.uint8([[[255,0,1]]])
COLOR_DARKGRAY = np.uint8([[[66,59,50]]])
COLOR_DARKGREEN = np.uint8([[[2,100,3]]])
COLOR_UNSURE = np.uint8([[[99,98,97]]])

# 206, 24, 26, 217, 20, 42

COLORS = [COLOR_BLACK, COLOR_WHITE, COLOR_BROWN, COLOR_DARKGRAY]

COLORS_BOUND = [20, 10, 10, 20]

MOSAIC_NAME = "mosaic.bmp"

REGIONS = ["top_left", "top_right", "bot_left", "bot_right"]

ACTIONS = ["start_new_region", "instruction", "complete"]

MOSAIC_SIZE = 16 # 32 - 2*2

PLATE_SIZE = 20

TRANSFORM_SIZE = 320

LOWER_BLACK = np.array([0, 0, 0], dtype=np.uint8)        
UPPER_BLACK = np.array([180, 255, 50], dtype=np.uint8)     
                                                                                 
LOWER_DARK_GRAY = np.array([80, 30, 45], dtype=np.uint8)      
UPPER_DARK_GRAY = np.array([120, 130, 100], dtype=np.uint8)   
                                                                                 
LOWER_BROWN = np.array([0, 0, 40], dtype=np.uint8)     
UPPER_BROWN = np.array([40, 160, 120], dtype=np.uint8)  
                                                                                 
LOWER_BROWN2 = np.array([130, 60, 40], dtype=np.uint8)                           
UPPER_BROWN2 = np.array([180, 110, 60], dtype=np.uint8)                          
                                                                                 
LOWER_WHITE = np.array([0, 0, 120], dtype=np.uint8)        
UPPER_WHITE = np.array([180, 45, 255], dtype=np.uint8)     

LOWER_BLUE = np.array([100, 90, 45], dtype=np.uint8)        
UPPER_BLUE = np.array([140, 255, 255], dtype=np.uint8)     

THRESHOLD = 60

#BLUE = 1
#BLACK = 2
#WHITE = 3
#LIGHT_GREY = 4
#DARK_GREY = 5
#BROWN = 6


Task2 = np.array([[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                  [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                  [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                  [1,1,1,3,3,3,3,3,3,1,1,1,1,3,3,3,1,1,1,1],
                  [1,1,1,3,3,3,3,3,3,1,1,5,5,2,6,5,1,1,1,1],
                  [1,1,3,3,1,1,1,1,1,1,1,5,5,1,1,5,3,1,1,1],
                  [1,1,3,3,1,1,1,1,1,1,1,2,2,1,1,1,6,6,1,1],
                  [1,1,5,5,1,1,1,1,1,1,1,2,2,1,1,1,6,6,1,1],
                  [1,1,5,5,1,1,1,1,1,1,1,2,2,1,1,1,6,6,1,1],
                  [1,1,1,2,2,2,2,1,1,1,1,2,2,1,1,1,6,6,1,1],
                  [1,1,1,2,2,2,2,6,6,1,1,2,2,1,1,1,5,5,1,1],
                  [1,1,1,1,1,1,1,6,6,1,1,2,2,1,1,1,5,5,1,1],
                  [1,1,1,1,1,1,1,6,6,1,1,2,2,3,3,3,3,1,1,1],
                  [1,1,1,1,1,1,1,6,6,1,1,2,2,3,3,3,3,1,1,1],
                  [1,1,5,5,5,5,5,5,1,1,1,1,1,1,1,1,1,1,1,1],
                  [1,1,5,5,5,5,5,5,1,2,2,1,1,1,1,1,1,1,1,1],
                  [1,1,1,1,1,1,1,1,1,1,2,1,1,1,1,1,1,1,1,1],
                  [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                  [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                  [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]],dtype=np.uint8)
