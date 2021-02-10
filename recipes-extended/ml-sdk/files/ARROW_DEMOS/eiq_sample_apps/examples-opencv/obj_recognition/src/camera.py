#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "Diego Dorta"
__copyright__ = "Copyright (C) 2019 NXP Semiconductors"
__license__ = "BSD-3-Clause"
from socket import gethostbyaddr, gethostname
import cv2 as opencv
from threading import Thread

class singleShotDetector(object):
    def __init__(self, l, **kwargs):
        self.__dict__.update(kwargs)
        self.nn = opencv.dnn.readNetFromCaffe(self.modelSSDProtoPath,
                                              self.modelSSDCaffePath)
        self.video = opencv.VideoCapture(self.mode)
        self.labels = l
        self.coordinates = []
        self.files = []
        self.ir = 0
        self.ic = 0
        self.hf = 0
        self.wf = 0
        self.blob = 0
                                          
    def caffeInference(self, img, nn):
        self.blob = opencv.dnn.blobFromImage(self.ir, self.scaleFactor,
            (self.height, self.width),
            (self.normalize, self.normalize, self.normalize), False)            
        nn.setInput(self.blob)
        det = nn.forward()
        self.ic = img.copy()
        cols = self.ir.shape[1] 
        rows = self.ir.shape[0]        

        for i in range(det.shape[2]):
            confidence = det[0, 0, i, 2]
            if (confidence > self.threshold):
                index = int(det[0, 0, i, 1])
                self.math(i, det, cols, rows)
                opencv.rectangle(img, (self.coordinates[4], self.coordinates[5]),
                    (self.coordinates[6], self.coordinates[7]), (0, 0, 0),2)
                if (index in self.labels):
                    l = (self.labels[index] + ": " + str(confidence))
                    size, line = opencv.getTextSize(l, opencv.FONT_HERSHEY_TRIPLEX, 1, 3)
                    self.coordinates[5] = max(self.coordinates[5], size[1])                    
                    opencv.rectangle(img, (self.coordinates[4], self.coordinates[5] - size[1]),
                        (self.coordinates[4] + size[0], self.coordinates[5] + line),
                            (255, 255, 255), opencv.FILLED)                            
                    opencv.putText(img, l, (self.coordinates[4], self.coordinates[5]),
                        opencv.FONT_HERSHEY_DUPLEX, 1, (0, 0, 0))
            self.coordinates = []

    def run(self):      
        while True:
            frame = self.video.read()
            self.ir = opencv.resize(frame[1], (self.height, self.width))
            self.hf = (frame[1].shape[0] / self.height)
            self.wf = (frame[1].shape[1] / self.width)
            self.caffeInference(frame[1], self.nn)
            opencv.namedWindow("appFrame")
            opencv.imshow("appFrame", frame[1])
            if (opencv.waitKey(1) >= 0):
                break

    def math(self, i, d, c, r):
        self.coordinates.append(int(d[0, 0, i, 3] * c))
        self.coordinates.append(int(d[0, 0, i, 4] * r))
        self.coordinates.append(int(d[0, 0, i, 5] * c))
        self.coordinates.append(int(d[0, 0, i, 6] * r))
        self.coordinates.append(int(self.wf * int(d[0, 0, i, 3] * c)))
        self.coordinates.append(int(self.hf * int(d[0, 0, i, 4] * r)))
        self.coordinates.append(int(self.wf * int(d[0, 0, i, 5] * c)))
        self.coordinates.append(int(self.hf * int(d[0, 0, i, 6] * r)))

def getHostName():
    l = [ "imx8qxpmek", "imx8qmmek",
          "imx8mqevk", "imx8mmevk" ]
    return True if gethostname() in l else False

def gStreamerSettings(width, height):
    return (("v4l2src ! video/x-raw,width={},height={} !"
                " videoconvert ! appsink").format(width, height))

if __name__ == "__main__":
    labels = {  0:  'Background',
                1:  'Aeroplane',
                2:  'Bicycle',
                3:  'Bird',
                4:  'Boat',
                5:  'Bottle',
                6:  'Bus',
                7:  'Car',
                8:  'Cat',
                9:  'Chair',
                10: 'Cow',
                11: 'Diningtable',
                12: 'Dog',
                13: 'Horse',
                14: 'Motorbike',
                15: 'Person',
                16: 'Pottedplant',
                17: 'Sheep',
                18: 'Sofa',
                19: 'Train',
                20: 'TVMonitor'
    }
    dict = {    "modelSSDProtoPath" : "model/MobileNetSSD_deploy.prototxt",
                "modelSSDCaffePath" : "model/MobileNetSSD_deploy.caffemodel",
                "mediaPath"         : "media/",
                "mode"              : gStreamerSettings(640, 480) if getHostName() else 0,
                "width"             : 300,
                "height"            : 300,
                "normalize"         : 127.5,
                "threshold"         : 0.2,
                "scaleFactor"       : 0.009718,
                "ext"               : (".jpeg", ".jpg", ".png")
    }
    app = singleShotDetector(labels, **dict)
    inf = Thread(target=app.run())
    inf.start()
