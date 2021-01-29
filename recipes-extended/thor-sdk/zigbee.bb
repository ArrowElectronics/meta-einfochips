SUMMARY = "Zigbee with MQTT support implemention and Add Zigbee Web Application"
DESCRIPTION = "Zigbee Gateway Host application with MQTT support. MQTT provides a lightweight method of carrying out messaging using a publish/subscribe model. Here we disable CLI and start zigbee service on bootup."
HOMEPAGE = "http://einfochips.com/"
LICENSE = "CLOSED"

SRC_URI = "file://zigbee \
"

DEPENDS = "apache2"

inherit systemd useradd

do_install() {
    install -d ${D}/home/root/zigbee

    install -m 0755 ${WORKDIR}/zigbee/zigbee.sh ${D}/home/root/zigbee/
    install -m 0755 ${WORKDIR}/zigbee/Z3GatewayHost ${D}/home/root/zigbee/
    install -m 0755 ${WORKDIR}/zigbee/Z3GatewayHost_HMI ${D}/home/root/zigbee/
    install -m 0644 ${WORKDIR}/zigbee/aws-iot-device-sdk-python.tar.gz ${D}/home/root/zigbee/

    install -d ${D}${systemd_unitdir}/system/
    install -m 0644 ${WORKDIR}/zigbee/zigbee.service ${D}${systemd_unitdir}/system/

}

FILES_${PN} = "${systemd_unitdir}/system/zigbee.service \
               /home/root/zigbee \
"

INSANE_SKIP_${PN} = "ldflags"
RDEPENDS_${PN} += "bash"

SYSTEMD_SERVICE_${PN} = "zigbee.service"

USERADD_PACKAGES = "${PN}"
USERADD_PARAM_${PN} = "--system --no-create-home --shell /bin/false \
                       --user-group zigbee"
