import debug
import sys
import cv2
import numpy as np


local_debug = 0

def main(frame):
    tmp_img = np.array(frame)
    hsv = cv2.cvtColor(tmp_img, cv2.COLOR_BGR2HSV)
    
    # define range of blue color in HSV
    lower_blue = np.array([100,50,50], dtype=np.uint8)
    upper_blue = np.array([130,255,255], dtype=np.uint8)
    
    # Threshold the HSV image to get only blue colors
    mask = cv2.inRange(hsv, lower_blue, upper_blue)
    
    kernel = np.ones((5,5),np.uint8)
    mask = cv2.erode (mask,kernel,iterations = 1)
    mask = cv2.dilate(mask,kernel,iterations = 1)
    mask = cv2.dilate(mask,kernel,iterations = 1)
    mask = cv2.erode (mask,kernel,iterations = 1)

    if local_debug == 1:
        debug.imshow("mask", mask)
        debug.imshow("frame", frame)
        cv2.waitKey(0)

    return mask

if __name__ == "__main__":
    img = cv2.imread(sys.argv[1])
    local_debug = 1 
    main(img)

