# Copyright 2020 The UmbraTek Inc. All Rights Reserved.
#
# Software License Agreement (BSD License)
#
# Author: Jimy Zhang <jimy.zhang@umbratek.com> <jimy92@163.com>
# =============================================================================
import threading
import socket
import queue
from common import print_msg


class SocketUDP(threading.Thread):

    def __init__(self, ip, port, rxque_max=8):
        self.DB_FLG = "[SockeUDP] "
        try:
            self.addr = (ip, port)
            self.rx_que = queue.Queue(rxque_max)
            self.fp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

            self.is_err = 0
            threading.Thread.__init__(self)
            self.daemon = True
            self.start()
        except Exception as err:
            print(err)
            print(self.DB_FLG + "Error: __init__")
            self.is_err = 1

    def is_error(self):
        return self.is_err

    def run(self):
        self.recv_proc()

    def close(self):
        if self.is_err == 0:
            self.fp.close()
            self.is_err = 1

    def flush(self):
        if self.is_err != 0:
            return -1
        while not self.rx_que.empty():
            self.rx_que.get()
        return 0

    def write(self, data):
        if self.is_err != 0:
            return -1
        try:
            self.fp.sendto(data, self.addr)
            # print_msg.nhex("[SockeUDP] write: ", data, len(data))
            return 0
        except Exception as err:
            self.is_err = 1
            self.close()
            print(err)
            print(self.DB_FLG + "Error: write")
            return -1

    def read(self, timeout_s=None):
        if self.is_err != 0:
            return -1
        try:
            buf = self.rx_que.get(timeout=timeout_s)
            return buf
        except queue.Empty:
            return -1

    def recv_proc(self):
        print(self.DB_FLG + 'recv_proc thread start')
        try:
            while self.is_err == 0:
                rx_data, addr = self.fp.recvfrom(1024)
                if self.addr != addr:
                    print(self.DB_FLG + "Error: recvfrom")
                    print(self.DB_FLG + "self.addr: ", self.addr)
                    print(self.DB_FLG + "addr: ", addr)
                    continue
                if len(rx_data) == 0:
                    self.is_err = 0
                    break
                if self.rx_que.full():
                    self.rx_que.get()
                self.rx_que.put(rx_data)
                # print_msg.nhex("[SockeUDP] read: ", rx_data, len(rx_data))
        except Exception as err:
            self.close()
            self.is_err = 1
            print(err)
            print(self.DB_FLG + "Error: recv_proc")
        print(self.DB_FLG + 'recv_proc exit')
