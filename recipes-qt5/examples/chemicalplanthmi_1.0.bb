SUMMARY = "Qt5 chemicalplant QML demo application"
DESCRIPTION = "This QML demo application is the showcase of how we can control chemical plant through GUI using QT application"
HOMEPAGE = "https://www.einfochips.com/"
LICENSE = "MIT"

LIC_FILES_CHKSUM = "file://${COMMON_LICENSE_DIR}/MIT;md5=0835ade698e0bcf8506ecda2f7b4f302"

DEPENDS = "qtdeclarative qtbase qtcharts qtquickcontrols2"

SRC_URI := "file://ChemicalPlantHMI.tar.gz"

S = "${WORKDIR}/ChemicalPlantHMI"

require recipes-qt/qt5/qt5.inc

inherit qmake5

do_install() {
    install -d ${D}${datadir}/${P}
    install -m 0755 ${B}/ChemicalPlantHMI ${D}${datadir}/${P}
}

FILES_${PN}-dbg += "${datadir}/${P}/.debug"
FILES_${PN} += "${datadir}"

RDEPENDS_${PN} = "qtdeclarative-qmlplugins qtbase-plugins qtquickcontrols2-qmlplugins"
