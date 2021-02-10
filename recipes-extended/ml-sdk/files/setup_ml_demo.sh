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

# Setup grpcio
pip3 install --upgrade grpcio-1.33.2-cp37-cp37m-linux_aarch64.whl

# Setup scipy
pip3 install scipy==1.5.4

if [ -f "$MARKER_FILE" ]
then
    echo "Setup is already completed. No need to do anything. Exiting..."
    exit 0
fi

python3 -c "import tensorflow"

if [ $? -ne 0 ]; then
    echo "install python package : tensorflow"

    ls -la  ~/tensorflow-1.15.0-cp37-cp37m-linux_aarch64.whl
    if [ $? -ne 0 ]; then
        echo "tensorflow-1.15.0-cp37-cp37m-linux_aarch64.whl file not found in home folder"
        exit -1
    fi

    pip3 --no-cache-dir install ~/tensorflow-1.15.0-cp37-cp37m-linux_aarch64.whl
    if [ $? -ne 0 ]; then
        echo "tensorflow not install properly. Please manually install package or re-run script."
        exit -1
    fi
fi

python3 -c "import sklearn"

if [ $? -ne 0 ]; then
    echo "install python package : scikit-learn."
    cd ~/scikit-learn-0.19.2/
    if [ $? -ne 0 ]; then
        echo "scikit-learn-0.19.2 directory not found in home folder"
        exit -1
    fi
    
    python3 setup.py install
    if [ $? -ne 0 ]; then
        echo "scikit-learn-0.19.2 not install properly. Please manually install package or re-run script."
        exit -1
    fi
fi


cd ~/

#python3 -c "import tensorboard"

#if [ $? -ne 0 ]; then
#    echo "install python package : tensorboard"
    
#    ls -la  ~/tensorboard-1.12.0-py3-none-any.whl
#    if [ $? -ne 0 ]; then
#        echo "tensorboard-1.12.0-py3-none-any.whl file not found in home folder."
#        exit -1
#    fi
    
#    pip3 --no-cache-dir install ~/tensorboard-1.12.0-py3-none-any.whl
#    if [ $? -ne 0 ]; then
#        echo "tensorboard not install properly. Please manually install package or re-run script."
#        exit -1
#    fi
#fi

python3 -c "import Keras"

if [ $? -ne 0 ]; then
    echo "install python package : Keras"
    pip3 --no-cache-dir install Keras
    if [ $? -ne 0 ]; then
        echo "Please check your network connection. Not able to download package."
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

