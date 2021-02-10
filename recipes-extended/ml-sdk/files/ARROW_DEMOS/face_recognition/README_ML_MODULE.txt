Face recognition using Machine learning models:
    
Face recognition uses Deep learning and scikit-learn / OpenCV technique
Machine learning - 
 1. Detects face in video streams using Caffe model. This model detects and localizes faces in 
     an image.
 2. Compute 128-d face embeddings to quantify a face using Torch deep learning openface model 
     pushing the embeddings for the negative image farther away
 3. Train a Support Vector Machine (SVM) on top of the embeddings using a supervised machine- 
      learning algorithm which can be used for both classification or regression challenges
 4. Recognize faces in video streams

This model have good accuracy and moderate speed. So better choice if we have trade of time and accuracy.

Inference Times:

On Board Training Time : Approx 346 sec for 350 photos (slower than opencv but faster than python)

On Board Testing       : With WEBCAM 1 to 1.5/2 FPS if every frame has atleast one face. (moderate speed)


