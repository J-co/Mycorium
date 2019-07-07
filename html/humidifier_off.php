<?php 
function humidifier_off(){
$command = '/home/pi/Projects/Mycorium/set_GPIO.py 13 LOW 2>&1';
exec($command, $out, $status);
echo join(', ', $out);
}
humidifier_off();
?>
