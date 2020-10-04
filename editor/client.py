import socket

def connectionMade(self):  # 关闭纳格算法
    rfb.RFBClient.connectionMade(self)  # 连接初始化函数

    if self.transport.addressFamily == socket.AF_INET:  # TCP/IP协议族
        self.transport.setTcpNoDelay(True)  # 关闭Nagle's algorithm，不再合并小数据包，有小的数据包立即发送。