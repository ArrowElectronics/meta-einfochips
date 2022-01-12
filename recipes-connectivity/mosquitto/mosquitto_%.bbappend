FILESEXTRAPATHS_append := "${THISDIR}"




FILES_${PN} += " \
				${bindir}/mosquitto_pub \
				${bindir}/mosquitto_sub \
				${libdir}/libmosquitto.so.1 \
				${libdir}/libmosquittopp.so.1 \
				"
