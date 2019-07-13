
#!/usr/bin/env python


import RPi.GPIO as GPIO
import sys

arguments = sys.argv
print arguments

if len(arguments)!=3:
	raise Exception('Incorrect number of arguments')

GPIO_Pin = int(arguments[1])

GPIO_Value = str(arguments[2])

GPIO.setmode(GPIO.BCM)


GPIO.setup(GPIO_Pin,GPIO.OUT)

if GPIO_Value=='LOW':
	GPIO.output(GPIO_Pin,GPIO.LOW)
elif GPIO_Value=='HIGH':
	GPIO.output(GPIO_Pin,GPIO.HIGH)
else:
	raise Exception('Second argument needs to be either  HIGH or LOW')








