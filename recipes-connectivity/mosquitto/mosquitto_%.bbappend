FILESEXTRAPATHS_append := "${THISDIR}"


do_install_append () {
        mv ${D}${sysconfdir}/mosquitto/mosquitto.conf.example ${D}${sysconfdir}/mosquitto/mosquitto.conf
}


FILES_${PN} += " \
				${bindir}/mosquitto_pub \
				${bindir}/mosquitto_sub \
				${libdir}/libmosquitto.so.1 \
				${libdir}/libmosquittopp.so.1 \
				"
