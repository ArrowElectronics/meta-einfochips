SUMMARY = "Qt5 Video HMI demo application"
DESCRIPTION = "This demo is the showcase for displaying any plant or production rooms conditions and monitoring them"
HOMEPAGE = "http://www.einfochips.com/"
LICENSE = "MIT"


#LICENSE = "LGPLv2.1+ & GFDL-1.2"
#LIC_FILES_CHKSUM = "file://COPYING.DOC;md5=ad1419ecc56e060eccf8184a87c4285f \
#                    file://COPYING.LIB;md5=2d5025d4aa3495befef8f17206a5b0a1"

LIC_FILES_CHKSUM = "file://${COMMON_LICENSE_DIR}/MIT;md5=0835ade698e0bcf8506ecda2f7b4f302"

DEPENDS = "qtdeclarative qtgraphicaleffects qtbase qtcharts qtquickcontrols2 qtmultimedia gstreamer1.0"


SRC_URI := "file://VideoHMIApplication.tar.gz"

S = "${WORKDIR}/VideoHMIApplication"

require recipes-qt/qt5/qt5.inc

do_install() {
    install -d ${D}${datadir}/${P}
    install -m 0755 ${B}/VideoHMIApplication ${D}${datadir}/${P}
}

FILES_${PN}-dbg += "${datadir}/${P}/.debug"
FILES_${PN} += "${datadir}"

RDEPENDS_${PN} = "qtdeclarative-qmlplugins qtgraphicaleffects-qmlplugins qtbase-plugins qtquickcontrols2-qmlplugins qtmultimedia-plugins gstreamer1.0"
