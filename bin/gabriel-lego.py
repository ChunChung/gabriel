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
        try:
            while 1:
                if self.data_queue.empty() == False:
                    image_data = self.data_queue.get()
                    sys.stdout.write("get image!!!!!!!!!!")
                    time.sleep(0.001)
            return 
        except:
            sys.stdout.write("Exception in DummyAccApp!")


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

    # dummy acc app
    #acc_client = None
    #acc_app = None
    #acc_queue = Queue.Queue(1)
    #acc_client = AppProxyStreamingClient((acc_ip, acc_port), acc_queue)
    #acc_client.start()
    #acc_client.isDaemon = True
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
        if acc_client is not None:
            acc_client.terminate()
        if acc_app is not None:
            acc_app.terminate()
        result_pub.terminate()

