#!/bin/sh

# To permit this cgi, replace # on the first line above with the
# appropriate #!/path/to/sh shebang, and set this script executable
# with chmod 755.
#
# This script turn off zigbee light.


# disable filename globbing
set -f


# This line is required for CGI-BIN script running and showing output on webserver.
echo "Content-type: text/plain; charset=iso-8859-1"
echo

EUI64=`cat /usr/share/apache2/htdocs/zigbee/EUI64`

if [[ $? != 0 ]]
then
    echo "ERROR !!! Please check zigbee service is running and also write correct EUI64 in /usr/share/apache2/htdocs/zigbee/EUI64 file"
    exit -1
fi

#DEVICE_EUI64=000D6F0001B96425

DEVICE_EUI64=`cat /usr/share/apache2/htdocs/zigbee/lightEUI64`

if [[ $? != 0 ]]
then
    echo "ERROR !!! Please check Zigbee Web Application is running and Correct Zigbee Light is called."
    exit -1
fi

echo "Turn Off Zigbee Device..."
echo

mosquitto_pub -m '{"commands":[{"command": "zcl on-off off", "postDelayMs":0},{"command": "plugin device-table send {'"$DEVICE_EUI64"'} 1", "postDelayMs":0 }] }' -t gw/$EUI64/commands

echo "result = $?"
