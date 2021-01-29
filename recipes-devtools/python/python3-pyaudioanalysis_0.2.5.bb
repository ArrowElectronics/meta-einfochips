SUMMARY = "Python3 Face Recognition Using dlib - models"
HOMEPAGE = ""
LICENSE = "CLOSED"
#LIC_FILES_CHKSUM = "file://LICENSE;md5=c011883ac26229b8ba3084f55c7664c6"

SRC_URI[md5sum] = "e8a20bad92071f672f770e1fa2078387"
SRC_URI[sha256sum] = "b8b7f8d662632019fe81d1638b73bc7faf87501c8bef31dcac3967f523f1a6af"

RDEPENDS_${PN} = " \
		python3-hmmlearn \
"

CLEANBROKEN = "1"

PYPI_PACKAGE = "pyAudioAnalysis"

inherit pypi

do_install() {
	install -d ${D}/home/root
	cp -r ${WORKDIR}/pyAudioAnalysis-${PV} ${D}/home/root/
}

FILES_${PN} = "/home/root"
