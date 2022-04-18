# Copyright 2020 The UmbraTek Inc. All Rights Reserved.
#
# Software License Agreement (BSD License)
#
# Author: Jimy Zhang <jimy.zhang@umbratek.com> <jimy92@163.com>
# =============================================================================
import queue
import threading
import serial
from common import print_msg


class SocketSerial(threading.Thread):
    def __init__(self, port, baud, bus_decode=-1, rxque_max=10):
        self.DB_FLG = "[SockeSer] "
        try:
            self.rx_que = queue.Queue(rxque_max)
            self.rx_decoder = bus_decode
            self.com = serial.Serial(port=port, baudrate=baud)
            if not self.com.isOpen():
                self.is_err = 1
                return

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
            self.com.close()
            self.is_err = 1

    def flush(self, master_id=-1, slave_id=-1):
        if self.is_err != 0:
            return -1
        while not self.rx_que.empty():
            self.rx_que.get()
        if self.rx_decoder != -1:
            self.rx_decoder.flush(master_id, slave_id)
        return 0

    def get_baud(self):
        if self.is_err == 0:
            return self.com.baudrate
        return 0

    def set_baud(self, baud):
        if self.is_err == 0:
            self.com.baudrate = baud

    def write(self, data):
        if self.is_err != 0:
            return -1
        try:
            self.com.write(data)
            # print_msg.nhex("[SockSeri] write: ", data, len(data))
            return 0
        except Exception as err:
            self.is_err = 1
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
        print(self.DB_FLG + "recv_proc thread start")
        try:
            while self.is_err == 0:
                rxch = self.com.read()
                if (len(rxch) <= 0):
                    continue
                if self.rx_decoder == -1:
                    if self.rx_que.full():
                        self.rx_que.get()
                    self.rx_que.put(rxch)
                else:
                    self.rx_decoder.put(rxch, 1, self.rx_que)
        except Exception as err:
            self.close()
            self.is_err = 1
            print(err)
            print(self.DB_FLG + "Error: recv_proc")
        print(self.DB_FLG + 'recv_proc exit')
