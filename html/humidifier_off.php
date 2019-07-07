<?php 
function humidifier_off(){
$command = 'python /home/pi/Projects/Mycorium/set_GPIO.py 13 HIGH';
exec($command, $out, $status);
echo join(', ', $out);
}
humidifier_off();
?>
