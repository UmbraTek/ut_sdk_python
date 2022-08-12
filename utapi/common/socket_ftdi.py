#!/usr/bin/env python3
#
# Copyright (C) 2020 UmbraTek Inc. All Rights Reserved.
#
# Software License Agreement (BSD License)
#
# Author: Jimy Zhang <jimy.zhang@umbratek.com> <jimy92@163.com>
# =============================================================================
import queue
import threading
import serial
import pyftdi
import pyftdi.ftdi
import time
import usb
import usb.core
import usb.util


class SocketFtdi(threading.Thread):
    def __init__(self, bus, address, baud, bus_decode=-1, rxque_max=10):
        self.DB_FLG = "[SockeSer] "
        try:
            """
            dev = usb.core.find(idVendor=0x0403, idProduct=0x6014, find_all=True)
            if dev is None:
                raise ValueError("device not found")
            else:
                for i in dev:
                    print(i)
            """
            self.is_err = 0
            self.rx_que = queue.Queue(rxque_max)
            self.rx_decoder = bus_decode

            self.ftdi = pyftdi.ftdi.Ftdi()
            self.ftdi.open(0x0403, 0x6014, bus, address)
            self.ftdi.set_latency_timer(1)
            self.set_baud(baud)

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
            self.ftdi.close()
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
            self.ftdi.set_baudrate(baud)
            pass

    def write(self, data):
        if self.is_err != 0:
            return -1
        try:
            self.time1 = time.time_ns()
            self.ftdi.write_data(data)
            self.time2 = time.time_ns()
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
            self.time5 = time.time_ns()
            buf = self.rx_que.get(timeout=timeout_s)
            self.time6 = time.time_ns()
            return buf
        except queue.Empty:
            return -1

    def recv_proc(self):
        print(self.DB_FLG + "recv_proc thread start")
        try:
            while self.is_err == 0:
                rxch = self.ftdi.read_data(1)
                if (len(rxch) <= 0):
                    continue
                if self.rx_decoder == -1:
                    if self.rx_que.full():
                        self.rx_que.get()
                    self.rx_que.put(rxch)
                else:
                    self.time3 = time.time_ns()
                    self.rx_decoder.put(rxch, 1, self.rx_que)
                    self.time4 = time.time_ns()
        except Exception as err:
            self.close()
            self.is_err = 1
            print(err)
            print(self.DB_FLG + "Error: recv_proc")
        print(self.DB_FLG + 'recv_proc exit')
