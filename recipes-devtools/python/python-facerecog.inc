SUMMARY = "The world's simplest facial recognition api for Python and the command line "
HOMEPAGE = "https://github.com/ageitgey/face_recognition"
LICENSE = "MIT"

LIC_FILES_CHKSUM = "file://LICENSE;md5=5350ad154eb80290f2faad56592be730"
SRC_URI[md5sum] = "e7e567a58dc66c6ee7ac91a9aeb19eb6"
SRC_URI[sha256sum] = "f70d92c8582113fed669832cd8036819b66eebf4a535b1b43b1c0cede0072fb7"

CLEANBROKEN = "1"

PYPI_PACKAGE = "face_recognition"

RDEPENDS_${PN} = "\
		${PYTHON_PN}-facerecogmodels \
		${PYTHON_PN}-click \
		${PYTHON_PN}-dlib \
		${PYTHON_PN}-numpy \
		${PYTHON_PN}-pillow \
		${PYTHON_PN}-opencv \
"
