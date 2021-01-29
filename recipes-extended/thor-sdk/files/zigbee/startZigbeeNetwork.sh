#!/bin/sh

# To permit this cgi, replace # on the first line above with the
# appropriate #!/path/to/sh shebang, and set this script executable
# with chmod 755.
#
# ***** !!! WARNING !!! *****
# This script leave previous zigbee network and start new zigbee network.
# Therefore all your previous connected zigbee devices will be disconnected.


# disable filename globbing
set -f

echo "Content-type: text/plain; charset=iso-8859-1"
echo

EUI64=`cat /usr/share/apache2/cgi-bin/zigbee/EUI64`

if [[ $? != 0 ]]
then
    echo "ERROR !!! Please check zigbee service is running and also write correct EUI64 in /usr/share/apache2/cgi-bin/zigbee/EUI64 file"
    exit -1
fi

echo "Start Zigbee Network..."
echo

echo "Clear all previous log files..."
cat /dev/null > /usr/share/apache2/htdocs/devicejoined.log
cat /dev/null > /usr/share/apache2/htdocs/deviceleft.log
cat /dev/null > /usr/share/apache2/htdocs/apsresponse.log
cat /dev/null > /usr/share/apache2/htdocs/zclresponse.log
cat /dev/null > /usr/share/apache2/htdocs/zigbee_devices.log
echo

echo "Leave previous Zigbee Network..."
mosquitto_pub -m '{"commands":[{"command": "network leave"}]}' -t gw/$EUI64/commands
echo "result = $?"
echo

sleep 3

echo "Create new Zigbee Network..."
mosquitto_pub -m '{"commands":[{"command": "plugin network-creator start 1"}]}' -t gw/$EUI64/commands
echo "result = $?"
