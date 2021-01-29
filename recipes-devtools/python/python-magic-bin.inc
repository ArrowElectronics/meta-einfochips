SUMMARY = "A python wrapper for libmagic"
HOMEPAGE = "http://jupyter.org/"
LICENSE = "MIT"

LIC_FILES_CHKSUM = "file://LICENSE;md5=16a934f165e8c3245f241e77d401bb88"
SRC_URI[md5sum] = "e384c95a47218f66c6501cd6dd45ff59"
SRC_URI[sha256sum] = "f3765c0f582d2dfc72c15f3b5a82aecfae9498bd29ca840d72f37d7bd38bfcd5"

CLEANBROKEN = "1"

SRC_URI = "git://github.com/julian-r/python-magic.git;branch=master"
SRCREV = "27e878aab0c5fa1751fa0e1a1e178bc0a58aac27"
S = "${WORKDIR}/git"
