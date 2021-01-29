# Copyright (C) 2020-2021 Einfochips


PATCHTOOL = "git"

FILESEXTRAPATHS_append := "${THISDIR}/linux-imx"

SRC_URI_append_imx8mqthor96 += "file://imx8mqthor96/0001-IMX8-THOR96-Added-support-for-thor96-board.patch \
						file://imx8mqthor96/0002-IMX8-THOR96-Enable-EEPROM-AT24-Support.patch \
				                file://imx8mqthor96/0003-IMX8-THOR96-Enable-support-for-NOR-SPI-Flash-sst-w25.patch \
				                file://imx8mqthor96/0004-IMX8-THOR96-Added-support-CAN-MCP2515T-I-ML.patch \
				                file://imx8mqthor96/0005-IMX8-THOR96-Enable-Native-HDMI.patch \
				                file://imx8mqthor96/0006-IMX8-THOR96-Enabled-Mezzanine-OV5640-camera-sensor.patch \
				                file://imx8mqthor96/0007-IMX8-THOR96-Added-support-for-adau1361-codec.patch \
				                file://imx8mqthor96/0008-IMX8-THOR96-Enabled-DSI-to-HDMI-ADV7533-bridge-chip.patch \
				                file://imx8mqthor96/0009-IMX8-THOR96-Added-USB-hub-and-otg-support.patch \
				                file://imx8mqthor96/0010-IMX8-THOR96-Added-support-of-spi2-for-zigbee.patch \
				                file://imx8mqthor96/0011-IMX8-THOR96-Camera-OV5640-enabled-for-mipi-csi1.patch \
				                file://imx8mqthor96/0012-IMX8-THOR96-Resolved-SD-card-timeout-issue.patch \
				                file://imx8mqthor96/0013-IMX8-THOR96-Added-support-for-LTE.patch \
				                file://imx8mqthor96/0014-IMX8-THOR96-Enabled-Disable-DSI_SW_SEL.patch \
				                file://imx8mqthor96/0015-IMX8-THOR96-Added-support-for-A2B-BUS-AD2428w.patch \
				                file://imx8mqthor96/0016-IMX8-THOR96-wifi-supoort-added.patch \
				                file://imx8mqthor96/0017-IMX8-THOR96-Enable-ethernet-support.patch \
				                file://imx8mqthor96/0018-IMX8-THOR96-Added-user-leds-support.patch \
						file://imx8mqthor96/arrow.cfg \
				                file://imx8mqthor96/0001-change-max-frequency-for-sd-card.patch \
						"

DELTA_KERNEL_DEFCONFIG +="${WORKDIR}/${MACHINE}/arrow.cfg"
