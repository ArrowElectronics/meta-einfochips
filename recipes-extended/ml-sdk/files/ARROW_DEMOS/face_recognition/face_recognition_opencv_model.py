# # Face Detection In Python Using OpenCV

# `OpenCV` contains many pre-trained classifiers for face, eyes, smile etc. The XML files of pre-trained classifiers
# are stored in `opencv/data/`. For face detection specifically, there are two pre-trained classifiers:
# 
# 1. Haar Cascade Classifier
# 2. LBP Cascade Classifier
#
# Each OpenCV face detection classifier has its own pros and cons but the major differences are in accuracy and
# speed. So in a use case where more accurate detections are required, `Haar` classifier is more suitable like in
# security systems, while `LBP` classifier is faster than Haar classifier and due to its fast speed, it is more
# preferable in applications where speed is important like in mobile applications or embedded systems.

# import required libraries
from __future__ import print_function

import numpy as np
import cv2
import os
import argparse
import pickle
import time
import imutils
from imutils.video import WebcamVideoStream
from imutils.video import FPS
import shutil
from distutils.dir_util import copy_tree

# As low the value, higher is detection
# Choose this value wisely by trial and error
MAX_CONFIDENCE = 60
inWidth = 300
inHeight = 300
faceThreshold = 0.7
MAX_TRAINING_IMAGES = 50

dataset = 'training_data'

trainned_model_name = 'opencv_face_trainned_model.yml'

subject_labels = 'Labels.pickle'

timestr = time.strftime("%Y%m%d-%H%M%S")


# function to detect face and draw rectangle for detected face for recognition
# And for training only detect largest face
# This function is useful for webcam face detection as well as for training
def detect_faces(image, isForTraining=False):
    # img_copy = np.copy(colored_img)
    # convert the test image to gray image as opencv face detector expects gray images
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # let's detect multiscale (some images may be closer to camera than others) images
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=4, minSize=(30, 30),
                                          flags=cv2.CASCADE_SCALE_IMAGE)

    # if no face detected then return None
    if len(faces) == 0:
        return None, None

    print("Found {} face/s".format(len(faces)))

    if not isForTraining:
        # go over list of faces and draw them as rectangles on original colored img
        for (x, y, w, h) in faces:
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

        return image, faces
    else:
        # under the assumption that there will be only one face,
        # extract the face area
        (x, y, w, h) = faces[0]
        # return only face cropped image and co-ordinates
        return gray[y:y + w, x:x + h], faces[0]


# this function will read all persons' training images, detect face from each image
# and will return two lists of exactly same size, one list
# of faces and another list of labels for each face
def prepare_training_data(aligned_image=False):
    dirLabels = []  # this list only contains image directory names

    # list to hold all subject faces
    faces = []
    # list to hold labels for all subjects
    labels = []

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

                if not aligned_image:
                    # display an image window to show the image
                    # cv2.imshow("Training on image...", cv2.resize(image, (400, 500)))
                    # cv2.waitKey(500)
                    # detect face
                    face, rect = detect_faces(image, isForTraining=True)
                else:
                    print("Take Direct Image {} after converting in grayscale".format(image_name))
                    # convert the to gray scale as opencv face detector expects gray images
                    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                    # create a CLAHE object (Arguments are optional).
                    # clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
                    # gray = clahe.apply(gray)
                    face = gray

                # we will ignore faces that are not detected
                if face is not None:
                    # add face to list of faces
                    faces.append(face)
                    # add label index for this face because opencv face recognizer expect int value
                    labels.append(dir_index)

    cv2.destroyAllWindows()

    # dump the names (labels) to disk
    print("Serializing labels...")
    f = open(subject_labels, "wb")
    f.write(pickle.dumps(dirLabels))
    f.close()

    return faces, labels


def train_model(aligned_image=False):

    training_start_time = time.time()

    # let's first prepare our training data
    # data will be in two lists of same size
    # one list will contain all the faces
    # and other list will contain respective labels for each face
    print("Preparing data...")
    faces, labels = prepare_training_data(aligned_image)
    print("Data prepared")

    # print total faces and labels
    print("Total faces: ", len(faces))
    print("Total labels: ", len(labels))

    print("Train our model...")

    # train our face recognizer of our training faces
    face_recognizer.train(faces, np.array(labels))

    print("Save our trained our model into {} file...".format(trainned_model_name))
    # save our trained model
    face_recognizer.write(trainned_model_name)

    training_end_time = time.time()

    print("Total Elapsed time for training {} faces is {:.2f} sec".format(len(faces),(training_end_time-training_start_time)))


# this function recognizes the person in image/frame passed
# and draws a rectangle around detected face with name of the subject
def predict(img, labels):
    # convert the test image to gray image as opencv face detector expects gray images
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # let's detect multiscale (some images may be closer to camera than others) images
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=4, minSize=(30, 30),
                                          flags=cv2.CASCADE_SCALE_IMAGE)

    # print("Found {} face/s in test image".format(len(faces)))

    if len(faces) > 0:

        for face in faces:
            (x, y, w, h) = face

            # print(" x  y  w h ",x, y, w, h)

            face_gray_image = gray[y:y + w, x:x + h]

            # create a CLAHE object (Arguments are optional).
            # clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
            # face_gray_image = clahe.apply(face_gray_image)

            # predict the image using our face recognizer
            label, confidence = face_recognizer.predict(face_gray_image)

            print("label id = ", label, " confidence : ", confidence)

            if 120 < w < 160 or 120 < h < 160:
                confidence -= 15
            elif 70 < w or 70 < w:
                confidence -= 20
            elif 50 < w or 50 < w:
                confidence -= 25

            if confidence < MAX_CONFIDENCE:
                # get name of respective label returned by face recognizer
                label_text = labels[label]
            else:
                label_text = "Unknown"

            # draw a rectangle around face detected
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

            # write name of predicted person
            cv2.putText(img, label_text, (x, y - 10), cv2.FONT_HERSHEY_PLAIN, 1.5, (0, 255, 0), 2)

    return img


def webcam_face_recognition(labels):
    # camera = cv2.VideoCapture(args["videosrc"])
    camera = WebcamVideoStream(src=args["videosrc"]).start()
    fps = FPS().start()

    while True:
        frame = camera.read()

        # if we are unable to get video view, exit from program.
        if frame is None:
            print("Unable to get video frame. Please check video source.")
            break

        frame = imutils.resize(frame, width=640)

        key = cv2.waitKey(1) & 0xFF

        # if the `q` key was pressed, break from the loop
        if key == ord("q"):
            print("`q` pressed, Exiting...")
            break

        out_img = predict(frame, labels)

        cv2.imshow("Output Image", out_img)

        fps.update()

    fps.stop()
    print("Elasped time: {:.2f}".format(fps.elapsed()))
    print("Approx. FPS: {:.2f}".format(fps.fps()))
    camera.stop()
    cv2.destroyAllWindows()


def custom_image_recognition(image, labels):
    out_img = predict(image, labels)

    cv2.imshow("Output Image", out_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


# capture atleast 100 photos for given label. This data set is used for retrain model.
def capture_new_training_set(label):
    cam = WebcamVideoStream(src=args["videosrc"]).start()
    time.sleep(1.0)

    img_counter = 0

    while True:
        frame = cam.read()

        # if we are unable to get video view, exit from program.
        if frame is None:
            print("Unable to get video frame. Please check video source.")
            break

        frame = imutils.resize(frame, width=640)

        cv2.imshow("Capture Test Images For Training. Press ESC to exit", frame)

        key = cv2.waitKey(400) & 0xFF

        # if the `q` key was pressed, break from the loop
        if key == ord("q") or img_counter > MAX_TRAINING_IMAGES:
            print("Exiting...")
            break

        face, rect = detect_faces(frame, isForTraining=True)

        # ensure at least one face was found
        # we will ignore frame where faces are not detected
        if face is not None:

            # now image has only one face. So save frame

            img_name = "{}_{}_{}.png".format(label, img_counter, timestr)

            cv2.imwrite(os.path.join(label, img_name), frame)

            print("new training image {} saved!".format(img_name))
            img_counter += 1

            if img_counter > MAX_TRAINING_IMAGES:
                print('Max Training images capture. so closing...')
                break

    cam.release()
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

            print("Copy training images from {} to {} ".format(src_dir, dst_dir))
            copy_tree(src_dir, dst_dir)

            # remove our temporary created directory if exist
            if os.path.exists(label):
                shutil.rmtree(label)
                print("Directory {} removed".format(label))
            else:
                print("Directory {} not exists ".format(label))
        # Trained your model
        # It will create "trainned_model.yml" file
        train_model()
    else:
        if not os.path.isfile(trainned_model_name):
            print("`{}` trained model not found. Please first train your model with `-r train` option.".format(
                trainned_model_name))
            return -1

        # first load recognizer
        face_recognizer.read(trainned_model_name)

        if not os.path.isfile(trainned_model_name):
            print(
                "`{}` labels (subject names) file not found. Please first train your model with `-r train` option.".format(
                    trainned_model_name))
            return -1

        # load the actual face recognition model along with the label encoder
        labels = pickle.loads(open(subject_labels, "rb").read())

        # Run webcam face detect and recognition
        webcam_face_recognition(labels)

        # Custom Image testing
        # image = cv2.imread("/home/anil/machine_learning/face_detection/test/face2.jpg")
        # custom_image_recognition(image,labels)


if __name__ == '__main__':
    print('Initializing Opencv Face recognition model...')

    # construct the argument parser and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-r", "--run", type=str, default="test",
                    help="Run model for `train` or `test`. Please provide input.")
    ap.add_argument("-l", "--label", type=str, default=None,
                    help="Label to create new training dataset and train on it.")
    ap.add_argument("-v", "--videosrc", type=str, default="/dev/video0",
                    help="Provide video source (device index of camera i.e. /dev/video5 for webcam "
                         "or v4l2 command for mazzanine camera)")
    args = vars(ap.parse_args())

    # load cascade classifier training file for haarcascade
    haar_face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_alt2.xml')

    # load cascade classifier training file for lbpcascade
    lbp_face_cascade = cv2.CascadeClassifier('lbpcascade_frontalface.xml')

    face_cascade = haar_face_cascade

    # create our LBPH face recognizer
    face_recognizer = cv2.face.LBPHFaceRecognizer_create()

    main()
