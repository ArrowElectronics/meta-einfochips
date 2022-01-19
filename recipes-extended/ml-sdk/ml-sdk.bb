DESCRIPTION = "Module which add/copy required machine learning related files on devices."
LICENSE = "CLOSED"

SRC_URI = 	" \
		 file://tensorflow_aarch64-2.7.0-cp39-cp39-linux_aarch64.whl \
		 file://tensorflow_io_gcs_filesystem-0.23.1-cp39-cp39-linux_aarch64.whl \
		 file://grpcio-1.37.1-cp39-cp39-linux_aarch64.whl \
		 file://setup_ml_demo.sh \
		 file://basler \
		 file://armnn  \
		 file://ARROW_DEMOS \
		"
S = "${WORKDIR}"

do_install() {
	install -d ${D}/home/root

	install -d ${D}${sysconfdir}/udev/rules.d/

	install -d ${D}/opt/pylon5

	install -d ${D}/opt/armnn
	cp -r ${S}/armnn/* ${D}/opt/armnn/
	chmod -R 777 ${D}/opt/armnn

	install -m 0775 ${S}/tensorflow_aarch64-2.7.0-cp39-cp39-linux_aarch64.whl ${D}/home/root/
	install -m 0775 ${S}/tensorflow_io_gcs_filesystem-0.23.1-cp39-cp39-linux_aarch64.whl ${D}/home/root/
	install -m 0775 ${S}/grpcio-1.37.1-cp39-cp39-linux_aarch64.whl ${D}/home/root/
	install -m 0775 ${S}/setup_ml_demo.sh ${D}/home/root/
	
	cp -r ${S}/basler/pylon-5.1.0.12682-arm64/pylon5/* ${D}/opt/pylon5/
	chmod -R 777 ${D}/opt/pylon5

	install -m 0775 ${S}/basler/pylon-5.1.0.12682-arm64/69-basler-cameras.rules  ${D}${sysconfdir}/udev/rules.d/

	cp -r ${S}/ARROW_DEMOS ${D}/home/root/
}

do_configure[noexec] = "1"
do_compile[noexec] = "1"

FILES_${PN} += "/home/root/*"
FILES_${PN} += "/opt/pylon5/*"
FILES_${PN} += "/opt/armnn/*"

ALLOW_EMPTY_${PN} = "1"
INSANE_SKIP_${PN} = " already-stripped debug-files dev-so file-rdeps rpaths staticdev file-rdeps ldflags"
SKIP_FILEDEPS_${PN} = "1"

RDEPENDS_${PN} += "bash"
