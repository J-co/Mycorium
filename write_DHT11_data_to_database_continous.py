#!/usr/bin/env python


import Adafruit_DHT
import time
sensor = Adafruit_DHT.DHT11



# Example using a Raspberry Pi with DHT sensor
# connected to GPIO23.
pin = 17

# Try to grab a sensor reading.  Use the read_retry method which will retry up
# to 15 times to get a sensor reading (waiting 2 seconds between each retry).

while True:
	humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)

	if humidity is not None and temperature is not None:
	    print('Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(temperature, humidity))
	else:
	    print('Failed to get reading. Try again!')



	#************************************************

	import MySQLdb


	db = MySQLdb.connect("localhost", "monitor", "raspberry", "mycorium")
	curs=db.cursor()

	with db:
	    curs.execute ("""INSERT INTO DHT11
	            values(NOW(), %f, %f)"""%(humidity,temperature))

	time.sleep(60)	    


	    
    
