#!/usr/bin/env python3
# Copyright 2020 NXP
# SPDX-License-Identifier: MIT

# Command : python3 tflite_mobilenetv1_quantized.py --cam 5
# 5 is device id of the attached USB Camera

import numpy as np
import pyarmnn as ann
import example_utils as eu
import os
import cv2
from PIL import Image

args = eu.parse_command_line()

# names of the files in the archive
labels_filename = 'labels_mobilenet_quant_v1_224.txt'
model_filename = 'mobilenet_v1_1.0_224_quant.tflite'
archive_filename = 'mobilenet_v1_1.0_224_quant_and_labels.zip'

archive_url = \
    'https://storage.googleapis.com/download.tensorflow.org/models/tflite/mobilenet_v1_1.0_224_quant_and_labels.zip'

model_filename, labels_filename = eu.get_model_and_labels(args.model_dir, model_filename, labels_filename,
                                                          archive_filename, archive_url)

# all 3 resources must exist to proceed further
assert os.path.exists(labels_filename)
assert os.path.exists(model_filename)

# Create a network from the model file
net_id, graph_id, parser, runtime = eu.create_tflite_network(model_filename)

# Load input information from the model
# tflite has all the need information in the model unlike other formats
input_names = parser.GetSubgraphInputTensorNames(graph_id)
assert len(input_names) == 1  # there should be 1 input tensor in mobilenet

input_binding_info = parser.GetNetworkInputBindingInfo(graph_id, input_names[0])
input_width = input_binding_info[1].GetShape()[1]
input_height = input_binding_info[1].GetShape()[2]

# Load output information from the model and create output tensors
output_names = parser.GetSubgraphOutputTensorNames(graph_id)
assert len(output_names) == 1  # and only one output tensor
output_binding_info = parser.GetNetworkOutputBindingInfo(graph_id, output_names[0])
output_tensors = ann.make_output_tensors([output_binding_info])

# Load labels file
labels = eu.load_labels(labels_filename)

camera_source = int(args.cam) if len(args.cam) == 1 else str(args.cam)

cam = cv2.VideoCapture(camera_source)
cam.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

def predict(img, input_width, input_height):

    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    pil_img = Image.fromarray(img_rgb)
    
    # Load images and resize to expected size
    processed_pil_image = eu.load_image(pil_img, input_width, input_height)

    result_txt = eu.run_inference_on_frame(runtime, net_id, processed_pil_image, labels, input_binding_info, output_tensors)

    # display predictions
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(img, result_txt, (10, 50), font, 1, (0, 255, 0), 1, cv2.LINE_AA)
    return img

# ===================== Run camera stream and inference on every frame ===================================

while True:
    # read frames
    ret, img = cam.read()

    if ret:
        im_w = img.shape[1]
        im_h = img.shape[0]

        predicted_img = predict(img, input_width, input_height)
        cv2.imshow("Video Stream", predicted_img)

        key = cv2.waitKey(1)
        if key == ord('q'):
            break
    else:
        break

## close camera
cam.release()
cv2.destroyAllWindows()
