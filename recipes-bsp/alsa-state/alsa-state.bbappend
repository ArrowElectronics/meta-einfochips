# Copyright Matthias Hentges <devel@hentges.net> (c) 2007
# License: MIT (see http://www.opensource.org/licenses/mit-license.php
#               for a copy of the license)
#
# Filename: alsa-state.bbappend

FILESEXTRAPATHS_prepend := "${THISDIR}/alsa-state:"

SRC_URI_append = "\
  file://${BOARD_TYPE}/asound.conf \
  file://${BOARD_TYPE}/asound.state \
"

do_install_append() {
    install -d ${D}/etc
    install -d ${D}/var/lib/alsa/

    install -m 0644 ${S}/${BOARD_TYPE}/asound.conf ${D}/etc/
    install -m 0644 ${S}/${BOARD_TYPE}/asound.state ${D}/var/lib/alsa/
}
