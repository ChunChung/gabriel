def detectBricks(img, color_type):

    e1 = cv2.getTickCount()

    img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    ##mask = cv2.inRange(hsv, lower_black, upper_black)
    ##rows, cols = mask.shape
    #
    #res = cv2.pyrDown(img)

    #rows, cols, channels = res.shape

    #while rows>64 and cols > 64:
    #    res = cv2.pyrDown(res)
    #    rows, cols, channels = res.shape

    #frame = cv2.resize(res, (32,32)) 

    #resize1 = cv2.resize(img, (32,32))
    #resize2 = cv2.resize(img, dsize=(32,32), interpolation=cv2.INTER_NEAREST)
    resize3 = cv2.resize(img, dsize=(32,32), interpolation=cv2.INTER_CUBIC)


    #cv2.imshow('123', img)
    e2 = cv2.getTickCount()
    time = (e2 - e1)/ cv2.getTickFrequency()
    print 'processing time: ', time

    detectColors(resize3)
    #cv2.imshow('default', img)
    #cv2.imshow('1', resize1)
    #cv2.imshow('2', resize2)
    resize3 = cv2.cvtColor(resize3, cv2.COLOR_HSV2BGR)
    #rows, cols, channels = resize3.shape

    #for i in range(0,rows):
    #    for j in range(0,cols):
    #        print img[i][j],
    #    print ""
    cv2.imshow('3', resize3)
    #cv2.imshow('mask', frame)
    cv2.waitKey(0)


def detectColors(img):
    lower_black = np.array([0,0,0], dtype=np.uint8)
    upper_black = np.array([60,60,10], dtype=np.uint8)
    lower_white = np.array([0,0,80], dtype=np.uint8)
    upper_white = np.array([255,20,255], dtype=np.uint8)

    rows, cols, channels = img.shape

    for i in range(0,rows):
        for j in range(0,cols):
            print img[i][j] ,
        print ""




