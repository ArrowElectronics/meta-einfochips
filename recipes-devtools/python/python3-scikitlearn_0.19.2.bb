SUMMARY = "scikit-learn is a Python module for machine learning built on top of SciPy."
HOMEPAGE = "http://scikit-learn.org/stable/"
LICENSE = "BSD"

LIC_FILES_CHKSUM = "file://COPYING;md5=2dbfbfce7c4e3df8a56ec61d0dc04f4f"
SRC_URI[md5sum] = "f91feb99601785fb2e6661349b696240"
SRC_URI[sha256sum] = "b276739a5f863ccacb61999a3067d0895ee291c95502929b2ae56ea1f882e888"

CLEANBROKEN = "1"

RDEPENDS_${PN} = "bash python"

PYPI_PACKAGE = "scikit-learn"

inherit pypi

do_install() {
	install -d ${D}/home/root
	cp -r ${WORKDIR}/scikit-learn-${PV} ${D}/home/root/
}

FILES_${PN} = "/home/root"
