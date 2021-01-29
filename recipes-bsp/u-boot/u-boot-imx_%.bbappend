# Copyright (C) 2018-2019 Einfochips

PATCHTOOL = "git"

FILESEXTRAPATHS_append := "${THISDIR}/u-boot-imx"


SRC_URI_append_imx8mqthor96 += " file://thor96/0001-IMX8-THOR96-Add-support-for-iMX8MQ-THOR96-board.patch \
             				file://thor96/0002-IMX8-THOR96-Configure-lpddr4-for-2GB.patch \
				        file://thor96/0003-IMX8-THOR96-SD-card-configuration.patch \
             				file://thor96/0004-IMX8-THOR96-Turn-on-USER_LED1-on-boot.patch \
             				file://thor96/0005-IMX8-THOR96-Zigbee-reset-gpio-config.patch \
             				file://thor96/0006-IMX8-THOR96-Configure-low-speed-expansion-gpio.patch \
           				"
