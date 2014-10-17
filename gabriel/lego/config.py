import numpy as np
# DEBUG 1: on 
#       2: off
DEBUG = 1


# Our detects color base on BGR model
# http://www.rapidtables.com/web/color/RGB_Color.htm
# COLORS -> 0: BLACK, 1: WHITE, 2:BROWN
COLOR_BLACK = np.uint8([[[18,9,5]]])
COLOR_WHITE = np.uint8([[[255,255,255]]])   
COLOR_BROWN = np.uint8([[[35,39,88]]])
COLOR_BLUE = np.uint8([[[255,0,0]]])
COLOR_GRAY = np.uint8([[[46,65,84]]])

COLORS = [COLOR_BLACK, COLOR_WHITE, COLOR_GRAY]

COLORS_BOUND = [20, 10, 10, 20]

MOSAIC_NAME = "mosaic.bmp"

REGIONS = ["top_left", "top_right", "bot_left", "bot_right"]

ACTIONS = ["start_new_region", "instruction", "complete"]

MOSAIC_SIZE = 28 # 32 - 2*2

PLATE_SIZE = 32
