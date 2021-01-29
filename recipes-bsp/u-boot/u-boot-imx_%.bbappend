# Copyright (C) 2020-2021 Einfochips

PATCHTOOL = "git"

FILESEXTRAPATHS_append := "${THISDIR}/u-boot-imx"

SRC_URI_append_imx8qxpaiml += " file://aiml/0001-IMX8-AIML-Add-support-for-iMX8QXP-AIML-board.patch \
				file://aiml/0002-low-speed-expansion.patch \
				"
