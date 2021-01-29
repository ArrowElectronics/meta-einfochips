SUMMARY = "hmmlearn is a set of algorithms for unsupervised learning and inference of Hidden Markov Models"
HOMEPAGE = "https://github.com/hmmlearn/hmmlearn"
LICENSE = "BSD-3-Clause"

LIC_FILES_CHKSUM = "file://LICENSE;md5=528d3b1b6b29c8974a64ef87ba477e78"
SRC_URI[md5sum] = "929acdbe7c97a2fed65bd3bbff516810"
SRC_URI[sha256sum] = "694646f8302bc6402925a4b6892f3a5ccede06d25f22157c18cfbdecdb748361"

RDEPENDS_${PN} = "python3-scikitlearn"

CLEANBROKEN = "1"

PYPI_PACKAGE = "hmmlearn"

inherit pypi

do_install() {
	install -d ${D}/home/root
	cp -r ${WORKDIR}/hmmlearn-${PV} ${D}/home/root/
}

FILES_${PN} = "/home/root"
