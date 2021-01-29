# Copyright 2019 EINFOCHIPS

DESCRIPTION = "Module which add/copy thor96 board related required files on devices."
LICENSE = "CLOSED"

SRC_URI = 	"file://thread \
		 file://SAI1 \
		 file://A2B \
		"
S = "${WORKDIR}"

do_configure[noexec] = "1"
do_compile[noexec] = "1"

do_install() {
	install -d ${D}/home/root

	install -d ${D}/home/root/A2B

	cp -r ${S}/thread ${D}/home/root/
	chmod -R 775 ${D}/home/root/thread/imx_host_apps/spi-server/spi-server
	chmod -R 775 ${D}/home/root/thread/imx_host_apps/spi-server/spi-server.sh
	chmod -R 775 ${D}/home/root/thread/imx_host_apps/ip-driver-app
	chmod -R 775 ${D}/home/root/thread/imx_host_apps/server-host
	cp -r ${S}/SAI1 ${D}/home/root/

	install -m 0775 ${S}/A2B/A2B.tar.gz ${D}/home/root/A2B/
}

FILES_${PN} += "/home/root/*"
FILES_${PN} += "/opt/pylon5/*"
FILES_${PN} += "/opt/armnn/*"


RDEPENDS_${PN} += "bash"

ALLOW_EMPTY_${PN} = "1"
INSANE_SKIP_${PN} = " ldflags already-stripped debug-files dev-so file-rdeps rpaths staticdev"
SKIP_FILEDEPS_${PN} = "1"
