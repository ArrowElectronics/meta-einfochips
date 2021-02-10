#!/bin/sh
# Copyright (c) 2019 Einfochips
LOG=/opt/armnn/log.txt

ID=$(cat $LOG | grep "prediction" | sed 's/[)(]//g')
ID=$(echo $ID | awk '{print $4}')
[ -z $ID ] && echo error || echo $ID
