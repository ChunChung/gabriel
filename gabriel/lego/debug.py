import cv2
def imshow(frameName, img):
    resize = cv2.resize(img, (320, 240))
    cv2.imshow(frameName, resize)
    cv2.waitKey(1) 
