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
import time
from scipy.stats import itemfreq

if os.path.isdir("../gabriel") is True:
    sys.path.insert(0, "..")

def main(img):
    print '----- start ', sys.modules[__name__], '-----'

    #while(1):
    if config.DEBUG:
        e1 = cv2.getTickCount()

    cv2.namedWindow("Detected_Bricks_w/o_Resize")

    orig_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    #resize_img = cv2.resize(orig_img, dsize=(config.PLATE_SIZE,config.PLATE_SIZE), interpolation=cv2.INTER_CUBIC)
    #resize_img = cv2.cvtColor(resize_img, cv2.COLOR_HSV2BGR)
    #res_img = detectBricks_v2(resize_img)
    res_window_img = detectBricks_window(orig_img)
    #resize_window_img = cv2.resize(res_window_img, dsize=(config.PLATE_SIZE,config.PLATE_SIZE))

    #plate_bricks_window = setBricks(res_window_img, config.PLATE_SIZE*10)
    final_img = setColors(res_window_img)

    #if config.DEBUG:
    cv2.imshow("Transformed_Plate", img)
        #enlargeImg = showEnlargeImg(res_img, 10)
        #cv2.imshow("Detected_Bricks", enlargeImg)
    cv2.imshow("Detected_Bricks_w/o_Resize", res_window_img)
        #cv2.imshow("Detected_Bricks_w/o_Resize_Window", showEnlargeImg(resize_window_img, 10))
    cv2.imshow("Detected_Bricks_final", showEnlargeImg(final_img, 10))
        #cv2.imshow("final", final_img)


    plate_bricks = setBricks(final_img, config.PLATE_SIZE)
    #mosaic_result = mosaicHandler.getRegion(0)
    #result_bricks = compareResult(plate_bricks, mosaic_result, 0)



    return plate_bricks

def setColors(input_img):
    res_img = np.empty((config.PLATE_SIZE, config.PLATE_SIZE, 3), dtype=np.uint8)
    for i in range(config.PLATE_SIZE):
        for j in range(config.PLATE_SIZE):
            partial_array = input_img[i*16:((i+1)*16), j*16:((j+1)*16)]
            freq_ = itemfreq(partial_array)

            freq_ = sorted(freq_, key=lambda x: x[1], reverse=True)
            #print len(freq_)
            color_count = len(freq_)/3

            colorScore = np.zeros((color_count, 2))

            for x in range(0, color_count):
                colorScore[x][0] = freq_[x*3][0]
                colorScore[x][1] = freq_[x*3][1]

            max_idx = -1
            max_value = 0
            for x in range(0, color_count):
                if colorScore[x][0] == 2 or colorScore[x][0] == 100 or colorScore[x][0] == 3:
                    if colorScore[x][1] < 50:
                        max_value = 0
                        for y in range(0, color_count):
                            if y != x:
                                if colorScore[y][0] == 255 or colorScore[y][0] == 0 or colorScore[y][0] == 1: 
                                    colorScore[y][1] = colorScore[y][1]
                                else:
                                    colorScore[y][1] = colorScore[x][1] * 0.5 + colorScore[y][1]  

                                if colorScore[y][1] > max_value:
                                    max_value = colorScore[y][1]
                                    max_idx = y
                        break
                else:
                    if colorScore[x][1] > max_value:
                        max_value = colorScore[x][1]
                        max_idx = x

            #print colorScore[max_idx][0], max_value

            if max_idx != -1 and max_value > 60:
                if colorScore[max_idx][0] == 18 or colorScore[max_idx][0] == 9 or colorScore[max_idx][0] == 5:
                    res_img[i][j] = config.COLOR_BLACK
                elif colorScore[max_idx][0] == 252 or colorScore[max_idx][0] == 254 or colorScore[max_idx][0] == 253:
                    res_img[i][j] = config.COLOR_WHITE
                elif colorScore[max_idx][0] == 35 or colorScore[max_idx][0] == 39 or colorScore[max_idx][0] == 88:
                    res_img[i][j] = config.COLOR_BROWN
                elif colorScore[max_idx][0] == 66 or colorScore[max_idx][0] == 59 or colorScore[max_idx][0] == 50:
                    res_img[i][j] = config.COLOR_DARKGRAY
                else:
                    res_img[i][j] = config.COLOR_BLUE
            else:
                res_img[i][j] = config.COLOR_BLUE



            #if freq_[0][1] > 1:
            #    if freq_[0][0] == 18 or freq_[0][0] == 9 or freq_[0][0] == 5:
            #        res_img[i][j] = config.COLOR_BLACK
            #    elif freq_[0][0] == 252 or freq_[0][0] == 254 or freq_[0][0] == 253:
            #        res_img[i][j] = config.COLOR_WHITE
            #    elif freq_[0][0] == 35 or freq_[0][0] == 39 or freq_[0][0] == 88:
            #        res_img[i][j] = config.COLOR_BROWN
            #    elif freq_[0][0] == 66 or freq_[0][0] == 59 or freq_[0][0] == 50:
            #        res_img[i][j] = config.COLOR_DARKGRAY
            #    else:
            #        if freq_ [0][1] == 100:
            #            res_img[i][j] = config.COLOR_BLUE
            #        else:
            #            if freq_[3][1] > 40:
            #                if freq_[3][0] == 18 or freq_[3][0] == 9 or freq_[3][0] == 5:
            #                    res_img[i][j] = config.COLOR_BLACK
            #                elif freq_[3][0] == 252 or freq_[3][0] == 254 or freq_[3][0] == 253:
            #                    res_img[i][j] = config.COLOR_WHITE
            #                elif freq_[3][0] == 35 or freq_[3][0] == 39 or freq_[3][0] == 88:
            #                    res_img[i][j] = config.COLOR_BROWN
            #                elif freq_[3][0] == 66 or freq_[3][0] == 59 or freq_[3][0] == 50:
            #                    res_img[i][j] = config.COLOR_DARKGRAY
            #                else:
            #                    res_img[i][j] = config.COLOR_BLUE
            #            else:
            #                res_img[i][j] = config.COLOR_BLUE
            #else:
            #    res_img[i][j] = config.COLOR_BLUE
    return res_img

def showEnlargeImg(res_img, times):
    colors_num = len(config.COLORS)

    rows, cols, channels = res_img.shape

    result = np.empty((rows*times,cols*times, 3), dtype=np.uint8)

    for i in range(0, rows):
        for j in range(0, cols):
            for m in range(i*times, (i+1)*times):
                for n in range(j*times, (j+1)*times):
                    result[m][n] = res_img[i][j]
    return result

def nothing(x):
    pass

def printHSV(resize_img,l_cols, l_rows, h_cols, h_rows):
    rows, cols, channels = img.shape
    
    for j in range(l_rows, h_rows):
        for i in range(l_cols, h_cols):
            print resize_img[i][j]

    print rows, cols

def detectBricks_window(resize_img):
    colors_num = len(config.COLORS)
    rows, cols, channels = resize_img.shape

    # Default Value
    lower_black = config.LOWER_BLACK
    upper_black = config.UPPER_BLACK

    lower_dark_gray = config.LOWER_DARK_GRAY
    upper_dark_gray = config.UPPER_DARK_GRAY

    lower_brown = config.LOWER_BROWN
    upper_brown = config.UPPER_BROWN

    lower_brown2 = config.LOWER_BROWN2
    upper_brown2 = config.UPPER_BROWN2

    lower_white = config.LOWER_WHITE
    upper_white = config.UPPER_WHITE

    if config.DEBUG == 2:
        cv2.createTrackbar('b_lower_h','Detected_Bricks_w/o_Resize',config.LOWER_BLACK[0],180,nothing)
        cv2.createTrackbar('b_lower_s','Detected_Bricks_w/o_Resize',config.LOWER_BLACK[1],255,nothing)
        cv2.createTrackbar('b_lower_v','Detected_Bricks_w/o_Resize',config.LOWER_BLACK[2],255,nothing)
        # create trackbars fb_or color change
        cv2.createTrackbar('b_higher_h','Detected_Bricks_w/o_Resize',config.UPPER_BLACK[0],180,nothing)
        cv2.createTrackbar('b_higher_s','Detected_Bricks_w/o_Resize',config.UPPER_BLACK[1],255,nothing)
        cv2.createTrackbar('b_higher_v','Detected_Bricks_w/o_Resize',config.UPPER_BLACK[2],255,nothing)
        b_lower_h = cv2.getTrackbarPos('b_lower_h', 'Detected_Bricks_w/o_Resize')
        b_lower_s = cv2.getTrackbarPos('b_lower_s', 'Detected_Bricks_w/o_Resize')
        b_lower_v = cv2.getTrackbarPos('b_lower_v', 'Detected_Bricks_w/o_Resize')
        b_higher_h = cv2.getTrackbarPos('b_higher_h', 'Detected_Bricks_w/o_Resize')
        b_higher_s = cv2.getTrackbarPos('b_higher_s', 'Detected_Bricks_w/o_Resize')
        b_higher_v = cv2.getTrackbarPos('b_higher_v', 'Detected_Bricks_w/o_Resize')

        cv2.createTrackbar('dg_lower_h','Detected_Bricks_w/o_Resize',config.LOWER_DARK_GRAY[0],180,nothing)
        cv2.createTrackbar('dg_lower_s','Detected_Bricks_w/o_Resize',config.LOWER_DARK_GRAY[1],255,nothing)
        cv2.createTrackbar('dg_lower_v','Detected_Bricks_w/o_Resize',config.LOWER_DARK_GRAY[2],255,nothing)
        # create trackbars fb_or color change
        cv2.createTrackbar('dg_higher_h','Detected_Bricks_w/o_Resize',config.UPPER_DARK_GRAY[0],180,nothing)
        cv2.createTrackbar('dg_higher_s','Detected_Bricks_w/o_Resize',config.UPPER_DARK_GRAY[1],255,nothing)
        cv2.createTrackbar('dg_higher_v','Detected_Bricks_w/o_Resize',config.UPPER_DARK_GRAY[2],255,nothing)
        dg_lower_h = cv2.getTrackbarPos('dg_lower_h', 'Detected_Bricks_w/o_Resize')
        dg_lower_s = cv2.getTrackbarPos('dg_lower_s', 'Detected_Bricks_w/o_Resize')
        dg_lower_v = cv2.getTrackbarPos('dg_lower_v', 'Detected_Bricks_w/o_Resize')
        dg_higher_h = cv2.getTrackbarPos('dg_higher_h', 'Detected_Bricks_w/o_Resize')
        dg_higher_s = cv2.getTrackbarPos('dg_higher_s', 'Detected_Bricks_w/o_Resize')
        dg_higher_v = cv2.getTrackbarPos('dg_higher_v', 'Detected_Bricks_w/o_Resize')

        cv2.createTrackbar('br_lower_h','Detected_Bricks_w/o_Resize',config.LOWER_BROWN[0],180,nothing)
        cv2.createTrackbar('br_lower_s','Detected_Bricks_w/o_Resize',config.LOWER_BROWN[1],255,nothing)
        cv2.createTrackbar('br_lower_v','Detected_Bricks_w/o_Resize',config.LOWER_BROWN[2],255,nothing)
        # create trackbars fb_or color change
        cv2.createTrackbar('br_higher_h','Detected_Bricks_w/o_Resize',config.UPPER_BROWN[0],180,nothing)
        cv2.createTrackbar('br_higher_s','Detected_Bricks_w/o_Resize',config.UPPER_BROWN[1],255,nothing)
        cv2.createTrackbar('br_higher_v','Detected_Bricks_w/o_Resize',config.UPPER_BROWN[2],255,nothing)
        br_lower_h = cv2.getTrackbarPos('br_lower_h', 'Detected_Bricks_w/o_Resize')
        br_lower_s = cv2.getTrackbarPos('br_lower_s', 'Detected_Bricks_w/o_Resize')
        br_lower_v = cv2.getTrackbarPos('br_lower_v', 'Detected_Bricks_w/o_Resize')
        br_higher_h = cv2.getTrackbarPos('br_higher_h', 'Detected_Bricks_w/o_Resize')
        br_higher_s = cv2.getTrackbarPos('br_higher_s', 'Detected_Bricks_w/o_Resize')
        br_higher_v = cv2.getTrackbarPos('br_higher_v', 'Detected_Bricks_w/o_Resize')

        cv2.createTrackbar('w_lower_h','Detected_Bricks_w/o_Resize',config.LOWER_WHITE[0],180,nothing)
        cv2.createTrackbar('w_lower_s','Detected_Bricks_w/o_Resize',config.LOWER_WHITE[1],255,nothing)
        cv2.createTrackbar('w_lower_v','Detected_Bricks_w/o_Resize',config.LOWER_WHITE[2],255,nothing)
        # create trackbars fb_or color change
        cv2.createTrackbar('w_higher_h','Detected_Bricks_w/o_Resize',config.UPPER_WHITE[0],180,nothing)
        cv2.createTrackbar('w_higher_s','Detected_Bricks_w/o_Resize',config.UPPER_WHITE[1],255,nothing)
        cv2.createTrackbar('w_higher_v','Detected_Bricks_w/o_Resize',config.UPPER_WHITE[2],255,nothing)
        w_lower_h = cv2.getTrackbarPos('w_lower_h', 'Detected_Bricks_w/o_Resize')
        w_lower_s = cv2.getTrackbarPos('w_lower_s', 'Detected_Bricks_w/o_Resize')
        w_lower_v = cv2.getTrackbarPos('w_lower_v', 'Detected_Bricks_w/o_Resize')
        w_higher_h = cv2.getTrackbarPos('w_higher_h', 'Detected_Bricks_w/o_Resize')
        w_higher_s = cv2.getTrackbarPos('w_higher_s', 'Detected_Bricks_w/o_Resize')
        w_higher_v = cv2.getTrackbarPos('w_higher_v', 'Detected_Bricks_w/o_Resize')
        

        print "b_lower", b_lower_h, b_lower_s, b_lower_v, "b_higher", b_higher_h, b_higher_s, b_higher_v
        print "dg_lower", dg_lower_h, dg_lower_s, dg_lower_v, "dg_higher", dg_higher_h, dg_higher_s, dg_higher_v
        print "br_lower", br_lower_h, br_lower_s, br_lower_v, "br_higher", br_higher_h, br_higher_s, br_higher_v
        print "w_lower", w_lower_h, w_lower_s, w_lower_v, "w_higher", w_higher_h, w_higher_s, w_higher_v

        lower_black = np.array([b_lower_h, b_lower_s, b_lower_v], dtype=np.uint8)
        upper_black = np.array([b_higher_h, b_higher_s, b_higher_v], dtype=np.uint8)

        lower_dark_gray = np.array([dg_lower_h, dg_lower_s, dg_lower_v], dtype=np.uint8)
        upper_dark_gray = np.array([dg_higher_h, dg_higher_s, dg_higher_v], dtype=np.uint8)

        lower_brown = np.array([br_lower_h, br_lower_s, br_lower_v], dtype=np.uint8)
        upper_brown = np.array([br_higher_h, br_higher_s, br_higher_v], dtype=np.uint8)

        lower_brown2 = np.array([130, 60, 40], dtype=np.uint8)
        upper_brown2 = np.array([180, 110, 60], dtype=np.uint8)

        lower_white = np.array([w_lower_h, w_lower_s, w_lower_v], dtype=np.uint8)
        upper_white = np.array([w_higher_h, w_higher_s, w_higher_v], dtype=np.uint8)


    res_img = np.empty((config.TRANSFORM_SIZE, config.TRANSFORM_SIZE,3), dtype=np.uint8)
    hsv = resize_img
    #hsv = cv2.cvtColor(resize_img, cv2.COLOR_BGR2HSV)

    mask_dark_gray = cv2.inRange(hsv, lower_dark_gray, upper_dark_gray)
    mask_black = cv2.inRange(hsv, lower_black, upper_black)
    mask_brown = cv2.inRange(hsv, lower_brown, upper_brown)
    mask_brown2 = cv2.inRange(hsv, lower_brown2, upper_brown2)
    mask_white = cv2.inRange(hsv, lower_white, upper_white)
    mask_blue = cv2.inRange(hsv, config.LOWER_BLUE, config.UPPER_BLUE)

    #bricks = [[1]*config.TRANSFORM_SIZE for x in range(config.TRANSFORM_SIZE)]

    for i in range(0, config.TRANSFORM_SIZE):
        for j in range(0, config.TRANSFORM_SIZE):
            if mask_blue[i][j] == 255:
                res_img[i][j] = config.COLOR_BLUE 
            elif mask_white[i][j] == 255:
                res_img[i][j] = config.COLOR_WHITE
            elif mask_dark_gray[i][j] == 255:
                res_img[i][j] = config.COLOR_DARKGRAY
            elif mask_brown[i][j] == 255:
                res_img[i][j] = config.COLOR_BROWN
            elif mask_brown2[i][j] == 255:
                res_img[i][j] = config.COLOR_BROWN
            elif mask_black[i][j] == 255:
                res_img[i][j] = config.COLOR_BLACK
            else:
                res_img[i][j] = config.COLOR_DARKGREEN 


    #svm_params = dict( kernel_type = cv2.SVM_LINEAR, svm_type = cv2.SVM_C_SVC, C=2.67, gamma=5.383 )
    #float_resize_img = np.empty((config.TRANSFORM_SIZE, config.TRANSFORM_SIZE,3), dtype=np.float32)
    #float_resize_img[:] = resize_img[:]

    #svm = cv2.SVM()
    #svm.train(float_resize_img, res_img) 

    #cv2.imshow("test", res_img)
    #cv2.waitKey(0)


    return res_img


    

# black
# [0 - 180, 0-80, 0-50]
# gray
# [0 - 180, 0-80, 50-90]
# white
# [0 - 180, 0-80, 90-255]


# blue:
#[255,0,0]
#[120, 255, 255]
#[100-140, >90, 0-255]
#

# black
# [0 - 180, 0-80, 0-50]
# gray
# [0 - 180, 0-80, 50-90]
# white
# [0 - 180, 0-80, 90-255]

def compareResult(plate, mosaic, region):
    p_size = config.PLATE_SIZE                                                
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

def setBricks(plate_img, p_size):
    bricks = np.empty((p_size, p_size), dtype=np.int32)                              
                                                                                
    for i in range(0, p_size):                                                   
        for j in range(0, p_size):                                              
            if np.array_equal(plate_img[i][j], config.COLOR_BLUE[0][0]):   
                bricks[i][j] = 1
            elif np.array_equal(plate_img[i][j], config.COLOR_BLACK[0][0]):
                bricks[i][j] = 2                                        
            elif np.array_equal(plate_img[i][j], config.COLOR_WHITE[0][0]):
                bricks[i][j] = 3                                        
            elif np.array_equal(plate_img[i][j], config.COLOR_DARKGRAY[0][0]): 
                bricks[i][j] = 5                                        
            elif np.array_equal(plate_img[i][j], config.COLOR_BROWN[0][0]): 
                bricks[i][j] = 6                                        
    return bricks

def getPlateRegion(plate_result, region):

    p_size = config.PLATE_SIZE                                                
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
                elif np.array_equal(plate_result[i][j], config.COLOR_DARKGRAY[0][0]): 
                    bricks[i+2][j+2] = 5                                        
                else:                                                           
                    bricks[i+2][j+2] = 6                                        
    return bricks

def detectBricks_v2(img):
    colors_num = len(config.COLORS)
    rows, cols, channels = img.shape

    res_img = np.empty((config.PLATE_SIZE, config.PLATE_SIZE,3), dtype=np.uint8)
    #cv2.imwrite("detecBricks.jpeg",img)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # define range of blue color in HSV
    lower_black = np.array([0,0,0], dtype=np.uint8)
    upper_black = np.array([180,100,70], dtype=np.uint8)
    mask_black = cv2.inRange(hsv, lower_black, upper_black)

    lower_gray = np.array([0,0,70], dtype=np.uint8)
    upper_gray = np.array([180,100,130], dtype=np.uint8)
    mask_gray = cv2.inRange(hsv, lower_gray, upper_gray)

    lower_white = np.array([0,0,130], dtype=np.uint8)
    upper_white = np.array([180,100,255], dtype=np.uint8)
    mask_white = cv2.inRange(hsv, lower_white, upper_white)

    bricks = [[1]*config.PLATE_SIZE for x in range(config.PLATE_SIZE)]


    for i in range(0, config.PLATE_SIZE):
        for j in range(0, config.PLATE_SIZE):
            if mask_white[i][j] == 255:
                res_img[i][j] = config.COLOR_WHITE
            elif mask_gray[i][j] == 255:
                res_img[i][j] = config.COLOR_DARKGRAY
            elif mask_black[i][j] == 255:
                res_img[i][j] = config.COLOR_BLACK
            else:
                res_img[i][j] = config.COLOR_BLUE 

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
    main(img)
