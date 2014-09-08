#!/usr/bin/env python
#
# Cloudlet Infrastructure for Mobile Computing
#
#   Author: Kiryong Ha <krha@cmu.edu>
#
#   Copyright (C) 2011-2013 Carnegie Mellon University
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#

import time
import Queue
import struct
import threading

import os
import sys
if os.path.isdir("../gabriel") is True:
    sys.path.insert(0, "..")

from gabriel.proxy.common import AppProxyStreamingClient
from gabriel.proxy.common import AppProxyThread
from gabriel.proxy.common import ResultpublishClient
from gabriel.proxy.common import get_service_list
from gabriel.common.config import ServiceMeta as SERVICE_META

import Image
import io
import cv
import cv2
import numpy as np

share_queue = Queue.Queue()

class DummyVideoApp(AppProxyThread):

    def handle(self, header, data):
        global share_queue
        share_queue.put_nowait(data)
        result = ""
        return result


class DummyAccApp(AppProxyThread):
    def handle(self, header, acc_data):
        global share_queue
        self.data_queue = share_queue
        self.result_queue = Queue.Queue()
        i = 0
        while 1:
            if self.data_queue.empty() == False:
                image_data = self.data_queue.get()
                imagere = Image.open(io.BytesIO(image_data))
                frame = np.array(imagere)

                tmp_img = np.array(frame)
                hsv = cv2.cvtColor(tmp_img, cv2.COLOR_BGR2HSV)
                
                # define range of blue color in HSV
                lower_blue = np.array([110,50,50], dtype=np.uint8)
                upper_blue = np.array([130,255,255], dtype=np.uint8)
                
                # Threshold the HSV image to get only blue colors
                mask = cv2.inRange(hsv, lower_blue, upper_blue)
                
                kernel = np.ones((5,5),np.uint8)
                mask = cv2.erode (mask,kernel,iterations = 1)
                mask = cv2.dilate(mask,kernel,iterations = 1)
                mask = cv2.dilate(mask,kernel,iterations = 1)
                mask = cv2.erode (mask,kernel,iterations = 1)
                
                # Bitwise-AND mask and original image
                res = cv2.bitwise_and(frame,frame, mask= mask)
                
                cv2.imshow('frame', frame )
                cv2.imshow('mask',mask)
                cv2.imshow('res',res)

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
                #result_img = cv.CreateMat(960,1280,cv.CV_8U)

                #cv.Copy(image_data,result_img)
                time.sleep(0.001)
        return 


if __name__ == "__main__":
    result_queue = list()

    sys.stdout.write("Discovery Control VM\n")
    service_list = get_service_list(sys.argv)
    video_ip = service_list.get(SERVICE_META.VIDEO_TCP_STREAMING_ADDRESS)
    video_port = service_list.get(SERVICE_META.VIDEO_TCP_STREAMING_PORT)
    acc_ip = service_list.get(SERVICE_META.ACC_TCP_STREAMING_ADDRESS)
    acc_port = service_list.get(SERVICE_META.ACC_TCP_STREAMING_PORT)
    return_addresses = service_list.get(SERVICE_META.RESULT_RETURN_SERVER_LIST)

    # image receiving thread
    video_frame_queue = Queue.Queue(1)
    video_client = AppProxyStreamingClient((video_ip, video_port), video_frame_queue)
    video_client.start()
    video_client.isDaemon = True
    dummy_video_app = DummyVideoApp(video_frame_queue, result_queue) # dummy app for image processing
    dummy_video_app.start()
    dummy_video_app.isDaemon = True

    acc_app = DummyAccApp(video_frame_queue, result_queue)
    acc_app.start()
    acc_app.isDaemon = True

    # result pub/sub
    result_pub = ResultpublishClient(return_addresses, result_queue)
    result_pub.start()
    result_pub.isDaemon = True

    try:
        while True:
            time.sleep(1)
    except Exception as e:
        pass
    except KeyboardInterrupt as e:
        sys.stdout.write("user exits\n")
    finally:
        if video_client is not None:
            video_client.terminate()
        if dummy_video_app is not None:
            dummy_video_app.terminate()
        if acc_app is not None:
            acc_app.terminate()
        result_pub.terminate()

