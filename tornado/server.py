import tornado.ioloop
import tornado.web
from tornado import websocket
import json
import re

answer_template = ""



wss = []    # Web-sockets


class MainHandler(tornado.web.RequestHandler):

    def get(self):
        # self.render("index.html")
        pass

    def post(self):
        print self.request.body
        json_data = json.loads(self.request.body)
        print json_data['new_answer']['url']

        for ws in wss:
            if ws.url == json_data['new_answer']['url']:
                ws.on_message(self.request.body)



class EchoWebSocket(tornado.websocket.WebSocketHandler):
    clients = [] 
    def check_origin(self, origin):
        return True

    def open(self):
        self.clients.append(self)
        # print 'new connection'
        self.write_message("Hello from server")

        wss.append(self)

    def on_message(self, message):

        try:
            temp_message = json.loads(message)
        except Exception, e:
            return
        key = temp_message.keys()[0]

        if key == 'url':
            url = temp_message[key]
            url = re.findall(r'http:\/\/[a-z0-9A-Z.\/]+question\/\d+', url)[0]
            self.url = url
        elif key == 'answer_template':
            with open('answer_template', 'r') as myfile:
                answer_template = myfile.read()
                json_answer = json.dumps({"answer_template": answer_template})
                self.write_message(json_answer)
        elif key == 'new_answer':
            self.write_message(message)
        else:
            pass

    def on_close(self):
        self.clients.remove(self)
        wss.remove(self)
        # print 'closed connection'





application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/test", EchoWebSocket),
])


if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()