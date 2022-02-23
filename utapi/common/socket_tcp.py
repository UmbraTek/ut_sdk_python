# Copyright 2020 The UmbraTek Inc. All Rights Reserved.
#
# Software License Agreement (BSD License)
#
# Author: Jimy Zhang <jimy.zhang@umbratek.com> <jimy92@163.com>
# =============================================================================

import queue
import socket
import threading
from common import print_msg


class SocketTcp(threading.Thread):
    def __init__(self, ip, port, rxque_max=10, rxdata_len=1024):
        self.DB_FLG = "[SockeTcp] "
        try:
            self.rxdata_len = rxdata_len
            self.rx_que = queue.Queue(rxque_max)

            socket.setdefaulttimeout(1)
            self.fp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.fp.setblocking(1)
            self.fp.connect((ip, port))

            self.is_err = 0
            threading.Thread.__init__(self)
            self.daemon = True
            self.start()
        except Exception as err:
            print(err)
            print(self.DB_FLG + "Error: __init__, ip:%s, port:%d" % (ip, port))
            self.is_err = 1

    def is_error(self):
        return self.is_err

    def run(self):
        self.recv_proc()

    def close(self):
        if self.is_err == 0:
            self.is_err = 1
            self.fp.shutdown(socket.SHUT_RDWR)
            self.fp.close()

    def flush(self, master_id=-1, slave_id=-1):
        if self.is_err != 0:
            return -1
        while not self.rx_que.empty():
            self.rx_que.get()
        return 0

    def write(self, data):
        if self.is_err != 0:
            return -1
        try:
            self.fp.send(data)
            # print_msg.nhex("[SockeTcp] Tx: ", data, len(data))
            return 0
        except Exception as err:
            self.is_err = 1
            print(err)
            print(self.DB_FLG + "Error: write")
            return -1

    def read(self, timeout_s=None):
        if self.is_err != 0:
            print(self.DB_FLG + "Error: read() self.is_err != 0")
            return -1
        # if self.rx_que.empty():
        #    return -1
        try:
            buf = self.rx_que.get(timeout=timeout_s)
            return buf
        except queue.Empty:
            return -1

    def recv_proc(self):
        print(self.DB_FLG + "recv_proc thread start")
        try:
            while self.is_err == 0:
                rx_data = self.fp.recv(self.rxdata_len)
                if len(rx_data) == 0:
                    self.is_err = 0
                    break
                if self.rx_que.full():
                    # print("[SockeTcp] Error! self.rx_que.full")
                    self.rx_que.get()
                self.rx_que.put(rx_data)
                # print_msg.nhex("[SockeTcp] Rx: ", rx_data, len(rx_data))
        except Exception as err:
            self.close()
            self.status = -1
            print(err)
            print(self.DB_FLG + "Error: recv_proc")
        print(self.DB_FLG + "recv_proc exit")
