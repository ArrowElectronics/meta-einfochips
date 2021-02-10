Dependencies
============

* i.MX 8 board running an image with the eIQ release.
* MIPI Camera (if camera input is wanted)
* Ethernet cable (for sending files)

On i.MX Board
=============

Boot the board with the correct .dtb file for camera operation and connect the
Ethernet cable.

After booting, create the needed folders:

```bash
# mkdir -p /opt/opencv/model
# mkdir -p /opt/opencv/media
# chmod 777 /opt/opencv
```

On Host
=======

1) Download the model:

```bash
$ mkdir -p model media
$ wget -qN https://github.com/diegohdorta/models/raw/master/caffe/MobileNetSSD_deploy.caffemodel -P model/
$ wget -qN https://github.com/diegohdorta/models/raw/master/caffe/MobileNetSSD_deploy.prototxt -P model/
```

2) Export the board's IP:

```bash
$ export IMX_INET_ADDR=<imx_ip>
```

3) Deploy the files to the board:

```bash
$ scp -r src/* model/ media/ root@${IMX_INET_ADDR}:/opt/opencv
```

Run
===

* File-based demo

1) Put images at your choice inside the media folder and run:

```bash
# ./file.py
```

2) This returns the inference results for all the images inside the
media/ folder. It includes labels for each recognized object in the
input images. The processed images are available in the media-labeled/
folder.

* Camera demo

1) Make sure the MIPI camera is connected to the board using the properly
dtb file and run:

```bash
# ./camera.py
```

2) This opens a camera preview with inference results.
