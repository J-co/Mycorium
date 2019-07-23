
import Adafruit_DHT
import RPi.GPIO as GPIO
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.websocket
import json

from tornado.options import define, options
define("port", default=8080, help="run on the given port", type=int)

GPIO.setmode(GPIO.BCM)

# Humidifier Setup
humidifierPin = 13
GPIO.setup(humidifierPin, GPIO.OUT)
GPIO.output(humidifierPin, GPIO.HIGH)  # disable humidifier on start up

# Lights Setup
lightsPinA = 5
lightsPinB = 22
GPIO.setup(lightsPinA, GPIO.OUT)
GPIO.setup(lightsPinB, GPIO.OUT)
GPIO.output(lightsPinA, GPIO.HIGH)  # disable lights on start up
GPIO.output(lightsPinB, GPIO.HIGH)  

# Adafruit Sensor Setup
sensor = Adafruit_DHT.DHT11
adafruitPin = 17


class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('index.html')


class WebSocketHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        print 'new connection'
        # self.write_message("connected")

    def on_message(self, message):
        print 'message received %s' % message
        #self.write_message('message received %s' % message)
        if message == "HUMIDIFIER_ON":
            GPIO.output(humidifierPin, GPIO.LOW)
            self.write_message({"head": message, "success": True})
        if message == "HUMIDIFIER_OFF":
            GPIO.output(humidifierPin, GPIO.HIGH)
            self.write_message({"head": message, "success": True})
        if message == "ADAFRUIT_READ":
            for i in range(15):
                humidity, temperature = Adafruit_DHT.read(
                    sensor, adafruitPin)
                if humidity is not None and humidity <= 100 and temperature is not None:
                    break
            if humidity is not None and temperature is not None:
                self.write_message(json.dumps({'head': message, 'success': True, 'body': {
                                   "temperature": temperature, "humidity": humidity}}))
            else:
                self.write_message(json.dumps(
                    {'head': message, 'success': False, 'body': {}}))
        if message == "LIGHTS_ON":
            GPIO.output(lightsPinA, GPIO.LOW)
            GPIO.output(lightsPinB, GPIO.LOW)
            self.write_message({"head": message, "success": True})
        if message == "LIGHTS_OFF":
            GPIO.output(lightsPinA, GPIO.HIGH)
            GPIO.output(lightsPinB, GPIO.HIGH)
            self.write_message({"head": message, "success": True})

    def on_close(self):
        print 'connection closed'


if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = tornado.web.Application(
        handlers=[
            (r"/", IndexHandler),
            (r"/ws", WebSocketHandler)
        ]
    )
    httpServer = tornado.httpserver.HTTPServer(app)
    httpServer.listen(options.port)
    print "Listening on port:", options.port
    tornado.ioloop.IOLoop.instance().start()
