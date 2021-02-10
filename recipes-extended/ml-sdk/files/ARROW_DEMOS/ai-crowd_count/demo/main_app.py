#!/usr/bin/python3
# -*- coding: utf-8 -*-

#
# Copyright (c) 2018 Arrow Electronics
#

import sys
import os
import time
import random
import numpy as np
import argparse

from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QPushButton, QDialog, QHBoxLayout, QStackedWidget, QSpacerItem
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from nn_thread import NeuralNetworkThread

### DEBUG CONSTANTs
CONFIG_DEBUG_MODE = False

### INFERENCE  CONSTANTS
CONFIG_INFERENCE_TICK_LIVE = 100#3000
CONFIG_INFERENCE_TICK_OFFLINE = 1000# 3000
CONFIG_USE_SAMPLE_DATA = True
CONFIG_OVERWRITE_OUTPUT_FILE = True
CONFIG_INCREMENT_ID = False
CONFIG_STORE_DATASET = False
CONFIG_STORE_DATASET_EVERY_N_SAMPLE = 200
CONFIG_NO_TITLE_BAR = False

### NEURAL NET CONFIG
IMG_SCALE_DIVIDER = 4

### GUI CONSTANTS
IMAGE_LABEL_SIZE_WIDTH = 244*3.5
IMAGE_LABEL_SIZE_HEIGHT = 160*3.5

BUTTON_LABEL_FONT_SIZE = 36
BUTTON_LABEL_FONT_NAME = "Arial"

TEXT_LABEL_FONT_SIZE = 48
TEXT_LABEL_FONT_NAME = "Arial"

IMAGE_WIDGET_FONT_SIZE = 48
IMAGE_WIDGET_FONT_NAME = "Arial"

ABOUT_LABEL_FONT_SIZE = 36
ABOUT_LABEL_FONT_NAME = "Arial"

# SMALL RESOLUTION FILES
# DATASET_PATH= "train/"
# INIT_IMAGE_NAME = "6_2.jpg"
# INIT_IMAGE_PATH = DATASET_PATH + INIT_IMAGE_NAME

# # LARGE RESOLUTION FILES
INIT_IMAGE_PATH = "gui/loading_widget_placeholder.png"

DATASET_PATH= "train_images/"
INIT_IMAGE_NAME = "IMG_197.jpg"
INIT_IMAGE_PATH = DATASET_PATH + INIT_IMAGE_NAME


CAPTURE_PATH = "capture/"
CAPTURE_BASE_NAME = "cam_capture"
CAPTURE_FORMAT = ".jpg"

STORE_DATASET_RANDOM_PREFIX = str(random.randint(0, 1000000000))
STORE_DATASET_PATH = "captured_dataset/" + STORE_DATASET_RANDOM_PREFIX

### ABOUT PAGE CONFIG
NEURAL_NETWORK_TOP_IMAGE_PATH = "gui/neural_net_topology.png"
EXAMPLES_PATH = "gui/examples.png"


### GUI CONSTANTS
IMAGE_LABEL_SIZE_WIDTH = 244*3.5
IMAGE_LABEL_SIZE_HEIGHT = 160*3.5

# BUTTON_LABEL_FONT_SIZE = 36
BUTTON_LABEL_FONT_NAME = "Arial"

# TEXT_LABEL_FONT_SIZE = 48
TEXT_LABEL_FONT_NAME = "Arial"

# IMAGE_WIDGET_FONT_SIZE = 36
IMAGE_WIDGET_FONT_NAME = "Arial"

# ABOUT_LABEL_FONT_SIZE = 36
ABOUT_LABEL_FONT_NAME = "Arial"


LOGO_ARROW_PATH = "gui/logo_arrow-white.png"
LOGO_NXP_PATH= "gui/NXP_logo_RGB_web.jpg"

### ABOUT PAGE CONFIG
NEURAL_NETWORK_TOP_IMAGE_PATH = "gui/neural_net_topology.png"
EXAMPLES_PATH = "gui/examples.png"


background_color = "rgb(24, 24, 24);"
font_name_def = "'Arial'"
font_color_def = "rgb(220, 220, 220);"
font_size_def = str(24)


def _set_font(widget, font_name=font_name_def, font_size=font_size_def, font_color=font_color_def):
    # newfont = QFont(name, size, QFont.Bold)
    # widget.setFont(newfont)
    # #font: bold large 'Arial';
    print("font size:", font_size)

    widget.setStyleSheet("color: " + font_color +
                         "font-family: " + font_name + ";" +
                         "font-size: " + str(font_size) + "px;" +
                         "background-color: " + background_color +
                         "border: none")


class ImageWidget(QWidget):
    def __init__(self, title, image_path, width=IMAGE_LABEL_SIZE_WIDTH, height=IMAGE_LABEL_SIZE_HEIGHT):
        super(ImageWidget, self).__init__()
        self.hor_layout = QVBoxLayout(self)
        self.hor_layout.setAlignment(Qt.AlignCenter)

        if title != "":
            self.text_label = QLabel(title)
            _set_font(self.text_label, IMAGE_WIDGET_FONT_NAME, IMAGE_WIDGET_FONT_SIZE)
            self.hor_layout.addWidget(self.text_label)

        self.width = width
        self.height = height

        self.image_label = QLabel()
        self.set_image(image_path)
        self.hor_layout.addWidget(self.image_label)

    def set_image(self, image_path):
        #TODO: dont spawn a new pixmapevery time, what the hell
        # self.pixmap = QPixmap(image_path)
        self.image = QPixmap(image_path)
        self.image = self.image.scaled(self.width, self.height)
        self.image_label.setPixmap(self.image)

    def set_pixmap(self, pixmap):
        self.image = pixmap
        self.image = self.image.scaled(self.width, self.height)
        self.image_label.setPixmap(self.image)

    def set_image_with_qimage(self, qimage):
        #TODO: dont spawn a new pixmapevery time, what the hell
        # self.pixmap = QPixmap(image_path)
        self.image = QPixmap()
        success = self.image.convertFromImage(qimage)
        print("img instantiated: ", success)
        self.image = self.image.scaled(self.width, self.height)
        self.image_label.setPixmap(self.image)


class TextLabel(QLabel):
    def __init__(self):
        super(TextLabel, self).__init__()
        self.setText("<placeholder>")
        self.setFixedWidth(600)
        _set_font(self, TEXT_LABEL_FONT_NAME, TEXT_LABEL_FONT_SIZE)


class Button(QPushButton):
    def __init__(self, text):
        super(Button, self).__init__()
        self.setText(text)
        self.setFixedHeight(100)
        self.setFixedWidth(400)
        _set_font(self, BUTTON_LABEL_FONT_NAME, BUTTON_LABEL_FONT_SIZE)

    def set_as_disabled(self):
        self.setStyleSheet("background-color: rgb(120, 120, 120)")

    def set_as_enabled(self):
        self.setStyleSheet("background-color: rgb(30, 160, 50)")


class CustomTabWidget(QStackedWidget):
    def __init__(self):
        super(CustomTabWidget, self).__init__()
        # self.setStyleSheet("border-top: 2px solid #C2C7CB;")
        # stylesheet = """
        #     QTabBar::tab:selected {background: red;}
        #     QTabWidget>QWidget>QWidget{background: gray;}
        #     """
        # stylesheet = "QTabWidget::pane {border - top: 2px solid  #C2C7CB};"
        # self.qbar = QTabBar()
        # self.setTabBar(self.qbar)
        # stylesheet = ("background-color: rgb(200, 30, 30)")
        # self.qbar.setStyleSheet(stylesheet)
        _set_font(self, BUTTON_LABEL_FONT_NAME, BUTTON_LABEL_FONT_SIZE)


class BackgroundWidget(QWidget):
    def __init__(self):
        super(BackgroundWidget, self).__init__()
        _set_font(self, BUTTON_LABEL_FONT_NAME, BUTTON_LABEL_FONT_SIZE)


class Dialog(QDialog):
    def __init__(self, use_sample_data, neural_net_thread):
        super(Dialog, self).__init__()
        print("Initiating GUI dialog")

        self.neural_net_thread = neural_net_thread

        # if CONFIG_NO_TITLE_BAR:
        self.setWindowFlags(Qt.FramelessWindowHint)
		# self.showMaximized()
        self.setFixedWidth(1920)
        self.setFixedHeight(1080)
        _set_font(self)

        self.config_use_sample_data = use_sample_data

        tab_widget = CustomTabWidget()
        demo_widget = BackgroundWidget()
        about_widget = BackgroundWidget()
        self.__setup_about_widget(about_widget)
        tab_widget.addWidget(demo_widget)
        tab_widget.addWidget(about_widget)

        dialog_layout = QVBoxLayout()
        self.setLayout(dialog_layout)

        dialog_layout.addWidget(tab_widget)

        mainLayout = QVBoxLayout()
        demo_widget.setLayout(mainLayout)
        self.setLayout(mainLayout)
        self.setWindowTitle("Crowd counting demo using MCDNN")

        # self.resize(500, 550)

        top_label = TextLabel()
        top_label.setFixedWidth(1900)
        top_label.setText("Crowd Counting with Density Maps - Multi-column Deep Neural Network")
        mainLayout.addWidget(top_label)

        # Top images
        top_button_hor_layout = QHBoxLayout()
        mainLayout.addLayout(top_button_hor_layout)
        self.live_but = Button("Live mode")
        self.offline_but = Button("Pre-captured mode")
        top_button_hor_layout.setAlignment(Qt.AlignCenter)
        #TODO: add connecting these buttons to set/reset live mode
        if self.config_use_sample_data:
            self.live_but.set_as_disabled()
            self.offline_but.set_as_enabled()
        else:
            self.live_but.set_as_enabled()
            self.offline_but.set_as_disabled()

        self.live_but.clicked.connect(self.set_mode_live)
        self.offline_but.clicked.connect(self.set_mode_offline)
        top_button_hor_layout.addSpacerItem(QSpacerItem(65, 50))
        top_button_hor_layout.addWidget(self.live_but)
        top_button_hor_layout.addWidget(self.offline_but)
        top_button_hor_layout.setAlignment(Qt.AlignLeft)

        # Images - raw image, dens map
        upper_img_hor_layout = QHBoxLayout()
        mainLayout.addLayout(upper_img_hor_layout)
        # self.raw_image_widget = ImageWidget("Input: Raw Image", INIT_IMAGE_PATH)
        # self.dens_map_widget = ImageWidget("Output: Density Map", INIT_IMAGE_PATH)
        self.raw_image_widget = ImageWidget("", INIT_IMAGE_PATH)
        self.dens_map_widget = ImageWidget("", INIT_IMAGE_PATH)
        upper_img_hor_layout.addWidget(self.raw_image_widget)
        upper_img_hor_layout.addWidget(self.dens_map_widget)

        # Text below images
        lower_label_hor_layout = QHBoxLayout()
        mainLayout.addLayout(lower_label_hor_layout)
        self.date_label = TextLabel()
        self.count_label = TextLabel()
        self.count_label.setFixedWidth(500)
        self.inference_time = TextLabel()
        self.inference_time.setFixedWidth(800)
        lower_label_hor_layout.setAlignment(Qt.AlignCenter)

        lower_label_hor_layout.addWidget(self.count_label)
        # lower_label_hor_layout.addSpacerItem(QSpacerItem(300, 50))
        lower_label_hor_layout.addWidget(self.inference_time)
        # lower_label_hor_layout.addSpacerItem(QSpacerItem(300, 50))
        lower_label_hor_layout.addWidget(self.date_label)

        bottom_panel_widget = QWidget()
        # bottom_panel_widget.setStyleSheet("background-color: rgb(255,255,255)")
        mainLayout.addWidget(bottom_panel_widget)


        bottom_logo_horizontal_lay = QHBoxLayout()
        bottom_logo_horizontal_lay.setAlignment(Qt.AlignRight)
        arrow_logo_widget = ImageWidget("", LOGO_ARROW_PATH, 500, 101)
        bottom_logo_horizontal_lay.addWidget(arrow_logo_widget)
        bottom_panel_widget.setLayout(bottom_logo_horizontal_lay)

        self.__init_timer()

    def __setup_about_widget(self, parent):
        main_widget_layout = QHBoxLayout()
        main_widget_layout.setAlignment(Qt.AlignTop)
        parent.setLayout(main_widget_layout)

        description_layout = QVBoxLayout()
        main_widget_layout.addLayout(description_layout)

        about_section_widget = TextLabel()
        about_section_widget.setText("About")
        description_layout.addWidget(about_section_widget)

        description_widget = TextLabel()
        description_layout.addWidget(description_widget)
        _set_font(description_widget, ABOUT_LABEL_FONT_NAME, ABOUT_LABEL_FONT_SIZE)
        description_widget.setText(""
        "Crowd count estimation\n"
        "Based on work by Zhan et al. 2016, CVPR IEEE:\n"
        "Single-Image Crowd Counting via\n Multi-Column Convolutional Neural Network\n\n"
        "Demo: MCDNN, PyTorch/Tensorflow, Qt, ONNX\n\n"
        "Input: Raw image, a still picture\n\n"
        "Output: Human density map\n\n"
        "The denser the map, the more\nheadcount in specific area\n (brighter -> more people)\n\n"
        "The map is then integrated over\nto get the final headcount\n\n"
        "Live mode:\n"
        "Captures image from camera and\nestimates the headcount\n\n"
        "Pre-captured mode:\n"
        "Estimates headcount using validation\nset from training")

        sample_io_layout = QVBoxLayout()
        main_widget_layout.addLayout(sample_io_layout)
        examples_widget = TextLabel()
        examples_widget.setText("Examples")
        sample_io_layout.addWidget(examples_widget)

        raw_image_widget = ImageWidget("", EXAMPLES_PATH, 250*2, 335*2)
        sample_io_layout.addWidget(raw_image_widget)

        topology_layout = QVBoxLayout()
        main_widget_layout.addLayout(topology_layout)
        mcdnn_text_widget = TextLabel()
        mcdnn_text_widget.setText("Multi-column Deep Neural Network")
        topology_layout.addWidget(mcdnn_text_widget)
        raw_image_widget = ImageWidget("", NEURAL_NETWORK_TOP_IMAGE_PATH)
        topology_layout.addWidget(raw_image_widget)


    def __init_timer(self):
        print("Initializing timers")
        self.timer = QTimer()
        self.timer.timeout.connect(self.__new_frame)
        self.timer.start(CONFIG_INFERENCE_TICK_OFFLINE)

    def __new_frame(self):
        print("#################")
        print("APP> ITERATION > START")
        lock_status = self.neural_net_thread.acquire_lock()
        print("APP> lock status:", lock_status)
        if lock_status:
            iter_count, nn_output = self.neural_net_thread.get_new_results()
            if iter_count > 0:
                self.set_new_frame(nn_output)
            self.neural_net_thread.release_lock()
        else:
            print("APP> neural network still busy")
        print("APP> ITERATION > END")

    def set_mode_live(self):
        if self.config_use_sample_data is True:
            self.timer.stop()
            print("# # # # # # # # #")
            print("SWITCHING MODE > LIVE")
            print("# # # # # # # # #")
            self.config_use_sample_data = False
            self.timer.start(CONFIG_INFERENCE_TICK_LIVE)
            self.live_but.set_as_enabled()
            self.offline_but.set_as_disabled()
            self.neural_net_thread.set_mode_live_mode(True)
        else:
            print("### Warning: live mode already selected")

    def set_mode_offline(self):
        if self.config_use_sample_data is False:
            self.timer.stop()
            print("# # # # # # # # #")
            print("SWITCHING MODE > DATASET")
            print("# # # # # # # # #")
            self.config_use_sample_data = True
            self.timer.start(CONFIG_INFERENCE_TICK_OFFLINE)
            self.live_but.set_as_disabled()
            self.offline_but.set_as_enabled()
            self.neural_net_thread.set_mode_live_mode(False)
        else:
            print("### Warning: dataset mode already selected")

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_L:
            self.set_mode_live()
        elif event.key() == Qt.Key_O:
            self.set_mode_offline()
        if event.key() == Qt.Key_Escape:
            sys.exit(dialog.exec_())
        time.sleep(1)

    def set_new_frame(self, nn_output_dict):
        print("APP> raw neural net output: ", nn_output_dict)
        # Setting new widget images
        self.raw_image_widget.set_pixmap(nn_output_dict['input_pixmap'])
        self.dens_map_widget.set_pixmap(nn_output_dict['output_pixmap'])

        # Setting new text values
        self.count_label.setText("People count: " + str(round(nn_output_dict['headcount'], 0)))
        print("APP> >>>>>>>>>>>>HEAD COUNTS")
        print("APP> HEAD COUNT TENSORFLOW QT ONLY ", nn_output_dict['headcount'], 'shape: ', nn_output_dict['dens_map_dim'])
        self.inference_time.setText("Inference time:" + str(round(nn_output_dict['inference_time'], 2)) + "ms")
        self.date_label.setText(time.strftime("%b %d %Y %H:%M:%S", time.gmtime(time.time())))


class CrowdCountApp():
    def __init__(self, dialog_handle):
        self.dialog_handle = dialog_handle
        print("Initiating main app")


if __name__ == '__main__':
    # construct the argument parse and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-v", "--videosrc", type=str, default="/dev/video0",
                    help="video device node entry (for usb web camera) or gstreamer pipeline (for mazzanine camera)")
    args = vars(ap.parse_args())

    app = QApplication(sys.argv)
    nn_thread_handle = NeuralNetworkThread(DATASET_PATH, "test_img.jpg", video_src = args["videosrc"], use_cv=True, use_qt_only=True)
    nn_thread_handle.daemon = True
    nn_thread_handle.start()
    # nn_thread_handle = None
    dialog = Dialog(CONFIG_USE_SAMPLE_DATA, nn_thread_handle)

    crowd_app = CrowdCountApp(dialog)

    sys.exit(dialog.exec_())
