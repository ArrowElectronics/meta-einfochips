#!/bin/bash

reset_gpio=42
power_gpio=77
path="/sys/class/gpio"
reset_path="$path/gpio$reset_gpio"
power_path="$path/gpio$power_gpio"
delay=0.5

# Power ON Sequence of EC25-E LTE Modem

echo "EC25-E modem power ON starts"
#Reset gpio
#Set both Reset and Powerkey to low
( cd $path ; echo $reset_gpio > export )
( cd $reset_path ; echo out > direction )
( cd $reset_path ; echo 0 > value )
( cd $path ; echo $power_gpio > export )
( cd $power_path ; echo out > direction )
( cd $power_path ; echo 0 > value )
sleep $delay
sleep $delay

#set powerkey to high then back to low
( cd $power_path ; echo 0 > value )
sleep $delay
( cd $power_path ; echo 1 > value )
sleep 0.2
( cd $power_path ; echo 0 > value )

#set reset to zero, then to 1 and then back to zero
( cd $reset_path ; echo 0 > value )
sleep $delay
( cd $reset_path ; echo 1 > value )
sleep $delay
( cd $reset_path ; echo 0 > value )
sleep $delay

#sleep
sleep 7
echo "EC25-E modem power ON done"
