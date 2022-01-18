# Copyright (C) 2020-2021 Einfochips


PATCHTOOL = "git"

FILESEXTRAPATHS_append := "${THISDIR}/linux-imx"

SRC_URI_append_imx8mqthor96 += "file://0001-imx8mq-thor96-Change-max-frequency-for-sd-card.patch \
					file://0002-IMX8-THOR96-Added-support-for-thor96-board.patch \
					file://0003-IMX8-THOR96-Enabled-Disable-DSI_SW_SEL.patch \
					file://0004-IMX8-THOR96-Enable-EEPROM-AT24-Support.patch \
					file://0005-IMX8-THOR96-Enable-support-for-NOR-SPI-Flash-sst-w25.patch \
					file://0006-IMX8-THOR96-Added-support-CAN-MCP2515T-I-ML.patch \
					file://0007-IMX8-THOR96-Enable-Native-HDMI.patch \
					file://0008-IMX8-THOR96-Enabled-Mezzanine-OV5640-camera-sensor.patch \
					file://0009-IMX8-THOR96-Added-support-for-adau1361-codec.patch \
					file://0010-IMX8-THOR96-Enabled-DSI-to-HDMI-ADV7533-bridge-chip.patch \
					file://0011-IMX8-THOR96-Added-USB-hub-and-otg-support.patch \
					file://0012-IMX8-THOR96-Added-support-of-spi2-for-zigbee.patch \
					file://0013-IMX8-THOR96-Added-support-for-LTE.patch \
					file://0014-IMX8-THOR96-Added-support-for-A2B-BUS-AD2428w.patch \
					file://0015-thor96-Update-uart2-to-work-BT-and-uart-debug-togeth.patch \
					file://0016-IMX8-THOR96-Enable-vpu_v4l2.patch \
                                        file://imx8mqthor96/arrow.cfg \
				"
DELTA_KERNEL_DEFCONFIG +="${WORKDIR}/${MACHINE}/arrow.cfg"
