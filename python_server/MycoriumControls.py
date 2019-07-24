import Adafruit_DHT
import RPi.GPIO as GPIO
import time
import datetime
import threading


class Controller:
    def __init__(self):
        GPIO.setmode(GPIO.BCM)

        # Humidifier Setup
        self.humidifierPin = 13
        GPIO.setup(self.humidifierPin, GPIO.OUT)
        # disable humidifier on start up
        GPIO.output(self.humidifierPin, GPIO.HIGH)
        self.humidityControlActive = False

        # Lights Setup
        self.lightsPinA = 5
        self.lightsPinB = 22
        self.lightControlActive = False
        GPIO.setup(self.lightsPinA, GPIO.OUT)
        GPIO.setup(self.lightsPinB, GPIO.OUT)
        GPIO.output(self.lightsPinA, GPIO.HIGH)  # disable lights on start up
        GPIO.output(self.lightsPinB, GPIO.HIGH)

        # Adafruit Sensor Setup
        self.sensor = Adafruit_DHT.DHT11
        self.adafruitPin = 17
        self.currentTemperature = None
        self.currentHumidity = None
        self.adafruitMeasuring = False

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
            time.sleep(1)
        self.currentHumidity = humidity
        self.currentTemperature = temperature
        print "Humidity: %f; Temperature: %f" % (humidity, temperature)
        return humidity, temperature

    def startAdafruitMeasuring(self):
        if self.adafruitMeasuring == True:
            print "Already Measuring"
            return
        self.adafruitMeasuring = True

        def looper():
            while self.adafruitMeasuring:
                self.readAdafruit()
                time.sleep(10)
        t = threading.Thread(target=looper)
        t.start()

    def stopAdafruitMeasuring(self):
        self.adafruitMeasuring = False

    def startHumidityControl(self, humiditySetpoint):
        if self.humidityControlActive == True:
            print "Already active"
            return
        self.humidityControlActive = True
        if self.adafruitMeasuring == False:
            self.startAdafruitMeasuring()
        humidityTolerance = 10
        upperBound = max([humiditySetpoint+humidityTolerance, 100])
        lowerBound = min([humiditySetpoint-humidityTolerance, 0])

        def looper():
            while self.humidityControlActive == True:
                if self.currentHumidity <= lowerBound:
                    self.humidifierOn()
                if self.currentHumidity > upperBound:
                    self.humidifierOff()
        t = threading.Thread(target=looper)
        t.start()

    def stopHumidityControl(self):
        self.humidityControlActive = False

    def startLightControl(self, beginTime, endTime):
        if self.lightControlActive == True:
            print "Light Control already active"
            return
        self.lightControlActive = True

        def looper():
            while self.lightControlActive:
                currentTime = datetime.datetime.now().time()
                currentHour = currentTime.hour
                currentMinute = currentTime.minute
                if currentHour >= beginTime and currentHour < endTime:
                    self.lightsOn()
                else:
                    self.lightsOff()
                time.sleep(60)
        t = threading.Thread(target=looper)
        t.start()

    def stopLightControl(self):
        self.lightControlActive = False
