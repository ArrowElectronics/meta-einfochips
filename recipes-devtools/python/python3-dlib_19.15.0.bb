SUMMARY = "Dlib is a modern C++ toolkit containing machine learning algorithms and tools for creating complex software in C++ to solve real world problems"
HOMEPAGE = "http://dlib.net/"
LICENSE = "BSL-1.0"

LIC_FILES_CHKSUM = "file://dlib/LICENSE.txt;md5=2c7a3fa82e66676005cd4ee2608fd7d2"
SRC_URI += "file://CMakeLists.txt;md5=a286de4dfb94a36b2b3820d8e9b9dbf8 \
		file://dlib.CMakeLists.txt;md5=829d79b4dc43cd846179efcd57c95c2b \
		file://find_blas.cmake;md5=4118353f0a1689534eb0b2fb3160c10b"

SRC_URI[md5sum] = "0b023764805a39a51e068367def62b36"
SRC_URI[sha256sum] = "ad5e9e6276d1486b8ef7383229379d759f155f7d2c703e67e3d84682fb2a93c5"

CLEANBROKEN = "1"

DEPENDS = "cmake-native openblas-dev"
RDEPENDS_${PN} = "openblas"

PYPI_PACKAGE = "dlib"
inherit pypi setuptools3

do_configure_prepend() {
	mv ${WORKDIR}/find_blas.cmake ${WORKDIR}/dlib-19.15.0/dlib/cmake_utils
}

do_compile() {
	python3 setup.py install --compiler-flags "-fprofile-use" --set NEON=ON --set ENABLE_NEON=ON --set CMAKE_LIBRARY_PATH=${STAGING_LIBDIR} --set CMAKE_PREFIX_PATH=${STAGING_DIR_HOST} --set CMAKE_VERBOSE_MAKEFILE=ON --set DLIB_LINK_WITH_SQLITE3=OFF --set CMAKE_STRIP=${STAGING_DIR_NATIVE}/usr/bin/aarch64-poky-linux/aarch64-poky-linux-strip
}


BBCLASSEXTEND = "native"
