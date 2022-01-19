import time

import tensorflow as tf
from tensorflow.python.platform import gfile
import numpy as np

from PyQt5.QtGui import QImage, QPixmap

input_y = 0
input_x = 0
output_path = 'output/density_map_tf.png'


TENSORFLOW_USE_CUDA = False
TENSORFLOW_VERSION = 1.4
print("NN> using tensorflow version: ", TENSORFLOW_VERSION)
if TENSORFLOW_USE_CUDA:
    print("NN> using CUDA acceleration with tensorflow-gpu")
else:
    print("NN> using CPU-only (NO CUDA) with tensorflow")
time.sleep(1)


if TENSORFLOW_VERSION == 1.4:
    # For i.MX 8M that only supports 1.4 in our case
    model_160x120_path = "model/tf1.4_crowd_count_160x120.pb"
    model_640x480_path = "model/tf1.4_crowd_count_640x480.pb"
else:
    if TENSORFLOW_USE_CUDA:
        model_160x120_path = "model/tf1.11_crowd_count_160x120_gpu.pb"
        model_640x480_path = "model/tf1.11_crowd_count_640x480_gpu.pb"
    else:
        # Use the latest
        model_160x120_path = "model/tf1.11_crowd_count_160x120.pb"
        model_640x480_path = "model/tf1.11_crowd_count_640x480.pb"


def get_image_qt(img_path):
    print("QT LOAD> loading image using QT STARTED")
    channels_count = 1
    qimage = QImage(img_path) # TODO: For some weird reason, if this is not *just declared*, then this thread crashes
    full_pixmap = QPixmap(img_path)
    pixmap = full_pixmap
    print("QT LOAD> Qt input pixmap size (pre-scaling): ", pixmap.size())
    pixmap = pixmap.scaled(input_x, input_y)
    image = pixmap.toImage().convertToFormat(QImage.Format_Grayscale8)
    pixmap = QPixmap.fromImage(image)
    bytes_per_pixel = int(image.depth() / 8)
    b = image.bits()
    print("QT LOAD> Qt input pixmap size (post-scaling):", pixmap.size())
    # sip.voidptr must know size to support python buffer interface
    b.setsize(pixmap.height() * pixmap.width() * channels_count * bytes_per_pixel)
    arr = np.frombuffer(b, np.uint8).reshape((1, 1, pixmap.height(), pixmap.width()))
    print("QT LOAD> numpy array shape:", arr.shape)
    return arr, full_pixmap


def set_image_resolution(rescale_to_640x480=True):
    global input_x
    global input_y
    if rescale_to_640x480:
        print("TF> using 640x480 resolution")
        input_x = 640
        input_y = 480
    else:
        print("TF> using 160x120 resolution")
        input_x = 160
        input_y = 120


def get_pixmap_from_arr(arr):
    print("QT LOAD> QPixmap -> numpy array STARTED")
    im_np = arr.astype(np.uint8)
    qimage = QImage(im_np, im_np.shape[1], im_np.shape[0], QImage.Format_Grayscale8)
    pixmap = QPixmap(qimage)
    return pixmap


def process_predictions(density_map, downscale_dens_map=False):
    print("TF> inference results processing STARTED")
    print("TF> HEADCOUNT TF prior to resizing", np.sum(density_map))

    if downscale_dens_map:
        print("TF> downscaling density map (used in live mode for more visual cues)")
        size_y = int(input_y / 4)
        size_x = int(input_x / 4)
        density_map = density_map.reshape((size_y, size_x))
        M, N = density_map.shape
        # print(density_map.shape)
        K = 4
        L = 4
        MK = M // K
        NL = N // L
        density_map = density_map[:MK * K, :NL * L].reshape(MK, K, NL, L).mean(axis=(1, 3))
    else:
        size_y = int(input_y / 4)
        size_x = int(input_x / 4)
        density_map = density_map.reshape((size_y, size_x))

    et_count = np.sum(density_map)
    print("TF> HEADCOUNT TF after resizing", et_count)

    density_map /= np.max(np.abs(density_map))
    density_map *= (255.0 / density_map.max())
    density_map = np.floor(density_map)

    print("TF> output density map shape:" , density_map.shape)
    # img = Image.fromarray(density_map).convert("L")
    # img.save(output_path)

    # print(density_map)
    # density_map = density_map.flatten()
    # print(density_map)
    # density_map =
    # qimage = QImage(density_map, 120, 160, QImage.Format_Grayscale8)
    # image = image.convertToFormat(QImage.Format_Grayscale8)
    # pixmap = QPixmap.fromImage(image)
    return et_count, density_map


def get_session(use_640x480_sess=True):
    if use_640x480_sess:
        print("TF> using 640x480 session")
        return persisted_sess_640x480
    else:
        print("TF> using 160x120 session")
        return persisted_sess_160x120


def run_inference_on_image(img_path, use_640x480_sess=True, use_qt_only=False, downscale_dens_map=False):
    persisted_sess = get_session(use_640x480_sess)
    tf.compat.v1.reset_default_graph()
    persisted_sess_160x120.graph.as_default()
    set_image_resolution(use_640x480_sess)
    if use_640x480_sess:
         softmax_tensor = persisted_sess.graph.get_tensor_by_name(
             'Relu_12:0')  # this is the max but output is in minus, but kinda correct
    else:
        softmax_tensor = persisted_sess.graph.get_tensor_by_name(
            'Relu_12:0')  # this is the max but output is in minus, but kinda correct
    if use_qt_only:
        np_img_array, input_pixmap = get_image_qt(img_path)
    else:
        # TODO: fix this, currently does not work, our distro did not have support for Pillow so this was not supported
        from PIL import Image
        img = Image.open(img_path).convert('L')
        img = img.resize((input_x, input_y))
        image = np.array(img).reshape(1, 1, input_y, input_x)
        # image = img_loader.load_image_using_qt(img_path)
        # image = np.array(image).reshape(1, 1, image.width(), image.height())
        np_img_array = image

    print("TF> inference STARTED")
    start = time.time()
    if use_640x480_sess:
        #output = persisted_sess.run(softmax_tensor, {'import/0:0': np_img_array})
        output = persisted_sess.run(softmax_tensor, {'0:0': np_img_array})
    else:
        output = persisted_sess.run(softmax_tensor, {'0:0': np_img_array})
    inference_time = round(((time.time() - start) * 1000), 2)
    print("TF> DONE, inference total time:", inference_time)
    headcount, dens_map = process_predictions(output, downscale_dens_map)
    pixmap = get_pixmap_from_arr(dens_map)
    nn_dict = {"image_path": img_path, "output_path": output_path, "headcount": headcount,
               'inference_time': inference_time, 'dens_map_dim': dens_map.shape, 'output_pixmap': pixmap,
               'input_pixmap': input_pixmap}
    return nn_dict


def print_information_about_graph_ops_and_tensors(persisted_sess):
    print("####### TRAINABLE VARIABLES, this are empty because this is protobuf and no training?")
    print(tf.get_collection(tf.GraphKeys.TRAINABLE_VARIABLES))

    print("Last operation in session: ", persisted_sess.graph.get_operations()[-1])

    for op in persisted_sess.graph.get_operations():
       print("####### OPERATION")
       print(op)
    # for op in tf.get_default_graph().get_operations():
    #     print("###### OPERATION NAME")
    #     print(str(op.name))
    # for op in tf.get_default_graph().get_operations():
    #     print("###### OPERATION VALUES - EACH VALUE IS A TENSOR, FIRST = input, LAST = softmax/output")
    #     print(str(op.values)) # NOTE THE DIFFERENCE
    #     print(str(op.values())) # this, the last tensor, has to be usually used with sess.run!
    op_values = [op.values() for op in tf.get_default_graph().get_operations()]
    for values in op_values:
        for each in values:
            print("###### OPERATION VALUES NAMES AKA TENSOR NAMES FIRST = input, LAST = softmax/output")
            print(each.name)

    # op_values = [op.values() for op in persisted_sess.graph.get_operations()]
    # for values in op_values:
    #     for each in values:
    #         print("###### OPERATION VALUES NAMES AKA TENSOR NAMES FIRST = input, LAST = softmax/output")
    #         print(each.name)


print("##### LOADING TENSORFLOW GRAPH")
print("##### 160x120 used for live mode as these typically are close")
print("##### 640x480 used for pre-captured large images of crowd as these are far")

with gfile.FastGFile(model_160x120_path, 'rb') as f:
    graph_def_160x120 = tf.compat.v1.GraphDef()
    graph_def_160x120.ParseFromString(f.read())
    # tf.import_graph_def(graph_def_160x120)
    graph = tf.import_graph_def(graph_def_160x120, name='160x120')
    persisted_sess_160x120 = tf.compat.v1.Session(graph)
    persisted_sess_160x120.graph.as_default()
    tf.compat.v1.reset_default_graph()

with gfile.FastGFile(model_640x480_path, 'rb') as f:
    graph_def_640x480 = tf.compat.v1.GraphDef()
    graph_def_640x480.ParseFromString(f.read())
    graph_640x480 = tf.import_graph_def(graph_def_640x480, name='')
    graph2 = tf.import_graph_def(graph_def_640x480, name='640x480')
    persisted_sess_640x480 = tf.compat.v1.Session(graph2)

tf.compat.v1.reset_default_graph()
persisted_sess_160x120.graph.as_default()
set_image_resolution(rescale_to_640x480=True)
