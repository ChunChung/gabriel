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
from gabriel.lego import perspectiveTransform
from gabriel.lego import bricksDetector
from gabriel.lego import debug
from gabriel.lego import plateMaskDetector
from gabriel.lego import config
from gabriel.lego import mosaicHandler
from gabriel.lego import InstRender

import Image
import io
import cv
import cv2
import numpy as np

class DummyVideoApp(AppProxyThread):
    def __init__(self, video_frame_queue, result_queue):
        AppProxyThread.__init__(self, video_frame_queue, result_queue)



    def handle(self, header, data):
        #print "start:" + str(time.time())
        imagere = Image.open(io.BytesIO(data))
        frame = np.array(imagere)
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

        if config.RECORD == 1:
            filename = "./test_images8/frame-" + str(header['id']).zfill(5) + ".jpeg"
            cv2.imwrite(filename, frame)
            return "some messages"

        # Generate mosaic
        if 'stream_type' in header and header['stream_type'] == 1: 
            if os.path.isfile(config.MOSAIC_NAME):
                os.remove(config.MOSAIC_NAME)
                print "Reset " + config.MOSAIC_NAME + " file"
            cv2.imwrite('test.bmp', frame)
            result_msg = mosaicHandler.main(frame)
            region_num = 0
            region = config.REGIONS[region_num]
            action = config.ACTIONS[0]
            bricks = mosaicHandler.getRegion(region_num)
            #results = {"action": action, "bricks": {"status":bricks, "region": region}, "voice": "let's start at left top of the plat"}
            #TODO: pass mosaic 18x18 numpy array into InstRender constructor
	    self.m = np.empty((18, 18), dtype=np.int32)
    	    self.m.fill(config.BLUE)
    	    for i in range(2, 16):
        	for j in range(2, 16):
            	    self.m[i, j] = j % 5 + 2
	    self.ir = InstRender.InstRender(self.m)
    	    results = self.ir.start(config.REGIONS[0])
	    return results
	elif 'stream_type' in header and header['stream_type'] == 2:
	    #TODO: pass detect numpy array into InstrRender.update()
            self.d = np.empty((18, 18), dtype=np.int32)
            self.d.fill(config.BLUE)
            for i in range(2, 4):
                for j in range(2, 4):
                    self.d[i, j] = self.m[i, j]
            results = self.ir.update(self.d)
	    return results


        e1 = cv2.getTickCount()
        debug.imshow('frame', frame)

        # create trackbars for color change
        cv2.createTrackbar('lower_h','frame',100,180,plateMaskDetector.nothing)
        cv2.createTrackbar('lower_s','frame',90,255,plateMaskDetector.nothing)
        cv2.createTrackbar('lower_v','frame',45,255,plateMaskDetector.nothing)
                           
        # create trackbars for color change
        cv2.createTrackbar('higher_h','frame',140,180,plateMaskDetector.nothing)
        cv2.createTrackbar('higher_s','frame',255,255,plateMaskDetector.nothing)
        cv2.createTrackbar('higher_v','frame',255,255,plateMaskDetector.nothing)


        lower_h = cv2.getTrackbarPos('lower_h', 'frame')
        lower_s = cv2.getTrackbarPos('lower_s', 'frame')
        lower_v = cv2.getTrackbarPos('lower_v', 'frame')
        higher_h = cv2.getTrackbarPos('higher_h', 'frame')
        higher_s = cv2.getTrackbarPos('higher_s', 'frame')
        higher_v = cv2.getTrackbarPos('higher_v', 'frame')

        #lower_h = 100
        #lower_s = 90
        #lower_v = 0

        #higher_h = 140
        #higher_s = 255
        #higher_v = 255

        mask = plateMaskDetector.main(frame, np.array([lower_h, lower_s, lower_v], dtype=np.uint8), np.array([higher_h, higher_s, higher_v], dtype=np.uint8))

        # Bitwise-AND mask and original image
        res = cv2.bitwise_and(frame,frame, mask= mask)


        debug.imshow('mask', mask)
        debug.imshow('res', res)


        lego_img = perspectiveTransform.perspective_transform(frame, mask)

        if lego_img is not None:
            #TODO: detect bricks
            cv2.imwrite("compare.jpg", frame)
            region_num = 0
            bricks = bricksDetector.main(lego_img, region_num)
            region = config.REGIONS[region_num]
            action = config.ACTIONS[1]
            results = {"action": action, "bricks": {"status":bricks, "region": region}, "voice": "let's start at left top of the plat"}
	    return results
	
        #Performance Measurement 	
        e2 = cv2.getTickCount()
        time = (e2 - e1)/ cv2.getTickFrequency()
        print 'processing time: ', time

        return "some message"


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

    #acc_app = DummyAccApp(video_frame_queue, result_queue)
    #acc_app.start()
    #acc_app.isDaemon = True

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
        #if acc_app is not None:
        #    acc_app.terminate()
        result_pub.terminate()

