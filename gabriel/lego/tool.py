import cv2
import math
import numpy as np
def get_corner_pts(bw, perimeter = None, center = None, method = 'line'):
    '''
    Given an input image @bw where the borders of a rough rectangle are
masked, the function detects its corners
    Two methods:
    'line' tries to detect four lines first, and
    'point' directly gets the top-left, top-right, bottom-left,
bottom-right points
    The function returns None if cannot find the corners with confidence
    '''
    if method == 'line':
        center = (center[1], center[0]) # in (x, y) format
        perimeter = int(perimeter)


        lines = cv2.HoughLinesP(bw, 1, np.pi/180, perimeter/40 ,
                minLineLength = perimeter / 20, maxLineGap = perimeter / 20)
        lines = lines[0]

        # This is only for test
        img = np.zeros((bw.shape[0], bw.shape[1], 3), dtype=np.uint8)
        for line in lines:
            pt1 = (line[0], line[1])
            pt2 = (line[2], line[3])
            #print (pt1, pt2)
            cv2.line(img, pt1, pt2, (255, 255, 255), 3)
        #display_image('test', img, wait_time = config.DISPLAY_WAIT_TIME,
        cv2.imshow('test', img)
        cv2.waitKey(0)
        
        #resize_max = config.DISPLAY_MAX_PIXEL, save_image = config.SAVE_IMAGE)

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
        if len(new_lines) != 4:
            print new_lines
            return None
        #print new_lines

        # get four reasonable line intersections
        corners = list()
        for idx1, line1 in enumerate(new_lines):
            for idx2, line2 in enumerate(new_lines):
                if idx1 >= idx2:
                    continue
                inter_p = line_interset(line1, line2)
                if inter_p == (-1, -1):
                    continue
                dist = euc_dist(inter_p, center)
                if dist < perimeter / 3:
                    corners.append(inter_p)
        if len(corners) != 4:
            return None

        # put the four corners in order
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

        # some sanity check here
        len_b = euc_dist(bl, br)
        len_u = euc_dist(ul, ur)
        len_l = euc_dist(ul, bl)
        len_r = euc_dist(ur, br)
        if len_b < len_u or len_b < len_l or len_b < len_r:
            return None

    elif method == 'point':
        bw = bw.astype(bool)
        row_mtx, col_mtx = np.mgrid[0 : bw.shape[0], 0 : bw.shape[1]]
        row_mtx = row_mtx[bw]
        col_mtx = col_mtx[bw]

        row_plus_col = row_mtx + col_mtx
        ul_idx = np.argmin(row_plus_col)
        ul = (col_mtx[ul_idx], row_mtx[ul_idx])
        br_idx = np.argmax(row_plus_col)
        br = (col_mtx[br_idx], row_mtx[br_idx])

        row_minus_col = row_mtx - col_mtx
        ur_idx = np.argmin(row_minus_col)
        ur = (col_mtx[ur_idx], row_mtx[ur_idx])
        bl_idx = np.argmax(row_minus_col)
        bl = (col_mtx[bl_idx], row_mtx[bl_idx])

    corners = np.float32([ul, ur, bl, br])
    return corners


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


def line_interset(a, b):
    x1 = a[0]; y1 = a[1]; x2 = a[2]; y2 = a[3]
    x3 = b[0]; y3 = b[1]; x4 = b[2]; y4 = b[3]
    d = ((float)(x1-x2) * (y3-y4)) - ((y1-y2) * (x3-x4))
    if d:
        x = ((x1*y2 - y1*x2) * (x3-x4) - (x1-x2) * (x3*y4 - y3*x4)) / d
        y = ((x1*y2 - y1*x2) * (y3-y4) - (y1-y2) * (x3*y4 - y3*x4)) / d
    else:
        x, y = (-1, -1)
    return (x, y)

def euc_dist(pt1,pt2):
    return math.sqrt((pt2[0]-pt1[0])*(pt2[0]-pt1[0])+(pt2[1]-pt1[1])*(pt2[1]-pt1[1]))

def write_img(img, filename):
    cv2.imwrite(filename, img)
