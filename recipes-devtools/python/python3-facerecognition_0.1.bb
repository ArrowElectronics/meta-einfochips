SUMMARY = "Python facial recognition api for Python and the command line"
SECTION = "devel/python"
LICENSE = "CLOSED"
# LIC_FILES_CHKSUM = "file://LICENSE;md5sum=5350ad154eb80290f2faad56592be730"

inherit setuptools3 pkgconfig

SRC_URI = " \
    https://github.com/ageitgey/face_recognition/archive/master.zip \
"

SRC_URI[md5sum] = "042eb2feabc0045298b8d2511b99e2ec"
SRC_URI[sha256sum] = "5c4a37c38743cbb58329f9a2ef5eefaaf4f2b1328449eab6a004eac2a7cdb017"

S = "${WORKDIR}/face_recognition-master"

DEPENDS += "python3 libjpeg-turbo zlib tiff freetype libpng jpeg"

# DISTUTILS_INSTALL_ARGS += "--disable-platform-guessing"

CFLAGS_append = " -I${STAGING_INCDIR}"
LDFLAGS_append = " -L${STAGING_LIBDIR}"

do_compile_prepend() {
    export LDFLAGS="$LDFLAGS -L${STAGING_LIBDIR}"
    export CFLAGS="$CFLAGS -I${STAGING_INCDIR}"
}
