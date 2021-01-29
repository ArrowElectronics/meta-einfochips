SUMMARY = "Python3 Face Recognition Using dlib - models"
HOMEPAGE = ""
LICENSE = "CLOSED"
#LIC_FILES_CHKSUM = "file://LICENSE;md5=c011883ac26229b8ba3084f55c7664c6"

SRC_URI[md5sum] = "7e4c88139284033f67b4336c74eda3b8"
SRC_URI[sha256sum] = "93bfde30e0b64e63a46f2fd77e85c41fd51182a4a3413d9edfaf9ffaa26efb74"

inherit pypi

CLEANBROKEN = "1"

DEPENDS = "${PYTHON_PN} portaudio-v19"

PYPI_PACKAGE = "PyAudio"
