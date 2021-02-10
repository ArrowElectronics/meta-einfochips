#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "Diego Dorta, Marco Franchi and Vanessa Maegima"
__copyright__ = "Copyright (C) 2019 NXP Semiconductors"
__license__ = "MIT"
import subprocess as s
import time, csv, cv2, sys
from imutils.video import WebcamVideoStream
from imutils.video import FPS
from threading import Lock, Thread

import argparse
from pathlib import Path

lock = Lock()

ARMNN_RUN = "TfInceptionV3-Armnn --data-dir=data --model-dir=models > /opt/armnn/log.txt"
PARSER_SCRIPT = "./parser.sh"
INPUT_PATH = "/opt/armnn/data/"
UGLY_HACK = "Dog.jpg"
RECTANGLE = 4
READY = 8


def labeler(data):
    with open("labels.csv") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=':')
        for row in csv_reader:
            if(data == row[0]): return row[1]
    return False

def execute_armnn_output_parser(process=None):
    p = s.Popen(PARSER_SCRIPT, stdout=s.PIPE)
    return str(p.communicate()[0], encoding="utf-8").rstrip("\n")    

def execute_armnn_camera_input():
    s.call(ARMNN_RUN, shell=True)

def inference_process():
    try:
        execute_armnn_camera_input()
    except:
        exit()        
    parsed = execute_armnn_output_parser()
    print(labeler(parsed))
    return 0

def get_image_contours(f=None):
    g = cv2.cvtColor(f, cv2.COLOR_BGR2GRAY)
    t, thres = cv2.threshold(g, 60, 255, cv2.THRESH_BINARY_INV)
    return cv2.findContours(thres, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)[-2]

def get_largest_contours(c=None):
    contours = sorted(c, key = cv2.contourArea)
    l = contours[-1]
    return cv2.approxPolyDP(l, 0.02*cv2.arcLength(l, True), True)

def draw_contours(f, r):
    return cv2.drawContours(f, [r], -1, (0, 255, 255), 1, cv2.LINE_AA)

def create_mask_crop_rectangle_content(f, r):
    m = f.copy()
    cv2.drawContours(f, [r], -1, 0, -1)
    return m
    
def get_contours_perimeter_crop(r, m):
    x, y, width, height = cv2.boundingRect(r)
    x += 10
    y += 10
    return m[y:y + height - 30, x:x + width - 30]
    
def save_cam_mipi_input(r):
    cv2.imwrite(INPUT_PATH + UGLY_HACK, r)
    return 0
    

def inference():
    lock.acquire()
    inference_process()
    lock.release()
 
def main(count=0):
    print("Starting video stream...")
    input_cam = WebcamVideoStream(src=args["videosrc"]).start()
    time.sleep(1.0)
    while True:
        frame = input_cam.read()
        contours = get_image_contours(frame)
        result = get_largest_contours(contours)    
        if (len(result) == RECTANGLE):
            draw_contours(frame, result)
            count += 1
        else: count = 0
        if (count == READY):
            mask = create_mask_crop_rectangle_content(frame, result)
            roi = get_contours_perimeter_crop(result, mask)                        
            count = save_cam_mipi_input(roi)
            print ("Image captured. Wait... ")   
            inf = Thread(target=inference)
            inf.start()
        cv2.imshow("demo", frame)
        if (cv2.waitKey(1) & 0xFF == ord('q')): break

    input_cam.stop()
    return cv2.destroyAllWindows()

if __name__ == "__main__":

    # construct the argument parser and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-v", "--videosrc", type=str, default="/dev/video0",
                    help="provide video source (device index of camera i.e. /dev/video5 "
                         "or v4l2 command for mazzanine camera)")

    args = vars(ap.parse_args())
    main()
