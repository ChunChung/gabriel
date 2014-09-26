import numpy as np
# DEBUG 1: on 
#       2: off
DEBUG = 1


# Our detects color base on BGR model
# http://www.rapidtables.com/web/color/RGB_Color.htm
# COLORS -> 0: BLACK, 1: WHITE, 2:BROWN
COLOR_BLACK = np.uint8([[[18,9,5]]])
COLOR_WHITE = np.uint8([[[255,255,255]]])   
COLOR_BRWORN = np.uint8([[[35,39,88]]])
COLOR_BLUE = np.uint8([[[255,0,0]]])

COLORS = [COLOR_BLACK, COLOR_WHITE, COLOR_BRWORN]

COLORS_BOUND = [20, 10, 10]
