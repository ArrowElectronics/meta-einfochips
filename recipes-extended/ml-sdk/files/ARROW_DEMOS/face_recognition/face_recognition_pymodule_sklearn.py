#!/usr/bin/python3

# face recognition using python package "face_recognition" and Scikit learn SVM module.
# This is a demo of running face recognition on a camera video output frame.
# Here we find encoding of faces using "face_recognition" package and train this data on SVM.


# import the necessary packages
from __future__ import print_function

import numpy
import face_recognition
import argparse
import glob
import pickle
import cv2
import os
import time
import imutils
import shutil
from distutils.dir_util import copy_tree
from imutils.video import WebcamVideoStream, VideoStream
from imutils.video import FPS
import multiprocessing
import concurrent.futures
from sklearn.preprocessing import LabelEncoder
from sklearn.svm import SVC

dataset = 'training_data'

recognizer_filename = 'recognizer_sklearn_pymodule.pickle'
labels_filename = 'labels_sklearn_pymodule.pickle'

MIN_CONFIDENCE = 0.4
MAX_TRAINING_IMAGES = 50

timestr = time.strftime("%Y%m%d-%H%M%S")


# capture atleast MAX_TRAINING_IMAGES photos for given label. This data set is used for retrain model.
def capture_new_training_set(label):
    # initialize the video stream, then allow the camera sensor to warm up
    print("Starting video stream to capture new training dataset...")
    camera_source = int(args["videosrc"]) if len(args["videosrc"]) == 1 else str(args["videosrc"])
    # cam = WebcamVideoStream(src=camera_source).start()
    cam = VideoStream(src=camera_source).start()
    time.sleep(1.0)

    # start the FPS throughput estimator
    fps = FPS().start()

    img_counter = 0

    while True:

        frame = cam.read()

        # if we are unable to get video view, exit from program.
        if frame is None:
            print("Unable to get video frame. Please check video source.")
            break

        frame = imutils.resize(frame, width=640)

        cv2.imshow("Capture Test Images For Training. Press q to exit", frame)

        key = cv2.waitKey(300) & 0xFF

        # if the `q` key was pressed, break from the loop
        if key == ord("q"):
            print("`q` pressed, Exiting...")
            break

        # Identify face location in the given image

        # load the input image and convert it from BGR (OpenCV ordering)
        # to dlib ordering (RGB)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # detect the (x, y)-coordinates of the bounding boxes
        # corresponding to each face in the input image
        boxes = face_recognition.face_locations(rgb)

        print(boxes)
        total_faces = len(boxes)
        print("detected faces - ", total_faces)

        # ensure at least one face was found
        if total_faces == 1:

            # now image has only one face. So save frame

            img_name = "{}_{}_{}.png".format(label, img_counter, timestr)

            cv2.imwrite(os.path.join(label, img_name), frame)

            print("new training image {} saved!".format(img_name))
            img_counter += 1

            if img_counter > MAX_TRAINING_IMAGES:
                print('Max Training images capture. so closing...')
                break

        elif total_faces > 1:
            print('More than one face found. Please provide only {} face image.'.format(label))

    fps.stop()
    print("Total Elapsed time: {:.2f} sec".format(fps.elapsed()))
    cam.stop()
    cv2.destroyAllWindows()


def recognize_faces_process(inputQueues, outputQueues):
    # wait for some times to load first image
    time.sleep(1.0)

    rgb_image = []
    while True:

        if not inputQueues.empty():
            rgb_image = inputQueues.get()

        if rgb_image is not None:

            # detect the (x, y)-coordinates of the bounding boxes
            # corresponding to each face in the input frame, then compute
            # the facial embeddings for each face
            boxes = face_recognition.face_locations(rgb_image)
            encodings = face_recognition.face_encodings(rgb_image, boxes)

            outputQueues.put((boxes, encodings))


def encode_faces_from_image(img_path):
    print("Processing Image : ", img_path)

    # load the input image and convert it from BGR (OpenCV ordering)
    # to dlib ordering (RGB)
    image = cv2.imread(img_path)

    (h, w) = image.shape[:2]

    # resize frame to have a maximum of 640 X 480 pixels
    if w > 640:
        image = imutils.resize(image, width=640)

    if h > 480:
        image = imutils.resize(image, height=480)

    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # detect the (x, y)-coordinates of the bounding boxes
    # corresponding to each face in the input image
    boxes = face_recognition.face_locations(rgb)

    # compute the facial embedding for the face
    encodings = face_recognition.face_encodings(rgb, boxes)

    return encodings


def train_model(data):
    print("Start Training model using encoding of faces and SVM (support vector machine)...")

    # encode the labels
    print("Encoding labels...")
    le = LabelEncoder()
    labels = le.fit_transform(data["names"])

    # train the model used to accept the 128-d encodings of the face and
    # then produce the actual face recognition
    recognizer = SVC(C=1.0, kernel="linear", probability=True)
    recognizer.fit(data["encodings"], labels)

    # write the actual face recognition model to disk
    f = open(recognizer_filename, "wb")
    f.write(pickle.dumps(recognizer))
    f.close()

    # write the label encoder to disk
    f = open(labels_filename, "wb")
    f.write(pickle.dumps(le))
    f.close()


def encode_faces():
    # grab the paths to the input images in our dataset
    print("Quantifying faces from training dataset...")
    # imagePaths = list(paths.list_images(dataset))

    # capture start time
    training_starttime = time.time()

    # initialize the list of known encodings and known names
    allKnownEncodings = []
    allKnownNames = []

    # get the directories (one directory for each subject) in data folder
    image_dirs = os.listdir(dataset)

    # let's go through each directory and read images within it
    for dir_name in image_dirs:
        # ignore any non-relevant directories if any like hidden directory
        if dir_name.startswith("."):
            continue

        # extract label number of subject from dir_name
        name = dir_name

        # build path of directory containing images for current subject subject
        # sample subject_dir_path = "training-data/anil"
        subject_dir_path = dataset + "/" + dir_name

        # get the images names that are inside the given subject directory
        # All supported image extension should be add here
        subject_images_names = glob.glob(subject_dir_path + "/*.JPG")
        subject_images_names += glob.glob(subject_dir_path + "/*.jpg")
        subject_images_names += glob.glob(subject_dir_path + "/*.png")

        # go through each image name, read image,
        # detect face and add face to list of faces

        encodings=[]

        # Create a pool of processes. By default, one is created for each CPU in your machine.
        with concurrent.futures.ProcessPoolExecutor(max_workers=4) as executor:

            # Process the list of files, but split the work across the process pool to use all CPUs!
            for image_name, encodings in zip(subject_images_names,
                                             executor.map(encode_faces_from_image, subject_images_names)):
                print("Encoding done for image = " + image_name)
                # loop over the encodings
                for encoding in encodings:
                    # add each encoding + name to our set of known names and
                    # encodings
                    allKnownEncodings.append(encoding)
                    allKnownNames.append(name)

    data = {"encodings": allKnownEncodings, "names": allKnownNames}

    train_model(data)

    training_endtime = time.time()

    print("Total Elapsed time for training : {:.2f} sec".format(training_endtime - training_starttime))


def recognize_faces():
    # initialize our list of queues --
    # input Queue contains one frame that need to be process
    # output Queue contains detections of latest given input frame
    inputQueues = multiprocessing.Queue(maxsize=1)
    outputQueues = multiprocessing.Queue(maxsize=1)

    # load the actual face recognition model along with the label encoder
    recognizer = pickle.loads(open(recognizer_filename, "rb").read())
    le = pickle.loads(open(labels_filename, "rb").read())

    print("Starting face recognition using camera...")

    # initialize the video stream, allow the cammera sensor to warmup,
    # and initialize the FPS counter
    print("Starting video stream...")
    # vs = WebcamVideoStream(args["videosrc"]).start()
    camera_source = int(args["videosrc"]) if len(args["videosrc"]) == 1 else str(args["videosrc"])
    vs = VideoStream(src=camera_source).start()
    time.sleep(1.0)

    if not vs.grabbed:
        print("Unable to get video frame. Please check video source.")
        return

    fps = FPS().start()

    print("Initialized Face Recognition process as daemon...")
    fr_process = multiprocessing.Process(target=recognize_faces_process, args=(inputQueues, outputQueues))
    fr_process.daemon = True
    fr_process.start()

    # initialized some variables.
    boxes = []
    encodings = []

    # loop over the frames from the video stream
    while True:
        # grab the frame from the threaded video stream 
        frame = vs.read()

        # if we are unable to get video view, exit from program.
        if frame is None:
            print("Unable to get video frame. Please check video source.")
            break

        # resize frame to have a maximum width of 640 pixels
        frame = imutils.resize(frame, width=640)

        # convert the input frame from BGR to RGB
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # r = frame.shape[1] / float(rgb.shape[1])

        if not inputQueues.full():
            inputQueues.put(rgb)

        if not outputQueues.empty():
            boxes, encodings = outputQueues.get()

        names = []

        # loop over the facial encodings
        for encoding in encodings:
            # perform classification to recognize the face
            preds = recognizer.predict_proba(encoding.reshape(1,-1))[0]
            j = numpy.argmax(preds)
            proba = preds[j]
            pred_name = le.classes_[j]

            if proba > MIN_CONFIDENCE:
                name = "{}: {:.2f}%".format(pred_name, proba * 100)
            else:
                name = "unknown"

            # update the list of names
            names.append(name)

        # loop over the recognized faces
        for ((top, right, bottom, left), name) in zip(boxes, names):
            # rescale the face coordinates
            # top = int(top * r)
            # right = int(right * r)
            # bottom = int(bottom * r)
            # left = int(left * r)

            # draw the predicted face name on the image
            cv2.rectangle(frame, (left, top), (right, bottom),
                          (0, 255, 0), 2)

            # draw the bounding box of the face along with the
            # associated probability
            y = top - 15 if top - 15 > 15 else top + 15
            cv2.putText(frame, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX,
                        0.75, (0, 255, 0), 2)

        # Display output frame
        cv2.imshow("Face Recognition Demo. Press q to exit", frame)

        key = cv2.waitKey(1) & 0xFF

        # if the `q` key was pressed, break from the loop
        if key == ord("q"):
            print("`q` pressed, Exiting...")
            break

    fps.stop()
    print("Total Elapsed time: {:.2f} sec".format(fps.elapsed()))
    vs.stop()

    cv2.destroyAllWindows()


def main():
    if args["run"].lower() == 'train':
        if args["label"] is not None:
            label = args["label"].lower()

            # Create target Directory if don't exist
            if not os.path.exists(label):
                os.mkdir(label)
                print("Directory {} created".format(label))
            else:
                print("Directory {} already exists ".format(label))

            capture_new_training_set(label)

            src_dir = label

            if not os.path.exists(os.path.join(dataset, label)):
                os.mkdir(os.path.join(dataset, label))

            dst_dir = os.path.join(dataset, label)

            copy_tree(src_dir, dst_dir)

            # remove our temporary created directory if exist
            if os.path.exists(label):
                shutil.rmtree(label)
                print("Directory {} removed".format(label))
            else:
                print("Directory {} not exists ".format(label))

        encode_faces()

    else:
        recognize_faces()


if __name__ == '__main__':
    # construct the argument parser and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-r", "--run", type=str, default="test",
                    help="face detection model use for `train` or `test`. Please provide input.")
    ap.add_argument("-l", "--label", type=str, default=None,
                    help="Label to create new training dataset and train on it.")
    ap.add_argument("-v", "--videosrc", type=str, default="/dev/video0",
                    help="provide video source (device index of camera i.e. /dev/video5 "
                         "or v4l2 command for mazzanine camera)")

    args = vars(ap.parse_args())

    main()
