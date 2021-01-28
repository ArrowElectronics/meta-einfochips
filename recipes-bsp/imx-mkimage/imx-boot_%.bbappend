PATCHTOOL = "git"

FILESEXTRAPATHS_prepend := "${THISDIR}/imx-boot:"


SRC_URI_append_imx8mqthor96 += "file://thor96/0001-Add-thor96-board-dtb-support.patch  \
"
