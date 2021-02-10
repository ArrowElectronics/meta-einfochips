#!/usr/bin/python3
# -*- coding: utf-8 -*-

#
# Copyright (c) 2018 Arrow Electronics
#

from threading import Thread, Lock
import time
import random
import os

import neural_net


class NeuralNetworkThread(Thread):
    class OfflineImages:
        def __init__(self, data_path):
            self.image_list = ["".join([data_path, filename]) for filename in os.listdir(data_path) if
                               os.path.isfile(os.path.join(data_path, filename))]
            self.image_list.sort()
            random.shuffle(self.image_list)
            self.num_samples = len(self.image_list)
            print("OFF_IMG> LIST OF IMAGES:")
            print(self.image_list)
            self.last_idx = 0

        def get_next_image_path(self):
            image_path = self.image_list[self.last_idx]
            self.last_idx += 1
            if self.last_idx == self.num_samples:
                self.last_idx = 0
            print("OFF_IMG> IMAGE_PATH: ", image_path)
            return image_path

    def __init__(self, offline_folder, online_file_name, video_src, use_cv=False, use_qt_only=False):
        self.__online_file_name = online_file_name
        self.__offline_image_list = NeuralNetworkThread.OfflineImages(offline_folder)

        self.__use_cv = use_cv
        self.__use_qt_only = use_qt_only
        if use_cv:
            print("NN THREAD> USING CV2")
            import cv2
            # #CAPTURE_GST_PIPELINE="videotestsrc is-live=true ! video/x-raw, width=160, height=120, format=NV12 ! videoconvert ! appsink"
            # CAPTURE_GST_PIPELINE="\
            # nvarguscamerasrc sensor-id=0 ! \
            # video/x-raw(memory:NVMM), width=1280, height=720, format=NV12, framerate=120/1 ! \
            # nvvidconv flip-method=2 ! \
            # video/x-raw, width=640, height=360, format=NV12, framerate=120/1 ! \
            # appsink"
            # self.__camera_device = cv2.VideoCapture(CAPTURE_GST_PIPELINE, cv2.CAP_GSTREAMER)
            camera_source = int(video_src) if len(video_src) == 1 else str(video_src)
            self.__camera_device = cv2.VideoCapture(camera_source)
        self.__iter_count = 0
        self.__nn_dict_tf_qt = {}
        self.__live_mode = False
        self.lock = Lock()
        super(NeuralNetworkThread, self).__init__()

    def set_mode_live_mode(self, is_live=True):
        print("NN> setting live mode to: ", is_live)
        if is_live:
            print("NN> switching to 160x120 model")
        else:
            print("NN> switching to 640x480 model")
        self.__live_mode = is_live

    def acquire_lock(self):
        print("NN> acquiring lock (non=blocking)")
        return self.lock.acquire_lock(blocking=False)

    def release_lock(self):
        print("NN> releasing lock")
        self.lock.release_lock()

    def get_new_results(self):
        print("NN> returning inference results, iter count:", self.__iter_count)
        iter_count = self.__iter_count
        nn_output = self.__nn_dict_tf_qt
        return iter_count, nn_output

    def run(self):
        while 1:
            print("NN> SPINNING NN THREAD")
            if self.__live_mode:
                if self.__use_cv:
                    import cv2
                    ret, frame = self.__camera_device.read()
                    # gray = cv2.cvtColor(frame, cv2.COLOR_YUV2GRAY_NV12)
                    cv2.imwrite(self.__online_file_name, frame)
                image_path = self.__online_file_name
                use_640x480_model = False
            else:
                image_path = self.__offline_image_list.get_next_image_path()
                use_640x480_model = True
            output = neural_net.run_inference_on_image(image_path, use_640x480_sess=use_640x480_model, use_qt_only=self.__use_qt_only, downscale_dens_map=False)
            self.lock.acquire()
            self.__nn_dict_tf_qt = output
            self.__iter_count += 1

            self.lock.release()
            print("NN> FINISHED ITERATION, NOTIFYING LISTENING THREAD")
