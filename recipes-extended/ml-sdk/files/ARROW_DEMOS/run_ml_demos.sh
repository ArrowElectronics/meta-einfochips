#!/bin/bash

SCRIPT_PATH="$( cd "$(dirname "$0")" ; pwd -P )"

run_crowd_count()
{
	cd ${SCRIPT_PATH}/ai-crowd_count/demo
	echo "Welcome to AI Crowd Counting"
	echo "This is a demo application using Python, QT, Tensorflow to be run on embedded devices for Crowd counting"
	echo "You can choose Option for Live Mode (Camera)/Pre-captured Image Mode By clicking on GUI"

	echo "Please choose type of camera used in demo"
	echo "Press 1: For USB Web Cam"
	echo "Press 2: For D3 Mazzanine Camera"
	read reply
	case "$reply" in
		1)
			echo "USB Web Camera is used for demo"
			echo "Enter Camera device node entry e.g. /dev/video4 then 4 as numeric"
			read camera_input
			python3 main_app.py -v "$camera_input"
			;;
		2)
			echo "D3 Mazzanine Camera is used for demo"
			echo "Enter Camera device node entry e.g. /dev/video0 then 0 as numeric"
			read node
			camera_input="v4l2src device=/dev/video"$node" ! video/x-raw,width=640,height=480 ! videoconvert ! appsink"
			python3 main_app.py -v "$camera_input"
			;;
		*)
			echo "Select correct option: (1/2)"
			;;
	esac
}

run_object_detection()
{
	cd ${SCRIPT_PATH}/real-time-object-detection
	echo "Welcome to object Detection"
	echo "This model detect aeroplane, bicycle, bus, car, cat, cow, dog, horse, motorbike, person, sheep, train (objects necessary for self-driving)"
	echo ""
	echo "Please choose type of camera used in demo"
	echo "Press 1: For USB Web Cam"
	echo "Press 2: For D3 Mazzanine Camera"
	read reply
	case "$reply" in
		1)
			echo "USB Web Camera is used for demo"
			echo "Enter Camera device node entry e.g. /dev/video4 then 4 as numeric"
			read camera_input
			;;
		2)
			echo "D3 Mazzanine Camera is used for demo"
			echo "Enter Camera device node entry e.g. /dev/video0 then 0 as numeric"
			read node
			camera_input="v4l2src device=/dev/video"$node" ! video/x-raw,width=640,height=480 ! videoconvert ! appsink"
			;;
		*)
			echo "Select correct option: (1/2)"
			return
			;;
	esac

	echo "Which Object detection Demo you want to run:"
	echo "Press 1: For Fast Object Detection. Here Video Output is smooth."
	echo "Because we randomly sample only few frames from camera and applied same object detections on the rest of frames."
	echo ""
	echo "Press 2: For Slow Object detection. Here we applied object detections on each camera frame and display output."
	echo "So video output is very choppy. But get real-time detection here."
	echo ""
	echo "Please Select: (1/2) "
	echo ""

	read demo_reply
	case "$demo_reply" in
		1)
			echo "Fast Object Detection demo"
			python3 real_time_object_detection.py -v "$camera_input"
			;;
		2)
			echo "Slow Object Detection demo"
			python3 real_time_object_detection_SLOW.py -v "$camera_input"
			;;
		*)
			echo "Select correct option: (1/2)"
			return
			;;
	esac
}


run_face_recognition()
{
	cd ${SCRIPT_PATH}/face_recognition
	echo "Welcome to Face Recognition Demo"
	echo "This is a demo application using Python modules to be run on embedded devices for recognition of faces."
	echo "We already train model using given images. But can retrain model with new images and can increase accuracy of model."

	echo ""
	echo "Please choose type of camera used in demo"
	echo "Press 1: For USB Web Cam"
	echo "Press 2: For D3 Mazzanine Camera"
	echo ""
	read reply
	case "$reply" in
		1)
			echo "USB Web Camera is used for demo"
			echo "Enter Camera device node entry e.g. /dev/video4 then 4 as numeric"
			read camera_input
			;;
		2)
			echo "D3 Mazzanine Camera is used for demo"
			echo "Enter Camera device node entry e.g. /dev/video0 then 0 as numeric"
			read node
			camera_input="v4l2src device=/dev/video"$node" ! video/x-raw,width=640,height=480 ! videoconvert ! appsink"
			;;
		*)
			echo "Select correct option: (1/2)"
			;;
	esac


	echo ""
	echo "Please choose which face recognition demo you want to run"
	echo "Press 1: For Fast Face recognition. Here Video Output is smooth."
	echo "Because we randomly sample only few frames from camera and applied same face recognition on the rest of frames."
	echo "As we only sample few frames, here output is slow. You can get correct result around after 2-3 sec."

	echo ""
	echo "Press 2: For Slow Face Recognition. Here we applied face recognition on each camera frame and display output."
	echo "So video output is very choppy. But get real-time detection here."
	echo ""
	echo "Please Select: (1/2) "
	echo ""

	read demo_reply
	case "$demo_reply" in
		1)
			echo "Fast Face recognition demo selected"
			demo_file="face_recognition_pymodule_sklearn.py"
			;;
		2)
			echo "Real-time face recognition demo"
			demo_file="face_recognition_ML_sklearn.py"
			;;
		*)
			echo "Select correct option: (1/2)"
			return
			;;
	esac

	echo ""
	echo "Please choose mode of operation for demo"
	echo "Press 1: Test Model"
	echo "Press 2: Train Model"

	read mode
	case "$mode" in
		1)
			echo "Face recognition Testing ..."
			python3 ${demo_file} -v "$camera_input"
			;;
		2)
			echo "Face recognition Training ..."
			echo "Please provide new label... e.g. Joshua"
			echo "With this label, we will create new training dataset and will our retrain model."
			echo "If you don't want to create new training dataset but simply retrain model with existing images, then press enter without giving any label name"
			read label
			if [[ "$label" != "" ]];
			then
				python3 ${demo_file} -v "$camera_input" -r train -l "$label"
			else
				python3 ${demo_file} -v "$camera_input" -r train
			fi
			;;
		*)
			echo "Select correct option: (1/2)"
			return
			;;
	esac

}

run_speech_recognition()
{
	export PATH=$PATH:/usr/lib/python3.5/site-packages/speech_recognition/

	cd ${SCRIPT_PATH}/speech_recognition_tensorflow
	echo "Welcome to Speech Recognition Demo"
	echo "This is a demo application using Python modules and Tensorflow to be run on embedded devices for recognition of spoken words."

	echo "Which Speech Recognition Demo you want to run:"
	echo "Press 1: For Speech Recognition of custom words using tensorflow. - OFFLINE"
	echo "In this demo, our trained model will be able to detect following words:"
	echo "yes  no  up  down  left  right  on  off  stop  go"
	echo "Note: We need to speak near to mic and laud to detect these words. We will get few warning logs. Please ignore that."
	echo ""
	echo "Press 2: For Google API speech to Text -  Need internet connectivity."
	echo "In this demo we use Google api to convert speech to text."
	echo ""
	echo "Please Select: (1/2) "
	echo ""

	read demo_reply
	case "$demo_reply" in
		1)
			echo "Speech Recognition of custom words using tensorflow."
			python3 speech_recognition_pymodule.py
			;;
		2)
			echo "Google API speech to Text Demo"
			python3 speech_to_text_google_api.py
			;;
		*)
			echo "Select correct option: (1/2)"
			return
			;;
	esac


}

run_arm_nn_demo()
{
	echo "Welcome to ARM NN Demo"
	echo "This is a demo we run sample ARM NN demo to showcase ARM NN capabilities on our board."
	echo "This demo classify images using tensorflow mobilenet model. Here we approx get 3 FPS unlike our normal demo where we max get 1 FPS."
	echo "So using ARM NN our demo can be faster by 3 times."

	ArmnnExamples -f tensorflow-binary -i input -s '1 224 224 3' -o MobilenetV1/Predictions/Reshape_1 -d /usr/share/arm/armnn/testvecs/test2.mp4 -m /usr/share/arm/armnn/models/mobilenet_v1_1.0_224_frozen.pb -c CpuAcc --number_frame 10000
}

run_face_recognition_using_tf_lite_demo()
{
	cd ${SCRIPT_PATH}/eiq_sample_apps/examples-tflite/face_recognition
	echo "Welcome to Face Recognition using TensorFlow Lite demo"
	echo "Detecting Biggest Face in Real-Time"
	echo "Pleae provide Camera Node Entry"
	echo "Node entry e.g. /dev/video4 so enter 4 as numeric"
	read camera_node
	./FaceRecognition -c "$camera_node" -h 0.85

#   binary path
}

run_image_classification_using_armnn_demo()
{
	cd ${SCRIPT_PATH}/TFLite-armnn/img_classification_demo
	echo "Welcome to Image Classification using Arm NN demo"
	echo "This is a sample ARM NN demo to showcase ARM NN capabilities on our board."
	echo "In demo we will detect an Object like Cat, Dog, Shark, Laptop, Notebook, etc."
	echo "This will fetch the video input from the USB camera and show classification label on screen in real time"

	echo "Camera Based Image Classification Demo"
	echo "Please choose type of camera used in demo"
	echo "Press 1: For USB Web Cam"
	echo "Press 2: For D3 Mazzanine Camera"
	read reply
	case "$reply" in
		1)
			echo "USB Web Camera is used for demo"
			echo "Enter Command Camera device node entry e.g. /dev/video5"
			echo "Node entry e.g. /dev/video5 so enter 5 as numeric"
			read camera_input
			python3 tflite_mobilenetv1_quantized.py --cam "$camera_input"
			;;
		2)
			echo "D3 Mazzanine Camera is used for demo"
			echo "Enter Camera device node entry e.g. /dev/video0 then 0 as numeric"
			read node
			camera_input="v4l2src device=/dev/video"$node" ! video/x-raw,width=640,height=480 ! videoconvert ! appsink"
			python3 tflite_mobilenetv1_quantized.py --cam "$camera_input"
			;;
		*)
			echo "Select correct option: (1/2)"
			return
			;;
	esac
}

run_handwritten_digit_classification_using_armnn_demo()
{
	cd ${SCRIPT_PATH}/TFLite-armnn/handwritten_char_rec_demo
	echo "Welcome to Handwritten Digit Classification using Arm NN demo"
	echo "This is a sample ARM NN demo to showcase ARM NN capabilities on our board."
	echo "In demo we will classify the handwritten digits and show the labels with images on display"
	echo "This will fetch the input files from the directory and show classification label for 5 seconds along with input images"

	python3 mnist-tflite-armnn.py
}

run_option()
{
	echo "Choose the option from following"
	echo "Press 1 : AI Crowd Count"
	echo "Press 2 : Object Detection"
	echo "Press 3 : Face Recognition"
	echo "Press 4 : Speech Recognition"
	echo "Press 5 : Face Recognition using TensorFlow Lite demo"
	echo "Press 6 : Image Classification using Arm NN demo"
	echo "Press 7 : Handwritten Digit Classification using Arm NN demo"
	echo ""
	echo "Select: (1/2/3/4/5/6/7) "
	echo ""
	read reply
	case "$reply" in
		1)
			run_crowd_count
			;;
		2)
			run_object_detection
			;;
		3)
			run_face_recognition
			;;
		4)
			run_speech_recognition
			;;
		5)
			run_face_recognition_using_tf_lite_demo
			;;
		6)
			run_image_classification_using_armnn_demo
			;;
		7)
			run_handwritten_digit_classification_using_armnn_demo
			;;
		*)
			echo "Select correct option: (1/2/3/4/5/6/7/8)"
			;;
	esac
}

run_ml_demos()
{
	echo "########  Welcome to ML Demos [AI Corowd Count/Object detection/Face Recognition/Speech Recognition/Arm NN] ##########"
	echo "Prerequisite: Have you run <setup_ml_demo.sh>?"
	echo "Press: (y/n)"
	echo ""
	read REPLY
	case "$REPLY" in
		y|Y)
			run_option
			;;

		n|N)
			~/setup_ml_demo.sh
			run_option
			;;

		*)
			echo "Select correct option: (y/n)"
			;;
	esac
}

run_ml_demos

echo "Exiting Demo..."

