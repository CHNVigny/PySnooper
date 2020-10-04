import threading
import json

class MyThreading(threading.Thread):
    def __init__(self, socket, server = True, send = True):
        """
        server: True == 是服务器
        send: True == 是发送线程
        """
        threading.Thread.__init__(self)
        self.socket = socket
        self.server = server
        self.send = send
#        self.socket.accept()


    def run(self):
        #线程内要做的事
        while 1:
            dict_json = self.recv_func()
            # if str:
            #     print(str)
            dict_s = json.loads(dict_json)
            print(dict_s)
            #print(type(dict_s))


    def send_func(self, str):
        pass

    def recv_func(self):
        return self.socket.recv()

