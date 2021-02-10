Face recognition using OpenCV :
    
A very basic and first of its kind in Face recognition model
OpenCV comes with two pre-trained and ready to use models Haar Classifier  & LBP Classifier for face detection.
Classifier decides if an image is a positive image <face image> or negative image <non-face image>.
A classifier is trained on hundreds of thousands of faces and non-face images to mature to classify a new image correctly.
This model is comparatively slower for face detection than ML module but face recognition part is faster then other modules.

If we required speed and accuracy is not constraint then we can use this model.


Inference Times:

On Board Training Time :  Approx 320 sec for 350 photos

On Board Testing       :  With WEBCAM 5 to 6 FPS if every frame has atleast one face.
