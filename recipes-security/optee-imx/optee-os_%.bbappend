FILESEXTRAPATHS_append := "${THISDIR}/optee-os-imx_git"


PATCHTOOL = "git"

SRC_URI += "file://0001-porting-imx8mqthor-in-optee-os-imx.patch \
			"
