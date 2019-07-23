import Adafruit_DHT
import RPi.GPIO as GPIO


class Controller:
    def __init__(self):
        GPIO.setmode(GPIO.BCM)

        # Humidifier Setup
        self.humidifierPin = 13
        GPIO.setup(self.humidifierPin, GPIO.OUT)
        # disable humidifier on start up
        GPIO.output(self.humidifierPin, GPIO.HIGH)

        # Lights Setup
        self.lightsPinA = 5
        self.lightsPinB = 22
        GPIO.setup(self.lightsPinA, GPIO.OUT)
        GPIO.setup(self.lightsPinB, GPIO.OUT)
        GPIO.output(self.lightsPinA, GPIO.HIGH)  # disable lights on start up
        GPIO.output(self.lightsPinB, GPIO.HIGH)

        # Adafruit Sensor Setup
        self.sensor = Adafruit_DHT.DHT11
        self.adafruitPin = 17
        self.currentTemperature = None
        self.currentHumidity = None

    def humidifierOn(self):
        GPIO.output(self.humidifierPin, GPIO.LOW)

    def humidifierOff(self):
        GPIO.output(self.humidifierPin, GPIO.HIGH)

    def lightsOn(self):
        GPIO.output(self.lightsPinA, GPIO.LOW)
        GPIO.output(self.lightsPinB, GPIO.LOW)

    def lightsOff(self):
        GPIO.output(self.lightsPinA, GPIO.HIGH)
        GPIO.output(self.lightsPinB, GPIO.HIGH)

    def readAdafruit(self):
        for i in range(15):
            humidity, temperature = Adafruit_DHT.read(
                self.sensor, self.adafruitPin)
            if humidity is not None and humidity <= 100 and temperature is not None:
                break
        self.currentHumidity = humidity
        self.currentTemperature = temperature
        return humidity, temperature
