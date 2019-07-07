<?php 
function humidifier_on(){
$command = 'python /home/pi/Projects/Mycorium/set_GPIO.py 13 LOW';
exec($command, $out, $status);
echo join(', ', $out);
}
humidifier_on();
?>
