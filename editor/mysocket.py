import socket
import pysnooper
import os
import sys
current_dir = os.getcwd()    # obtain work dir
sys.path.append(current_dir) # add work dir to sys path
import mythreading

class ServerSocket():
    def __init__(self, family = socket.AF_INET, type = socket.SOCK_STREAM, host = socket.gethostname(), self_port = 10032):
        self.socket = socket.socket(family = family, type = type)
        self.socket.bind((host,self_port))
        self.socket.listen(5)

    def accept(self):
        self.client, addr = self.socket.accept()

    def send(self, str):#只能传送字符串。
        self.client.send(str.encode('utf-8'))

    def recv(self, buffer=1024):
        return self.client.recv(buffer).decode()

    def close_c(self):
        self.client.close()

    def close_s(self):
        self.socket.close()

class ClientSocket():
    def __init__(self, family = socket.AF_INET, type = socket.SOCK_STREAM, host = socket.gethostname(), self_port = 10032, server_port = 10032):
        self.socket = socket.socket(family = family, type = type)
        self.server_port = server_port
    def connect(self, host = socket.gethostname()):
        self.socket.connect((host, self.server_port))

    def send(self, str):
        self.socket.send(str.encode('utf-8'))

    def recv(self, buffer=1024):
        return self.socket.recv(buffer).decode()

    def close(self):
        self.socket.close()





@pysnooper.snoop()
def test():
    serversocket = ServerSocket()
    serversocket.accept()#这个函数是我自己重新写的
    thread = mythreading.MyThreading(serversocket)
    thread.start()
    count = 10
    while count:
        message = "input message：" + str(count) + "\n"
        count -= 1
        serversocket.send(message)

if __name__ == '__main__':
    test()


