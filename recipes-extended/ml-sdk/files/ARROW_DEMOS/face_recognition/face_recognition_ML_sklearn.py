# Face recognition using deep learning and scikit-learn/opencv
# We will follow below sequence:
# 1. Detect faces
# 2. Compute 128-d face embeddings to quantify a face
# 3. Train a Support Vector Machine (SVM) on top of the embeddings
# 4. Recognize faces in video streams

# Description : we will detect face using pre-trained caffe model. The model is already trained on so many positive
# and negative images to detect faces.
# For computing 128-d face embedding we use A Torch deep learning openface model .
# Then we will train our model using scikit learn SVM (Support Vector Machine) algorithm.

from __future__ import print_function

import os
import numpy as np
import cv2
import pickle
import time
import argparse
import shutil
from distutils.dir_util import copy_tree
from imutils.video import WebcamVideoStream, VideoStream
from imutils.video import FPS
import imutils
from sklearn.preprocessing import LabelEncoder
from sklearn.svm import SVC

inWidth = 300
inHeight = 300
faceThreshold = 0.7
MIN_CONFIDENCE = 0.5
MAX_TRAINING_IMAGES = 100

prototxt = 'face_detection_model/deploy.prototxt'
caffemodel = 'face_detection_model/res10_300x300_ssd_iter_140000.caffemodel'
embedding_model = 'face_detection_model/openface_nn4.small2.v1.t7'

dataset = 'training_data'

recognizer_filename = 'recognizer_sklearn.pickle'
labels_filename = 'labels_sklearn.pickle'

timestr = time.strftime("%Y%m%d-%H%M%S")


# Identify face location in the given image
def detect_faces(image):
    (h, w) = image.shape[:2]

    if h > inHeight and w > inWidth:
        interpolation = cv2.INTER_AREA
    else:
        interpolation = cv2.INTER_LINEAR

    # crust image blob and set input
    detector.setInput(
        cv2.dnn.blobFromImage(cv2.resize(image, (inWidth, inHeight), interpolation=interpolation), 1.0,
                              (inWidth, inHeight), (104.0, 177.0, 123.0), False, False))

    # apply OpenCV's deep learning-based face detector to localize
    # faces in the input image
    detections = detector.forward()

    return detections


# capture atleast MAX_TRAINING_IMAGES photos for given label. This data set is used for retrain model.
def capture_new_training_set(label):
    # initialize the video stream, then allow the camera sensor to warm up
    print("Starting video stream...")
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

        cv2.imshow("Capture Test Images For Training. Press ESC to exit", frame)

        key = cv2.waitKey(300) & 0xFF

        # if the `q` key was pressed, break from the loop
        if key == ord("q"):
            print("`q` pressed, Exiting...")
            break

        total_faces = 0
        detections = detect_faces(frame)

        for i in range(0, detections.shape[2]):
            # get confidence of face detection
            confidence = detections[0, 0, i, 2]

            if confidence > faceThreshold:
                total_faces += 1

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

        fps.update()

    fps.stop()
    print("Total Elapsed time: {:.2f} sec".format(fps.elapsed()))
    print("Approx. FPS: {:.2f}".format(fps.fps()))
    cam.stop()
    cv2.destroyAllWindows()


# obtain the 128-d quantification of the face
def gen_face_vector(face_image):
    # construct a blob for the face ROI, then pass the blob through our face embedding model
    # to obtain the 128-d quantification of the face

    embedder.setInput(
        cv2.dnn.blobFromImage(face_image, 1.0 / 255, (96, 96), (0, 0, 0), swapRB=True, crop=False))
    vec = embedder.forward()

    # return 128-d quantification vector for particular face
    return vec


# Embedded face (obtain the 128-d quantification of the face) from each photos and save for training.
def embedded_faces():
    # initialize our lists of extracted facial embeddings and respective names
    knownEmbeddings = []
    knownNames = []
    dirLabels = []  # this list only contains image directory names

    # initialize the total number of faces processed
    total_faces = 0

    # get path of input images
    print("Quantifying faces from training dataset...")

    train_start_time = time.time()

    # get the directories (one directory for each subject) in data folder
    image_dirs = os.listdir(dataset)

    print("image dirs = ", image_dirs)

    # let's go through each directory and read images within it
    for dir_index, dir_name in enumerate(image_dirs):
        # ignore any non-relevant directories if any like hidden directory
        if dir_name.startswith("."):
            continue

        # extract label number of subject from dir_name
        if dir_name not in dirLabels:
            dirLabels.append(dir_name)

            # build path of directory containing images for current subject subject
            # sample subject_dir_path = "training-data/anil"
            subject_dir_path = dataset + "/" + dir_name

            # get the images names that are inside the given subject directory
            subject_images_names = os.listdir(subject_dir_path)

            # go through each image name, read image,
            # detect face and add face to list of faces
            for image_name in subject_images_names:

                # ignore system files like .DS_Store
                if image_name.startswith("."):
                    continue

                # build image path
                # sample image path = training-data/anil/1.png
                image_path = subject_dir_path + "/" + image_name

                print("Processing Image : ", image_path)

                # read image
                image = cv2.imread(image_path)

                (h, w) = image.shape[:2]

                detections = detect_faces(image)

                # ensure at least one face was found
                if len(detections) > 0:
                    # we're making the assumption that each image has only ONE
                    # face, so find the bounding box with the largest probability
                    i = np.argmax(detections[0, 0, :, 2])
                    confidence = detections[0, 0, i, 2]

                    # Compare confidence level with threshold value and neglect if confidence is low.
                    if confidence > faceThreshold:
                        # compute the (x, y)-coordinates of the bounding box for the face
                        box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                        (startX, startY, endX, endY) = box.astype("int")

                        # extract the face ROI and grab the ROI dimensions
                        face = image[startY:endY, startX:endX]
                        (fH, fW) = face.shape[:2]

                        # ensure the face width and height are sufficiently large
                        if fW < 50 or fH < 50:
                            continue

                        face_vec = gen_face_vector(face)

                        # add the name of the person + corresponding face embedding to their respective lists
                        knownNames.append(dir_name)
                        knownEmbeddings.append(face_vec.flatten())
                        total_faces += 1

    # dump the facial embeddings + names to disk
    print("serializing {} faces encodings...".format(total_faces))
    data = {"embeddings": knownEmbeddings, "names": knownNames}

    train_model(data)

    train_end_time = time.time()

    print("Total Elapsed time for training on {} encoding  is {:.2f} sec".format(total_faces,
                                                                                 (train_end_time - train_start_time)))


def train_model(data):
    print("Starting training process")

    # encode the labels
    print("Encoding labels...")
    le = LabelEncoder()
    labels = le.fit_transform(data["names"])

    # train the model used to accept the 128-d embeddings of the face and
    # then produce the actual face recognition
    print("Training model using scikit learn SVM...")
    recognizer = SVC(C=1.0, kernel="linear", probability=True)
    recognizer.fit(data["embeddings"], labels)

    # write the actual face recognition model to disk
    f = open(recognizer_filename, "wb")
    f.write(pickle.dumps(recognizer))
    f.close()

    # write the label encoder to disk
    f = open(labels_filename, "wb")
    f.write(pickle.dumps(le))
    f.close()


def recognize_faces():
    # load the actual face recognition model along with the label encoder
    recognizer = pickle.loads(open(recognizer_filename, "rb").read())
    le = pickle.loads(open(labels_filename, "rb").read())

    # initialize the video stream, then allow the camera sensor to warm up
    print("Starting video stream...")
    # vs = WebcamVideoStream(src=args["videosrc"]).start()
    camera_source = int(args["videosrc"]) if len(args["videosrc"]) == 1 else str(args["videosrc"])
    # cam = WebcamVideoStream(src=camera_source).start()
    vs = VideoStream(src=camera_source).start()
    time.sleep(1.0)

    # start the FPS throughput estimator
    fps = FPS().start()

    # loop over frames from the video file stream
    while True:
        # grab the frame from the threaded video stream
        frame = vs.read()

        # if we are unable to get video view, exit from program.
        if frame is None:
            print("Unable to get video frame. Please check video source.")
            break

        # resize the frame to have a width of 640 pixels
        frame = imutils.resize(frame, width=640)
        (h, w) = frame.shape[:2]

        # construct a blob from the image
        imageBlob = cv2.dnn.blobFromImage(
            cv2.resize(frame, (300, 300)), 1.0, (300, 300), (104.0, 177.0, 123.0), swapRB=False, crop=False)

        # apply OpenCV's deep learning-based face detector to localize
        # faces in the input image
        detector.setInput(imageBlob)
        detections = detector.forward()

        # loop over the detections
        for i in range(0, detections.shape[2]):
            # extract the confidence (i.e., probability) associated with
            # the prediction
            confidence = detections[0, 0, i, 2]

            # filter out weak detections
            if confidence > faceThreshold:
                # compute the (x, y)-coordinates of the bounding box for
                # the face
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                (startX, startY, endX, endY) = box.astype("int")

                # extract the face ROI
                face = frame[startY:endY, startX:endX]
                (fH, fW) = face.shape[:2]

                # ensure the face width and height are sufficiently large
                if fW < 20 or fH < 20:
                    continue

                # construct a blob for the face ROI, then pass the blob
                # through our face embedding model to obtain the 128-d
                # quantification of the face
                faceBlob = cv2.dnn.blobFromImage(face, 1.0 / 255,
                                                 (96, 96), (0, 0, 0), swapRB=True, crop=False)
                embedder.setInput(faceBlob)
                vec = embedder.forward()

                # perform classification to recognize the face
                preds = recognizer.predict_proba(vec)[0]
                j = np.argmax(preds)
                proba = preds[j]
                name = le.classes_[j]

                # draw the bounding box of the face along with the
                # associated probability

                if proba > MIN_CONFIDENCE:
                    text = "{}: {:.2f}%".format(name, proba * 100)
                else:
                    text = "unknown"

                y = startY - 10 if startY - 10 > 10 else startY + 10
                cv2.rectangle(frame, (startX, startY), (endX, endY),
                              (0, 0, 255), 2)
                cv2.putText(frame, text, (startX, y),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)

        # show the output frame
        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1) & 0xFF

        # if the `q` key was pressed, break from the loop
        if key == ord("q"):
            print("`q` pressed, Exiting...")
            break

        # update the FPS counter
        fps.update()

    # stop the timer and display FPS information
    fps.stop()
    vs.stop()
    # do a bit of cleanup
    cv2.destroyAllWindows()
    print("Total Elapsed time: {:.2f} sec".format(fps.elapsed()))
    print("Approx. FPS: {:.2f}".format(fps.fps()))


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

        embedded_faces()
    else:
        recognize_faces()


if __name__ == '__main__':
    print('Initializing Face recognition model...')

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

    detector = cv2.dnn.readNetFromCaffe(prototxt, caffemodel)

    embedder = cv2.dnn.readNetFromTorch(embedding_model)

    main()
