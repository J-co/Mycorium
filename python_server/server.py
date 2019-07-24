
from MycoriumControls import Controller
import Adafruit_DHT
import RPi.GPIO as GPIO
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.websocket
import json

from tornado.options import define, options
define("port", default=80, help="run on the given port", type=int)

MyControl = Controller()


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
            MyControl.humidifierOn()
            self.write_message({"head": message, "success": True})
        elif message == "HUMIDIFIER_OFF":
            MyControl.humidifierOff()
            self.write_message({"head": message, "success": True})
        elif message == "ADAFRUIT_READ":
            humidity, temperature = MyControl.readAdafruit()
            if humidity is not None and temperature is not None:
                self.write_message(json.dumps({'head': message, 'success': True, 'body': {
                                   "temperature": temperature, "humidity": humidity}}))
            else:
                self.write_message(json.dumps(
                    {'head': message, 'success': False, 'body': {}}))
        elif message == "ADAFRUIT_CONTINUOUS_MEASUREMENT_START":
            MyControl.startAdafruitMeasuring()
        elif message == "ADAFRUIT_CONTINUOUS_MEASUREMENT_STOP":
            MyControl.stopAdafruitMeasuring()
        elif message == "LIGHTS_ON":
            MyControl.lightsOn()
            self.write_message({"head": message, "success": True})
        elif message == "LIGHTS_OFF":
            MyControl.lightsOff()
            self.write_message({"head": message, "success": True})
        elif message == "LIGHTS_CONTROL_ON":
            MyControl.startLightControl(8, 20)
            self.write_message({"head": message, "success": True})
        elif message == "LIGHTS_CONTROL_OFF":
            MyControl.stopLightControl()
            self.write_message({"head": message, "success": True})
        else:
            self.write_message(
                {"head": message, "success": False, "body": "Unknown command"})

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
