Face recognition using Python Module:

1. This model uses a pre-developed python package called “face_recognition” developed by Adam Geitgey for face detection and face recognition. This python module is based on dlib library (another python package) developed by Davis King, This uses “deep metric learning” to construct the face embeddings which is used for the actual recognition process.
2. The 128-d embeddings is used for each face in the dataset to recognize the faces in video streams. It uses a dataset of ~3 million images.
3. This face recognition library requires RGB input before training or testing.
4. Two different algorithms to detect and recognition faces. “CNN” or “HOG”. 
The CNN method is more accurate but slower. HOG is faster but less accurate.
We use "HOG" model in demo.


Slower among other two module
But most accurate model.

If speed is not constraint then this model is best choice. For Image recognition we should use this model.



Inference Times:

On Board Training Time  :  Approx 66 sec for 30 photos

On Board Testing        :  With video file 0.6 FPS if every frame has atleast one face.

 
