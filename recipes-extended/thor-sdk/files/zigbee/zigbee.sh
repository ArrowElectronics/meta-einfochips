echo 132 > /sys/class/gpio/export
echo out > /sys/class/gpio/gpio132/direction
cat /sys/class/gpio/gpio132/value
echo 1 > /sys/class/gpio/gpio132/value
