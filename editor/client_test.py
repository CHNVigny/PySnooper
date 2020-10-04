import os
import sys
current_dir = os.getcwd()    # obtain work dir
sys.path.append(current_dir) # add work dir to sys path
import mysocket
import mythreading
import pysnooper
import json

@pysnooper.snoop()
def test():
    s = mysocket.ClientSocket()
    thread = mythreading.MyThreading(s)
    s.connect()
    thread.start()
    count = 10
    dict_s = {}
    while count:
        dict_s[str(count)] = count
        count -= 1
        s.send(json.dumps(dict_s))

if __name__ == "__main__":
    test()

