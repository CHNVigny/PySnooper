import os
import sys
current_dir = os.getcwd()    # obtain work dir
sys.path.append(current_dir) # add work dir to sys path
import mysocket
import mythreading
import pysnooper
import json

@pysnooper.snoop()
def server_test():
    serversocket = mysocket.ServerSocket()
    thread = mythreading.MyThreading(serversocket)
    serversocket.accept()#这个函数是我自己重新写的

    thread.start()
    count = 10
    dict_s = {}
    while count:
        dict_s[str(count)] = count
        count -= 1
        serversocket.send(json.dumps(dict_s))

if __name__ == '__main__':
    server_test()