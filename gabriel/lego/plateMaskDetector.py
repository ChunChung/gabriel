import debug
import sys
import cv2
import numpy as np
import math
import config 



local_debug = 0

def nothing(x):
    pass


def main(frame, lower_blue, upper_blue):
    # erode for trying to remove specular highlight
    kernel = np.ones((5,5),np.uint8)
    frame_erode = cv2.erode (frame,kernel,iterations = 1)

    #frame2 = specular_free(frame)
    hsv = cv2.cvtColor(frame_erode, cv2.COLOR_BGR2HSV)

    # define range of blue color in HSV
    #lower_blue = np.array([100,90,0], dtype=np.uint8)
    #upper_blue = np.array([140,255,255], dtype=np.uint8)

    if config.DEBUG == 1:
        print lower_blue
        print upper_blue

    #gray = cv2.cvtColor( tmp_img, cv2.COLOR_BGR2GRAY )

    #ret,thresh1 = cv2.threshold(gray,127,255,cv2.THRESH_BINARY)
    #ret,thresh2 = cv2.threshold(gray,127,255,cv2.THRESH_BINARY_INV)
    #ret,thresh3 = cv2.threshold(gray,127,255,cv2.THRESH_TRUNC)
    #ret,thresh4 = cv2.threshold(gray,127,255,cv2.THRESH_TOZERO)
    #ret,thresh5 = cv2.threshold(gray,127,255,cv2.THRESH_TOZERO_INV)
    #th3 = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
    #                    cv2.THRESH_BINARY_INV,11,2)
    #
    #im = cv2.threshold(th3, 0, 255, cv2.THRESH_OTSU)[1]
    #median = cv2.medianBlur(frame,5)
    #thresh = ['thresh1','thresh2','thresh3','thresh4','thresh5']

    # Threshold the HSV image to get only blue colors
    mask = cv2.inRange(hsv, lower_blue, upper_blue)

    orig_mask = mask

    
    kernel = np.ones((5,5),np.uint8)
    mask = cv2.erode (mask,kernel,iterations = 1)
    mask = cv2.dilate(mask,kernel,iterations = 1)
    mask = cv2.dilate(mask,kernel,iterations = 1)
    mask = cv2.erode (mask,kernel,iterations = 1)

    #if config.DEBUG == 1:
        #debug.imshow("mask", mask)
        #debug.imshow("frame", frame)
        #debug.imshow("erode", frame_erode)
        #debug.imshow("noerode dilte", orig_mask)

    return mask

def specular_free(frame, a=2):

    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    height, width, channels = frame.shape
    dst_data = np.empty((height,width,channels))
    for i in range(0, height):
        for j in range(0, width):
            matrix1 = np.empty((3,3))
            #matrix1[0] = [1, 0, 1/3]
            #matrix1[1] = [-1/2, math.sqrt(3)/2, 1/3]
            #matrix1[2] = [-1/2, -math.sqrt(3)/2, 1/3]
            matrix1[0] = [1, -1/2, -1/2]
            matrix1[1] = [0, math.sqrt(3)/2, -math.sqrt(3)/2]
            matrix1[2] = [1/3, 1/3, 1/3]
            m = np.dot(matrix1, frame[i][j])
            tmp_m3 = a * math.sqrt(m[0]*m[0] + m[1]*m[1])
            m2 = [m[0], m[1], tmp_m3]
            matrix2 = np.empty((3,3))
            #matrix2[0] = [2/3, -1/3, -1/3]
            #matrix2[1] = [0, 1/math.sqrt(3), -1/math.sqrt(3)]
            #matrix2[2] = [1, 1, 1]
            matrix2[0] = [2/3, 0, 1]
            matrix2[1] = [-1/3, 1/math.sqrt(3), 1]
            matrix2[2] = [-1/3, -1/math.sqrt(3), 1]

            dst_data[i][j] = np.dot(matrix2, m2)

    dst_data = dst_data.astype(np.uint8)
    dst_data = cv2.cvtColor(dst_data, cv2.COLOR_RGB2BGR)
    return dst_data


def remove_highlight(frame):
    height, width, channels = frame.shape

    dst_data = np.empty((height,width,channels))

    #int step=src->widthStep;
    #int i=0,j=0;
    #unsigned char R,G,B,MaxC;
    #double alpha,beta,alpha_r,alpha_g,alpha_b,beta_r,beta_g,beta_b,temp=0,realbeta=0,minalpha=0;
    #double gama,gama_r,gama_g,gama_b;
    #unsigned char* srcData;
    #unsigned char* dstData;
    #for (i=0;i<height;i++)
    for i in range(0, height):
        for j in range(0, width):
            R = float(frame[i][j][2])
            G = float(frame[i][j][1])
            B = float(frame[i][j][0])


            alpha_r = R / (R+G+B)
            alpha_g = G / (R+G+B)
            alpha_b = B / (R+G+B)
            alpha = max(max(alpha_r, alpha_g), alpha_b)
            print alpha
            maxC = max(max(R,G),B)
            minalpha = min(min(alpha_r, alpha_g), alpha_b)
            beta_r=1-(alpha-alpha_r)/(3*alpha-1)
            beta_g = 1-(alpha-alpha_g)/(3*alpha-1) 
            beta_b=1-(alpha-alpha_b)/(3*alpha-1)
            beta=max(max(beta_r,beta_g),beta_b)
            gama_r=(alpha_r-minalpha)/(1-3*minalpha)
            gama_g=(alpha_g-minalpha)/(1-3*minalpha)
            gama_b=(alpha_b-minalpha)/(1-3*minalpha)
            gama=max(max(gama_r,gama_g),gama_b)
            temp=(gama*(R+G+B)-maxC)/(3*gama-1)
            dst_data[i][j][2]=R-(temp+0.5)
            dst_data[i][j][1]=G-(temp+0.5)
            dst_data[i][j][0]=B-(temp+0.5)



    return dst_data
    # {
    #      srcData=(unsigned char*)src->imageData+i*step;
    #      dstData=(unsigned char*)dst->imageData+i*step;
    #      for (j=0;j<width;j++)
    #       {
    #             R=srcData[j*3];
    #            G=srcData[j*3+1];
    #            B=srcData[j*3+2];
    #
    #          alpha_r=(double)R/(double)(R+G+B);
    #         alpha_g=(double)G/(double)(R+G+B);
    #         alpha_b=(double)B/(double)(R+G+B);
    #         alpha=max(max(alpha_r,alpha_g),alpha_b);
    #         MaxC=max(max(R,G),B);// compute the maximum of the rgb channels
    #         minalpha=min(min(alpha_r,alpha_g),alpha_b);                 beta_r=1-(alpha-alpha_r)/(3*alpha-1);
    #         beta_g=1-(alpha-alpha_g)/(3*alpha-1);
    #         beta_b=1-(alpha-alpha_b)/(3*alpha-1);
    #         beta=max(max(beta_r,beta_g),beta_b);// gama is used to approximiate the beta
    #         gama_r=(alpha_r-minalpha)/(1-3*minalpha);
    #         gama_g=(alpha_g-minalpha)/(1-3*minalpha);
    #         gama_b=(alpha_b-minalpha)/(1-3*minalpha);
    #         gama=max(max(gama_r,gama_g),gama_b);   
    #
    #         temp=(gama*(R+G+B)-MaxC)/(3*gama-1);
    #         //beta=(alpha-minalpha)/(1-3*minalpha)+0.08;
    #         //temp=(gama*(R+G+B)-MaxC)/(3*gama-1);
    #        dstData[j*3]=R-(unsigned char)(temp+0.5);
    #        dstData[j*3+1]=G-(unsigned char)(temp+0.5);
    #        dstData[j*3+2]=B-(unsigned char)(temp+0.5);   
    #}


if __name__ == "__main__":
    img = cv2.imread(sys.argv[1])
    local_debug = 1 
    main(img)

