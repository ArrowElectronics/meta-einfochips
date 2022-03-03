#!/bin/sh

# To permit this cgi, replace # on the first line above with the
# appropriate #!/path/to/sh shebang, and set this script executable
# with chmod 755.
#
# This script subscribe different zigbee events/topics to get info for
# ongoing activities.


# disable filename globbing
set -f


cat /var/log/syslog | grep -i Z3GatewayHost | grep EUI64 | awk '{ print $10 }' > /usr/share/apache2/htdocs/zigbee/EUI64

EUI64=`cat /usr/share/apache2/htdocs/zigbee/EUI64`

if [[ $? != 0 ]]
then
    echo "ERROR !!! Please check zigbee service is running and also write correct EUI64 in /usr/share/apache2/htdocs/zigbee/EUI64 file"
    exit -1
fi

echo "Subscribe Zigbee Topics..."
echo

echo "subscribe devices"
mosquitto_sub -t gw/$EUI64/devices >> /usr/share/apache2/htdocs/zigbee_devices.log &
echo "result = $?"

echo "subscribe apsresponse"
mosquitto_sub -t gw/$EUI64/apsresponse >> /usr/share/apache2/htdocs/apsresponse.log &
echo "result = $?"

echo "subscribe zclresponse"
mosquitto_sub -t gw/$EUI64/zclresponse >> /usr/share/apache2/htdocs/zclresponse.log &
echo "result = $?"


echo "subscribe devicejoined"
mosquitto_sub -t gw/$EUI64/devicejoined >> /usr/share/apache2/htdocs/devicejoined.log &
echo "result = $?"

echo "subscribe deviceleft"
mosquitto_sub -t gw/$EUI64/deviceleft >> /usr/share/apache2/htdocs/deviceleft.log &
echo "result = $?"

echo "subscribe devicestatechange"
mosquitto_sub -t gw/$EUI64/devicestatechange >> /usr/share/apache2/htdocs/devicestatechange.log &
echo "result = $?"
