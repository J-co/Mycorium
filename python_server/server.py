
import Adafruit_DHT
import RPi.GPIO as GPIO
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.websocket

from tornado.options import define, options
define("port", default=8080, help="run on the given port", type=int)

GPIO.setmode(GPIO.BCM)

# Humidifier Setup
humidifierPin = 13
GPIO.setup(humidifierPin, GPIO.OUT)
GPIO.output(humidifierPin, GPIO.HIGH)  # disable humidifier on start up

# Adafruit Sensor Setup
sensor = Adafruit_DHT.DHT11
adafruitPin = 17


class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('index.html')


class WebSocketHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        print 'new connection'
        self.write_message("connected")

    def on_message(self, message):
        print 'message received %s' % message
        self.write_message('message received %s' % message)
        if message == "HUMIDIFIER_ON":
            GPIO.output(humidifierPin, GPIO.LOW)
        if message == "HUMIDIFIER_OFF":
            GPIO.output(humidifierPin, GPIO.HIGH)
        if message == "ADAFRUIT_READ":
            humidity, temperature = Adafruit_DHT.read_retry(
                sensor, adafruitPin)
            if humidity is not None and temperature is not None:
                print(
                    'Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(temperature, humidity))
            else:
                print('Failed to get reading. Try again!')

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
