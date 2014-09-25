import sys
import cv2
import numpy as np

import config
import debug
from tool import euc_dist

def perspective_transform(img, plate_mask): #return perspective transform version of img
                                            #img: original image
                                            #plate_mask : plate mask image    
    print '----- start ', sys.modules[__name__], '-----'
    # find plate's coners by using plate's mask
    rows,cols = plate_mask.shape
    print 'mask size: ', cols, 'x', rows    
    #Input image should be a binary image, so apply threshold or use canny edge detection before finding applying hough transform
    #edges = cv2.Canny(plate_mask, 100, 120, apertureSize = 3)
    #ret,thresh = cv2.threshold(img,127,255,0)
    contours,hierarchy = cv2.findContours(plate_mask, 1, 2)
    edges = np.empty((rows, cols), dtype=np.uint8)
    edges[:, :] = 0
    for cnt in contours:
        hull = cv2.convexHull(cnt)
        cv2.drawContours(edges, [hull], 0, (255), 1)
    if config.DEBUG == 1:
        debug.imshow('convex hull', edges)
    #In experiments the probabilistic Hough transform yields less line segments but with higher accuracy than the standard Hough transform.
    #threshold :  Accumulator threshold parameter. Only those lines are returned that get enough votes.
    #minLineLength : Minimum line length. Line segments shorter than that are rejected.
    #maxLineGap : Maximum allowed gap between points on the same line to link them.
    lines = cv2.HoughLinesP(edges, 1, np.pi/180, threshold = cols/4,
        minLineLength = cols/4, maxLineGap = 10)
    if lines is None:    
	print 'Abort: cannot find lines'
    	return None
    else:
	lines = lines[0]
	
        # get four major lines
        new_lines = list()
        for line in lines:
            flag = True
            for new_line in new_lines:
                if is_line_seg_close(line, new_line):
                    flag = False
                    break
            if flag:
                new_lines.append(list(line))
        
        lines = new_lines

        print 'find ', len(lines), ' lines'
	if len(lines) != 4:
            print 'Abort: cannot find exactly 4 lines'
	    return None

    #find intersections between lines
    corners = []
    for i in range(0, len(lines)):
        for j in range(i+1,len(lines)):
            (x, y) = compute_interset(lines[i], lines[j])
            if x >= 0 and x < cols and y >= 0 and y < rows:
                corners.append((int(x), int(y)))
    
    if len(corners) == 0:
        print 'Abort: cannot find intersections'
    	return None

    
    #Check if the approximate polygonal curve has 4 vertices
    approx = cv2.approxPolyDP(np.array(corners), cv2.arcLength(np.array(corners),True) * 0.02, True)
    
    if len(approx) != 4:
        print "Abort: cannot find a approx square."     
        return None    
    else:
        if config.DEBUG == 1:
            for line in lines:
                cv2.line(edges,(line[0],line[1]),(line[2],line[3]),255,3)
	    for corner in corners:
	        cv2.circle(edges, corner, 10, 255, -1)
            debug.imshow('four corners', edges)
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
	src_corners = np.float32([ul, ur, bl, br])
        dst_corners = np.float32([[0,0],[320,0],[0,320],[320,320]])
        print 'perspective transform: \n', src_corners, ' --> ', dst_corners
        M = cv2.getPerspectiveTransform(src_corners,dst_corners)
        #TODO: find size from dst_corners   
        dst = cv2.warpPerspective(img,M,(320,320))
        if config.DEBUG == 1:
            debug.imshow('perspective', dst)
	return dst
    
    
def is_line_seg_close(line1, line2):
    pt1_1 = np.array(line1[0 : 2])
    pt1_2 = np.array(line1[2 : 4])
    pt2_1 = np.array(line2[0 : 2])
    pt2_2 = np.array(line2[2 : 4])
    l1 = euc_dist(pt1_1, pt1_2)
    l2 = euc_dist(pt2_1, pt2_2)
    v1 = pt1_2 - pt1_1
    v2 = pt2_1 - pt1_1
    v3 = pt2_2 - pt1_1
    area1 = np.absolute(np.cross(v1, v2))
    area2 = np.absolute(np.cross(v1, v3))
    if max(area1, area2) < l1 * l2 / 3:
        return True
    else:
        return False    
    

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

