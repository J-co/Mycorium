import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.websocket
 
from tornado.options import define, options
define("port", default=8080, help="run on the given port", type=int)
 

import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)

humidifier_pin = 13
GPIO.setup(humidifier_pin,GPIO.OUT)

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
        if message=="humidifier_on":            
            GPIO.output(humidifier_pin,GPIO.LOW)
        if message=="humidifier_off":            
            GPIO.output(humidifier_pin,GPIO.HIGH)
 
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