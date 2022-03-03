
FILESEXTRAPATHS_prepend := "${THISDIR}/files:"

SRC_URI += "file://zigbee \
			file://apache2 \
			"

do_install_append() {

	install -d ${D}/${sysconfdir}/${BPN}

	# Replace our custom created httpd.conf file
	install -m 0644 ${WORKDIR}/apache2/httpd.conf ${D}/${sysconfdir}/${BPN}
	install -m 0644 ${WORKDIR}/apache2/httpd-ssl.conf ${D}/${sysconfdir}/${BPN}

	install -d ${D}${datadir}/apache2/cgi-bin/zigbee

	install -m 0755 ${WORKDIR}/zigbee/startZigbeeNetwork.sh ${D}${datadir}/apache2/cgi-bin/zigbee
	install -m 0755 ${WORKDIR}/zigbee/scanZigbeeDevices.sh ${D}${datadir}/apache2/cgi-bin/zigbee
	install -m 0755 ${WORKDIR}/zigbee/stopScanningZigbeeDevices.sh ${D}${datadir}/apache2/cgi-bin/zigbee
	install -m 0755 ${WORKDIR}/zigbee/subscribeZigbeeTopics.sh ${D}${datadir}/apache2/cgi-bin/zigbee
	install -m 0755 ${WORKDIR}/zigbee/turnLightOff.sh ${D}${datadir}/apache2/cgi-bin/zigbee
	install -m 0755 ${WORKDIR}/zigbee/turnLightOn.sh ${D}${datadir}/apache2/cgi-bin/zigbee

	install -m 0755 ${WORKDIR}/zigbee/serverEvent.php ${D}${datadir}/apache2/cgi-bin/zigbee
	install -m 0755 ${WORKDIR}/zigbee/sendData.php ${D}${datadir}/apache2/cgi-bin/zigbee
	install -m 0755 ${WORKDIR}/zigbee/devicelog.php ${D}${datadir}/apache2/cgi-bin/zigbee

	install -m 0666 ${WORKDIR}/zigbee/EUI64 ${D}${datadir}/apache2/cgi-bin/zigbee
	install -m 0666 ${WORKDIR}/zigbee/lightEUI64 ${D}${datadir}/apache2/cgi-bin/zigbee
	install -m 0666 ${WORKDIR}/zigbee/lightinfo.json ${D}${datadir}/apache2/cgi-bin/zigbee

	install -d ${D}${datadir}/apache2/htdocs

	cp -r ${WORKDIR}/zigbee/ZigBeeWebApplication ${D}${datadir}/apache2/htdocs/

	install -d ${D}${datadir}/apache2/htdocs/zigbee
	mv ${D}${datadir}/apache2/cgi-bin/zigbee ${D}${datadir}/apache2/htdocs
}

CONFFILES_${PN} += " ${sysconfdir}/${BPN}/httpd-ssl.conf "
