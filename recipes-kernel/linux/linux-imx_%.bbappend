# Copyright (C) 2018-2019 Einfochips


PATCHTOOL = "git"

FILESEXTRAPATHS_append := "${THISDIR}/linux-imx"

SRC_URI_append_imx8qxpaiml  += "file://imx8qxpaiml/0001-IMX8-AIML-Added-dts-file-for-aiml-platform.patch \
								file://imx8qxpaiml/0002-IMX8-AIML-Enable-EEPROM-support.patch \
								file://imx8qxpaiml/0003-IMX8-AIML-Enable-Sensors-Acc-Gyro-support.patch \
								file://imx8qxpaiml/0004-IMX8-AIML-OV5640-camera-support.patch \
								file://imx8qxpaiml/0005-IMX8-AIML-USB-hub-reset.patch \
								file://imx8qxpaiml/0006-IMX8-AIML-DSI-to-HDMI-display-support.patch \
								file://imx8qxpaiml/0007-IMX8-AIML-Enable-spdif-support.patch \
								file://imx8qxpaiml/0008-IMX8-AIML-Added-4-DMIC-support-on-ESAI-port.patch \
								file://imx8qxpaiml/0009-IMX8-AIML-Enable-USB-OTG-support.patch \
								file://imx8qxpaiml/0010-IMX8-AIML-wifi-bt-related-changes.patch \
								file://imx8qxpaiml/0011-IMX8-AIML-Added-user-leds-support.patch \
								file://imx8qxpaiml/0012-IMX8-AIML-Added-Low-speed-expansion-i2c-spi.patch \
								file://imx8qxpaiml/arrow.cfg \
								"
DELTA_KERNEL_DEFCONFIG +="${WORKDIR}/${MACHINE}/arrow.cfg"
