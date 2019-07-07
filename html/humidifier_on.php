<?php 
function humidifier_on(){
$command = '/home/pi/Projects/Mycorium/humidifier_on.py 2>&1';
exec($command, $out, $status);
echo join(', ', $out);
}
humidifier_on();
?>
