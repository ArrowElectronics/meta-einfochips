SUMMARY = "Keras is a high-level neural networks API, written in Python and capable of running on top of TensorFlow, CNTK, or Theano."
HOMEPAGE = "https://github.com/keras-team/keras"
SECTION = "devel/python"
LICENSE = "CLOSED"

SRC_URI[md5sum] = "bd92aafa85de6ae7574b080d65bb1d93"
SRC_URI[sha256sum] = "90b610a3dbbf6d257b20a079eba3fdf2eed2158f64066a7c6f7227023fd60bc9"

inherit pypi setuptools3

#S = "${WORKDIR}/git"

PYPI_PACKAGE = "Keras"

RDEPENDS_${PN} = "python3-numpy \
                  python3-h5py \
		  python3-keras-applications \
                  python3-keras-preprocessing \
                 "
