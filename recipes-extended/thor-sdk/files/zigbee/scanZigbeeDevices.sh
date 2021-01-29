#!/bin/sh

# To permit this cgi, replace # on the first line above with the
# appropriate #!/path/to/sh shebang, and set this script executable
# with chmod 755.
#
# This script scan zigbee network and paired them by creating open zigbee network.
# This open network paired devices for specific period of time lets say about a minutes.

# disable filename globbing
set -f

# This line is required for CGI-BIN script running and showing output on webserver.
echo "Content-type: text/plain; charset=iso-8859-1"
echo

EUI64=`cat /usr/share/apache2/cgi-bin/zigbee/EUI64`

if [[ $? != 0 ]]
then
    echo "ERROR !!! Please check zigbee service is running and also write correct EUI64 in /tmp/EUI64 file"
    exit -1
fi

echo "Scanning Zigbee Devices..."
echo

mosquitto_pub -m '{"commands":[{"command": "plugin network-creator-security open-network","postDelayMs":100}]}' -t gw/$EUI64/commands
echo "result = $?"
