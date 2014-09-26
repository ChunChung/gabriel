import Image
import cv
import cv2 
import numpy as np
import os
import sys 
import math
import config

if os.path.isdir("../gabriel") is True:
    sys.path.insert(0, "..")

def detectBricks(img, color_type):
    if config.DEBUG:
        e1 = cv2.getTickCount()
    orig_img = img

    img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    resize_img = cv2.resize(img, dsize=(32,32), interpolation=cv2.INTER_CUBIC)
    resize_img = cv2.cvtColor(resize_img, cv2.COLOR_HSV2BGR)

    detectColors(resize_img)

    if config.DEBUG:
        e2 = cv2.getTickCount()
        time = (e2 - e1)/ cv2.getTickFrequency()
        print 'procesmath.sing time: ', time
    cv2.imshow('orig', orig_img)
    cv2.imshow('32_32_orig', resize_img)
    cv2.waitKey(0)


def detectColors(img):
    # COLORS -> 0: BLACK, 1: WHITE, 2:BROWN

    for color in config.COLORS:
        panel = np.empty((32,32))

        if config.DEBUG:
            print "detect color:", color

        img_lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)

        color_lab = cv2.cvtColor(color, cv2.COLOR_BGR2LAB)
        

        comp = np.empty((32,32,3), dtype=np.uint8)
        comp[:, :] = color_lab
        dst = (img_lab - comp) 

        rows, cols, channels = img.shape

        for i in range(0,rows):
            for j in range(0,cols):
                print int(delta_e_cie2000(comp[i][j], img_lab[i][j])),
            print ""

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
  
    


if config.DEBUG:
    img = cv2.imread('result.jpg')
    detectBricks(img,1)
