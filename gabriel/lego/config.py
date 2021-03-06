import numpy as np
# DEBUG 1: on 
#       2: off
DEBUG = 1
RECORD = 2

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
UPPER_BLACK = np.array([180, 60, 50], dtype=np.uint8)     
                                                                                 
LOWER_BLACK2 = np.array([0, 0, 0], dtype=np.uint8)        
UPPER_BLACK2 = np.array([180, 130, 30], dtype=np.uint8)     

LOWER_BLACK3 = np.array([90, 100, 0], dtype=np.uint8)        
UPPER_BLACK3 = np.array([140, 255, 40], dtype=np.uint8)     

LOWER_BLACK4 = np.array([90, 0, 80], dtype=np.uint8)        
UPPER_BLACK4 = np.array([140, 40, 150], dtype=np.uint8)     

LOWER_DARK_GRAY = np.array([0, 0, 40], dtype=np.uint8)      
UPPER_DARK_GRAY = np.array([90, 130, 100], dtype=np.uint8)   
                                                                                 
LOWER_DARK_GRAY2 = np.array([90, 0, 0], dtype=np.uint8)      
UPPER_DARK_GRAY2 = np.array([140, 130, 90], dtype=np.uint8)   

LOWER_DARK_GRAY3 = np.array([140, 0, 40], dtype=np.uint8)      
UPPER_DARK_GRAY3 = np.array([180, 130, 100], dtype=np.uint8)   

LOWER_DARK_GRAY4 = np.array([0, 0, 0], dtype=np.uint8)      
UPPER_DARK_GRAY4 = np.array([180, 40, 50], dtype=np.uint8)   

LOWER_WHITE = np.array([0, 0, 120], dtype=np.uint8)        
UPPER_WHITE = np.array([100, 80, 255], dtype=np.uint8)     

LOWER_WHITE2 = np.array([100, 0, 160], dtype=np.uint8)        
UPPER_WHITE2 = np.array([140, 70, 255], dtype=np.uint8)     

LOWER_WHITE3 = np.array([140, 0, 120], dtype=np.uint8)        
UPPER_WHITE3 = np.array([180, 60, 255], dtype=np.uint8)     

LOWER_BLUE = np.array([100, 80, 40], dtype=np.uint8)        
UPPER_BLUE = np.array([140, 255, 255], dtype=np.uint8)     

LOWER_BLUE2 = np.array([100, 0, 0], dtype=np.uint8)        
UPPER_BLUE2 = np.array([140, 255, 255], dtype=np.uint8)     

LOWER_BROWN = np.array([0, 50, 40], dtype=np.uint8)     
UPPER_BROWN = np.array([30, 255, 120], dtype=np.uint8)  
                                                                                 
LOWER_BROWN2 = np.array([150, 50, 40], dtype=np.uint8)                           
UPPER_BROWN2 = np.array([180, 255, 120], dtype=np.uint8)                          
                                                                                 
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

MOSAIC_DEFAULT = np.empty((20, 20), dtype=np.int32)
MOSAIC_DEFAULT[:] = BLUE

