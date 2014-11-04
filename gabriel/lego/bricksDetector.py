import Image
import cv
import cv2 
import numpy as np
import os
import sys 
import math
import config
import debug
import mosaicHandler

if os.path.isdir("../gabriel") is True:
    sys.path.insert(0, "..")

def main(img, region):
    if config.DEBUG:
        e1 = cv2.getTickCount()
        cv2.imwrite("backup.jpg",img)

    orig_img = img

    img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    cv2.imshow("Transform_Plate", orig_img)

    resize_img = cv2.resize(img, dsize=(config.PLATE_SIZE,config.PLATE_SIZE), interpolation=cv2.INTER_CUBIC)
    resize_img = cv2.cvtColor(resize_img, cv2.COLOR_HSV2BGR)

    res_img = detectBricks_v2(resize_img)

    if config.DEBUG:
        cv2.imshow("Detected_Bricks", res_img)

    plate_bricks = setBricks(res_img)

    #for i in range(0, config.PLATE_SIZE):
    #    for j in range(0, config.PLATE_SIZE):
    #        print str(plate_bricks[i][j]).zfill(2), 
    #    print ""

    mosaic_result = mosaicHandler.getRegion(0)
    result_bricks = compareResult(plate_bricks, mosaic_result, 0)

    cv2.waitKey(0)

    return result_bricks
    #print result_bricks


    #if config.DEBUG:
    #    e2 = cv2.getTickCount()
    #    time = (e2 - e1)/ cv2.getTickFrequency()
    #    print 'processing time: ', time
    #    cv2.imshow('orig', orig_img)
    #    cv2.imshow('32_32_orig', resize_img)
    #    cv2.imshow('32_32_after', res_img)
    #    cv2.waitKey(0)
    #return 


# blue:
#[255,0,0]
#[120, 255, 255]
#[100-140, >90, 0-255]
#

# black
# [0 - 180, 0-80, 0-50]
# grey
# [0 - 180, 0-80, 50-90]
# white
# [0 - 180, 0-80, 90-255]

def compareResult(plate, mosaic, region):
    p_size = config.PLATE_SIZE/2                                                
    bricks = mosaic                        
    #print plate
    #print mosaic
    if region == 0:                                                         
        for i in range(0,p_size):                                                   
            for j in range(0, p_size):                                              
                if plate[i][j] == mosaic[i][j]:
                    if bricks[i][j] < 7 and plate[i][j] != 7 :
                        bricks[i][j] = bricks[i][j] + 6
                else:
                    if mosaic[i][j] != 7:
                        if plate[i][j] != 7:
                            bricks[i][j] = 13
    return bricks                                                               


def detectBricks(img):
    # COLORS -> 0: BLACK, 1: WHITE, 2:BROWN
    colors_num = len(config.COLORS)
    rows, cols, channels = img.shape
    panel = np.empty((rows,cols,colors_num))

    res_img = np.empty((config.PLATE_SIZE, config.PLATE_SIZE, 3), dtype=np.uint8)
    #cv2.imwrite("detecBricks.jpeg",img)
    for colors_idx in range(colors_num):
        color = config.COLORS[colors_idx]
        if config.DEBUG:
            print "detect color:", color
        img_lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
        color_lab = cv2.cvtColor(color, cv2.COLOR_BGR2LAB)
        
        for i in range(0,rows):
            for j in range(0,cols):
                panel[i][j][colors_idx] = int(delta_e_cie2000(color_lab[0][0], img_lab[i][j]))

    for i in range(0,rows):
        for j in range(0,cols):
            panel_idx = panel[i][j].argmin()
            if panel[i][j][panel_idx] <= config.COLORS_BOUND[panel_idx]:
                res_img[i][j] = config.COLORS[panel_idx]
            else:
                res_img[i][j] = config.COLOR_BLUE

    if config.DEBUG:
        print "color difference====="
        for i in range(0,rows):
            for j in range(0,cols):
                panel_idx = panel[i][j].argmin()
                print str(int(panel[i][j][panel_idx])).zfill(2),
            print ""
    return res_img

def setBricks(plate_img):
    p_size = config.PLATE_SIZE                                                
    bricks = [[1]*p_size for x in range(p_size)]                                
                                                                                
    for i in range(0,config.PLATE_SIZE):                                                   
        for j in range(0, config.PLATE_SIZE):                                              
            if np.array_equal(plate_img[i][j], config.COLOR_BLUE[0][0]):   
                bricks[i][j] = 7                                        
            elif np.array_equal(plate_img[i][j], config.COLOR_BLACK[0][0]):
                bricks[i][j] = 2                                        
            elif np.array_equal(plate_img[i][j], config.COLOR_WHITE[0][0]):
                bricks[i][j] = 3                                        
            elif np.array_equal(plate_img[i][j], config.COLOR_GRAY[0][0]): 
                bricks[i][j] = 5                                        
            else:                                                           
                bricks[i][j] = 6                                        
    return bricks

def getPlateRegion(plate_result, region):

    p_size = config.PLATE_SIZE/2                                                
    bricks = [[1]*p_size for x in range(p_size)]                                
                                                                                
    if region_num == 0:                                                         
        for i in range(0,14):                                                   
            for j in range(0, 14):                                              
                if np.array_equal(plate_result[i][j], config.COLOR_BLUE[0][0]):   
                    bricks[i+2][j+2] = 1                                        
                elif np.array_equal(plate_result[i][j], config.COLOR_BLACK[0][0]):
                    bricks[i+2][j+2] = 2                                        
                elif np.array_equal(plate_result[i][j], config.COLOR_WHITE[0][0]):
                    bricks[i+2][j+2] = 3                                        
                elif np.array_equal(plate_result[i][j], config.COLOR_GRAY[0][0]): 
                    bricks[i+2][j+2] = 5                                        
                else:                                                           
                    bricks[i+2][j+2] = 6                                        
    return bricks
                                                                            


def detectBricks_v2(img):
    colors_num = len(config.COLORS)
    rows, cols, channels = img.shape
    panel = np.empty((rows,cols,colors_num))

    res_img = np.empty((config.PLATE_SIZE, config.PLATE_SIZE,3), dtype=np.uint8)
    #cv2.imwrite("detecBricks.jpeg",img)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # define range of blue color in HSV
    lower_black = np.array([0,0,0], dtype=np.uint8)
    upper_black = np.array([180,100,70], dtype=np.uint8)
    mask_black = cv2.inRange(hsv, lower_black, upper_black)

    lower_grey = np.array([0,0,70], dtype=np.uint8)
    upper_grey = np.array([180,100,130], dtype=np.uint8)
    mask_grey = cv2.inRange(hsv, lower_grey, upper_grey)

    lower_white = np.array([0,0,130], dtype=np.uint8)
    upper_white = np.array([180,100,255], dtype=np.uint8)
    mask_white = cv2.inRange(hsv, lower_white, upper_white)

    bricks = [[1]*config.PLATE_SIZE for x in range(config.PLATE_SIZE)]
    mosaic_img = cv2.imread(config.MOSAIC_NAME)


    for i in range(0, config.PLATE_SIZE):
        for j in range(0, config.PLATE_SIZE):
            if mask_white[i][j] == 255:
                res_img[i][j] = config.COLOR_WHITE
            elif mask_grey[i][j] == 255:
                res_img[i][j] = config.COLOR_GRAY
            elif mask_black[i][j] == 255:
                res_img[i][j] = config.COLOR_BLACK
            else:
                res_img[i][j] = config.COLOR_BLUE 

# black
# [0 - 180, 0-80, 0-50]
# grey
# [0 - 180, 0-80, 50-90]
# white
# [0 - 180, 0-80, 90-255]


    return res_img

def delta_e_cie2000(color1, color2, Kl=1, Kc=1, Kh=1):
    """
    Calculates the Delta E (CIE2000) of two colors.
    """       
    # Color 1 
    L1 = float(color1[0])
    a1 = float(color1[1])
    b1 = float(color1[2])
    # Color 2
    L2 = float(color2[0])
    a2 = float(color2[1])
    b2 = float(color2[2])
  
    avg_Lp = (L1 + L2) / 2.0
    C1 = math.sqrt(pow(a1, 2) + pow(b1, 2))
    C2 = math.sqrt(pow(a2, 2) + pow(b2, 2))
    avg_C1_C2 = (C1 + C2) / 2.0
  
    G = 0.5 * (1 - math.sqrt(pow(avg_C1_C2 , 7.0) / (pow(avg_C1_C2, 7.0) + pow(25.0, 7.0))))
  
    a1p = (1.0 + G) * a1
    a2p = (1.0 + G) * a2
    C1p = math.sqrt(pow(a1p, 2) + pow(b1, 2))
    C2p = math.sqrt(pow(a2p, 2) + pow(b2, 2))
    avg_C1p_C2p =(C1p + C2p) / 2.0
  
    if math.degrees(math.atan2(b1,a1p)) >= 0:
        h1p = math.degrees(math.atan2(b1,a1p))
    else:
        h1p = math.degrees(math.atan2(b1,a1p)) + 360
  
    if math.degrees(math.atan2(b2,a2p)) >= 0:
        h2p = math.degrees(math.atan2(b2,a2p))
    else:
        h2p = math.degrees(math.atan2(b2,a2p)) + 360
  
    if math.fabs(h1p - h2p) > 180:
        avg_Hp = (h1p + h2p + 360) / 2.0
    else:
        avg_Hp = (h1p + h2p) / 2.0
  
    T = 1 - 0.17 * math.cos(math.radians(avg_Hp - 30)) + 0.24 * math.cos(math.radians(2 * avg_Hp)) + 0.32 * math.cos(math.radians(3 * avg_Hp + 6)) - 0.2  * math.cos(math.radians(4 * avg_Hp - 63))
  
    diff_h2p_h1p = h2p - h1p
    if math.fabs(diff_h2p_h1p) <= 180:
        delta_hp = diff_h2p_h1p
    elif (math.fabs(diff_h2p_h1p) > 180) and (h2p <= h1p):
        delta_hp = diff_h2p_h1p + 360
    else:
        delta_hp = diff_h2p_h1p - 360
  
    delta_Lp = L2 - L1
    delta_Cp = C2p - C1p
    delta_Hp = 2 * math.sqrt(C2p * C1p) * math.sin(math.radians(delta_hp) / 2.0)
  
    S_L = 1 + ((0.015 * pow(avg_Lp - 50, 2)) / math.sqrt(20 + pow(avg_Lp - 50, 2.0)))
    S_C = 1 + 0.045 * avg_C1p_C2p
    S_H = 1 + 0.015 * avg_C1p_C2p * T
  
    delta_ro = 30 * math.exp(-(pow(((avg_Hp - 275) / 25), 2.0)))
    R_C = math.sqrt((pow(avg_C1p_C2p, 7.0)) / (pow(avg_C1p_C2p, 7.0) + pow(25.0, 7.0)));
    R_T = -2 * R_C * math.sin(2 * math.radians(delta_ro))
  
    delta_E = math.sqrt(pow(delta_Lp /(S_L * Kl), 2) + pow(delta_Cp /(S_C * Kc), 2) + pow(delta_Hp /(S_H * Kh), 2) + R_T * (delta_Cp /(S_C * Kc)) * (delta_Hp / (S_H * Kh)))
  
    return delta_E
  
    

if __name__ == "__main__":
    img = cv2.imread(sys.argv[1])
    main(img, 0)