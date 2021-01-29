SUMMARY = "A series of convenience functions to make basic image processing functions such as translation, rotation, resizing, skeletonization, and displaying Matplotlib images easier with OpenCV and both Python 2.7 and Python 3."
HOMEPAGE = "https://github.com/jrosebr1/imutils"
LICENSE = "CLOSED"

SRC_URI[md5sum] = "bfb5a2cd095cebd3e4a27e8653d1322c"
SRC_URI[sha256sum] = "1d2bdf373e3e6cfbdc113d4e91547d3add3774d8722c8d4f225fa39586fb8076"

CLEANBROKEN = "1"

inherit pypi setuptools3

PYPI_PACKAGE = "imutils"

RDEPENDS_${PN} = "\
		${PYTHON_PN}-opencv \
"
