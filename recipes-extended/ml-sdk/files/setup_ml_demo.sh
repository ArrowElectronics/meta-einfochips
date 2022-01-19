#!/bin/bash

#-----------------------------------------------------------------------------------------------------------------------------------------------
#  Arrow IMX8 ML board setup script 
#-----------------------------------------------------------------------------------------------------------------------------------------------
#  The script will install all required wifi,BT and python packages
# 
#  NOTE : The script will run only once. No need to run each time when reboot. Script will take almost 15 min to run.
#-----------------------------------------------------------------------------------------------------------------------------------------------

echo "****** Script Started *******"
echo "Make sure your board have internet connectivity via ethernet or WiFi"
echo "Trying to install all required python packages... It will take around 30 min if not installed(One time setup)..."

pip3 install --upgrade pip
pip install --upgrade pip
MARKER_FILE="/opt/SetupCompleted"

# Setup Internet connection
sudo systemctl disable systemd-resolved.service
sudo systemctl stop systemd-resolved.service
sudo ln -sf /run/systemd/resolve/resolv.conf /etc/resolv.conf
ls -l /etc/resolv.conf
sudo systemctl enable systemd-resolved.service
sudo systemctl start systemd-resolved.service

# Setup scipy
pip3 install scipy==1.5.4

if [ -f "$MARKER_FILE" ]
then
    echo "Setup is already completed. No need to do anything. Exiting..."
    exit 0
fi

pkgs='absl-py astunparse flatbuffers gast google-pasta h5py keras keras-preprocessing libclang numpy opt-einsum protobuf six scikit-learn tensorboard tensorflow-estimator termcolor typing-extensions wheel wrapt opencv-python'

for pkg in $pkgs; do
	pip3 list | grep $pkg
    	if [ $? -ne 0 ]; then
		pip3 install $pkg
    	else 
        	echo "Already installed: $pkg"
    	fi
done

# Setup grpcio
pip3 list | grep grpcio

if [ $? -ne 0 ]; then
    echo "install python package : grpcio"

    ls -la  ~/grpcio-1.37.1-cp39-cp39-linux_aarch64.whl
    if [ $? -ne 0 ]; then
        echo "grpcio-1.37.1-cp39-cp39-linux_aarch64.whl file not found in home folder"
        exit -1
    fi

    pip3 --no-cache-dir install ~/grpcio-1.37.1-cp39-cp39-linux_aarch64.whl
    if [ $? -ne 0 ]; then
        echo "tensorflow not install properly. Please manually install package or re-run script."
        exit -1
    fi
fi

pip3 list | grep tensorflow_io_gcs_filesystem

if [ $? -ne 0 ]; then
    echo "install python package : tensorflow"

    ls -la  ~/tensorflow_io_gcs_filesystem-0.23.1-cp39-cp39-linux_aarch64.whl
    if [ $? -ne 0 ]; then
        echo "tensorflow_io_gcs_filesystem-0.23.1-cp39-cp39-linux_aarch64.whl file not found in home folder"
        exit -1
    fi

    pip3 --no-cache-dir install ~/tensorflow_io_gcs_filesystem-0.23.1-cp39-cp39-linux_aarch64.whl
    if [ $? -ne 0 ]; then
        echo "tensorflow_io_gcs_filesystem not install properly. Please manually install package or re-run script."
        exit -1
    fi
fi

python3 -c "import tensorflow"

if [ $? -ne 0 ]; then
    echo "install python package : tensorflow"

    ls -la  ~/tensorflow_aarch64-2.7.0-cp39-cp39-linux_aarch64.whl
    if [ $? -ne 0 ]; then
        echo "tensorflow_aarch64-2.7.0-cp39-cp39-linux_aarch64.whl file not found in home folder"
        exit -1
    fi

    pip3 --no-cache-dir install ~/tensorflow_aarch64-2.7.0-cp39-cp39-linux_aarch64.whl
    if [ $? -ne 0 ]; then
        echo "tensorflow not install properly. Please manually install package or re-run script."
        exit -1
    fi
fi

python3 -c "import imutils"

if [ $? -ne 0 ]; then
    echo "install python package : imutils"
    pip3 --no-cache-dir install imutils
    if [ $? -ne 0 ]; then
        echo "Please check your network connection. Not able to download package."
        exit -1
    fi
fi

echo "Create marker file $MARKER_FILE"
touch $MARKER_FILE

if [ $? -ne 0 ]; then
    echo "Unable to create marker file"
    exit -1
fi

echo "Installed all packages successfully."

