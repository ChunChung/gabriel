import numpy as np
# DEBUG 1: on 
#       2: off
DEBUG = 1


# Our detects color base on BGR model
# http://www.rapidtables.com/web/color/RGB_Color.htm
# COLORS -> 0: BLACK, 1: WHITE, 2:BROWN
COLOR_BLACK = np.uint8([[[0,0,0]]])
COLOR_WHITE = np.uint8([[[255,255,255]]])   
COLOR_BRWORN = np.uint8([[[39,40,91]]])

COLORS = [COLOR_BLACK, COLOR_WHITE, COLOR_BRWORN]
