<?php 
function humidifier_on(){
$command = '/home/pi/Projects/Mycorium/set_GPIO.py 13 HIGH 2>&1';
exec($command, $out, $status);
echo join(', ', $out);
}
humidifier_on();
?>
