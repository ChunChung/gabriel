import Image
import cv
import cv2 
import numpy as np
import os
import sys 
import math
import config
import debug
import bricksDetector
import json

if os.path.isdir("../gabriel") is True:
    sys.path.insert(0, "..")

local_debug = 0

def main(img):
    if config.DEBUG:
        e1 = cv2.getTickCount()
        print "start mosaic image handler"


    if not os.path.isfile(config.MOSAIC_NAME):
        mosaic = generateMosaic(img)
        cv2.imwrite(config.MOSAIC_NAME, mosaic)

    if config.DEBUG:
        e2 = cv2.getTickCount()
        time = (e2 - e1)/ cv2.getTickFrequency()
        print 'processing time: ', time
        print '=============================='
    return 

def getMosaicZone():
    return 1

def getRegion(region_num):
    #1: incomplete, expect empty(blue)
    #2: incomplete, expect black
    #3: incomplete, expect white
    #4: incomplete, expect light grey
    #5: incomplete, expect deep grey
    #6: incomplete, expect brown
    p_size = config.PLATE_SIZE/2
    bricks = [[7]*p_size for x in range(p_size)]

    mosaic_img = cv2.imread(config.MOSAIC_NAME)

    #if config.DEBUG == 1:
    #    debug.imshow("Mosaic", mosaic_img)
    if region_num == 0:
        for i in range(0,14):
            for j in range(0, 14):
                if np.array_equal(mosaic_img[i][j], config.COLOR_BLUE[0][0]):
                    bricks[i+2][j+2] = 7
                elif np.array_equal(mosaic_img[i][j], config.COLOR_BLACK[0][0]):
                    bricks[i+2][j+2] = 2
                elif np.array_equal(mosaic_img[i][j], config.COLOR_WHITE[0][0]):
                    bricks[i+2][j+2] = 3
                elif np.array_equal(mosaic_img[i][j], config.COLOR_GRAY[0][0]):
                    bricks[i+2][j+2] = 5
                else:
                    bricks[i+2][j+2] = 6

    return bricks


def generateMosaic(img):
    orig_img = img
    orig_img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    resize_img = cv2.resize(img, dsize=(config.MOSAIC_SIZE, config.MOSAIC_SIZE), interpolation=cv2.INTER_CUBIC)
    resize_img_gray = cv2.resize(orig_img_gray, dsize=(config.MOSAIC_SIZE, config.MOSAIC_SIZE), interpolation=cv2.INTER_CUBIC)
    #resize_img = cv2.cvtColor(resize_img, cv2.COLOR_HSV2BGR)

    #bricks_mosaic_img = bricksDetector.detectBricks(resize_img)
    gray_mosaic_img = grayMosaic(resize_img_gray)
    #result_img = combineMosaic(gray_mosaic_img, bricks_mosaic_img)

    if local_debug == 1:
        cv2.imshow('Mosaic_Orig', orig_img)
        #cv2.imshow("gray", gray_mosaic_img)
        #cv2.imshow("bricks", bricks_mosaic_img)
        #cv2.imshow("resize", resize_img)
        #cv2.imshow("resize_gray", resize_img_gray)
        cv2.imshow("Mosaic_Result", result_img)
        cv2.waitKey(0)

    return gray_mosaic_img

def grayMosaic(img):
    colors_num = len(config.COLORS)
    rows, cols = img.shape

    res_img = np.empty((config.MOSAIC_SIZE,config.MOSAIC_SIZE,3), dtype=np.uint8)


    
    for i in range(0,rows):
        for j in range(0,cols):
            if 180 < img[i][j] <= 255:
                res_img[i][j] = config.COLOR_WHITE
            #elif 150 < img[i][j] <= 190:
            #    res_img[i][j] = config.COLOR_BROWN
            elif 105 < img[i][j] <= 180:
                res_img[i][j] = config.COLOR_GRAY
            else:
                res_img[i][j] = config.COLOR_BLACK

    return res_img

def combineMosaic(gray_mosaic_img, bricks_mosaic_img):
    rows, cols, channels = gray_mosaic_img.shape
    res_img = np.empty((config.MOSAIC_SIZE,config.MOSAIC_SIZE,3), dtype=np.uint8)
    for i in range(0,rows):
        for j in range(0,cols):
            if bricks_mosaic_img[i][j].all() != config.COLOR_BLUE.all():
                res_img[i][j] = bricks_mosaic_img[i][j]
            else:
                res_img[i][j] = gray_mosaic_img[i][j]
    return res_img


if __name__ == "__main__":
    img = cv2.imread(sys.argv[1])
    local_debug = 1
    main(img)
    print getRegion(0)
