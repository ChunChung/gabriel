import sys
import cv2
import numpy as np

#from gabriel.lego import debug

def perspective_transform(img, plate_mask): #return perspective transform version of img
                                            #img: original image
                                            #plate_mask : plate mask image
    
    # find plate's coners by using plate's mask
    rows,cols = plate_mask.shape
    
    #Input image should be a binary image, so apply threshold or use canny edge detection before finding applying hough transform
    edges = cv2.Canny(plate_mask, 50, 150, apertureSize = 3)
    
    #In experiments the probabilistic Hough transform yields less line segments but with higher accuracy than the standard Hough transform.
    #threshold :  Accumulator threshold parameter. Only those lines are returned that get enough votes.
    #minLineLength : Minimum line length. Line segments shorter than that are rejected.
    #maxLineGap : Maximum allowed gap between points on the same line to link them.
    perimeter = 100
    lines = [] #in case it is None
    lines = cv2.HoughLinesP(edges, 1, np.pi/180, perimeter / 2,
        minLineLength = perimeter, maxLineGap = perimeter / 20)
    if lines is None:    
	print sys.modules[__name__], 'Cannot find lines'
    return None
    
    #extend lines
    for line in lines:
        v = line
        line[0] = 0
        line[1] = (float(v[1]) - v[3]) / (v[0] - v[2]) * -v[0] + v[1]
        line[2] = cols
        line[3] = (float(v[1]) - v[3]) / (v[0] - v[2]) * (cols - v[2]) + v[3]
        if lego_config.DEBUG == 1:
            cv2.line(edges,(line[0],line[1]),(line[2],line[3]),(0,0,255),2)
    
    #if lego_config.DEBUG == 1:
    #    debug.imshow('edges', edges)
    cv2.imshow('edges',edges)    
    #find intersections between lines
    corners = []
    for index, line1 in lines:
        for j in range(index+1,len(lines)):
            line2 = lines[j]
            (x, y) = compute_interset(line1, line2)
            if x >= 0 and y >= 0:
                corners.append((x, y))
    
    #Check if the approximate polygonal curve has 4 vertices
    approx = cv2.approxPolyDP(corners, cv2.arcLength(corners,True) * 0.02, True)
    
    
    if len(approx) != 4:
        print sys.modules[__name__], "Cannot find a square."     
        return None    
    else:
        #Determine top-left, bottom-left, top-right, and bottom-right corner
        dtype = [('x', float), ('y', float)]
        corners = np.array(corners, dtype = dtype)
        corners = np.sort(corners, order = 'y')
        if corners[0][0] < corners[1][0]:
            ul = corners[0]; ur = corners[1]
        else:
            ul = corners[1]; ur = corners[0]
        if corners[2][0] < corners[3][0]:
            bl = corners[2]; br = corners[3]
        else:
            bl = corners[3]; br = corners[2]
        ul = list(ul)
        ur = list(ur)
        bl = list(bl)
        br = list(br)
        
        #perspective transformation
        dst_corners = np.float32([[0,0],[320,0],[0,320],[320,320]])
        M = cv2.getPerspectiveTransform(src_corners,dst_corners)
        #TODO: find size from dst_corners   
        dst = cv2.warpPerspective(img,M,(320,320))
        #if lego_config.DEBUG == 1:
        #    debug.imshow('perspective', dst)
        cv2.imshow('perspective', dst)
	return dst
    
    
    
    

def compute_interset(a, b):
    x1 = a[0]; y1 = a[1]; x2 = a[2]; y2 = a[3]
    x3 = b[0]; y3 = b[1]; x4 = b[2]; y4 = b[3]
    d = ((float)(x1-x2) * (y3-y4)) - ((y1-y2) * (x3-x4))
    if d:
        x = ((x1*y2 - y1*x2) * (x3-x4) - (x1-x2) * (x3*y4 - y3*x4)) / d
        y = ((x1*y2 - y1*x2) * (y3-y4) - (y1-y2) * (x3*y4 - y3*x4)) / d
    else:
        x, y = (-1, -1)
    return (x, y)

