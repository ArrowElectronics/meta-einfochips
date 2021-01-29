SUMMARY = "Python3 Face Recognition Using dlib - models"
HOMEPAGE = ""
LICENSE = "CLOSED"
#LIC_FILES_CHKSUM = "file://LICENSE;md5=c011883ac26229b8ba3084f55c7664c6"

FILESEXTRAPATHS_prepend := "${THISDIR}/python-speechrecognition:"
SRC_URI = "git://github.com/Uberi/speech_recognition.git;branch=master \
	   file://flac;md5sum=5594523907096c584495b79021063173 \
	   file://setup.py;md5sum=d0ee3420ad489da312e0570dd730edcd \
"
SRCREV = "b24d05772828a895671c29dfb4f341ea55ee8e58"

DEPENDS = "flac"

S = "${WORKDIR}/git"

inherit setuptools3

CFLAGS_append = " -I${STAGING_INCDIR}"
LDFLAGS_append = " -L${STAGING_LIBDIR}"

do_configure_prepend() {
       rm -rf ${S}/speech_recognition/flac*
       mv ${WORKDIR}/flac ${S}/speech_recognition/
       mv ${WORKDIR}/setup.py ${S}/
}

do_compile_prepend() {
    export LDFLAGS="$LDFLAGS -L${STAGING_LIBDIR}"
    export CFLAGS="$CFLAGS -I${STAGING_INCDIR}"
}
