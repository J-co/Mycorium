<?php 
function makeMeasurement(){
$command = '/home/pi/Projects/Mycorium/write_DHT11_data_to_database.py 2>&1';
exec($command, $out, $status);


echo join(', ', $out);
}

makeMeasurement();
?>

