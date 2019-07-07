<?php 
function humidifier_off(){
$command = '/home/pi/Projects/Mycorium/humidifier_off.py 2>&1';
exec($command, $out, $status);
echo join(', ', $out);
}
humidifier_off();
?>
