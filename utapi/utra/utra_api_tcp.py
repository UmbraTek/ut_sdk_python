#!/usr/bin/env python3
#
# Copyright (C) 2020 UmbraTek Inc. All Rights Reserved.
#
# Software License Agreement (BSD License)
#
# Author: Jimy Zhang <jimy.zhang@umbratek.com> <jimy92@163.com>
# =============================================================================

from utapi.base.arm_api_base import _ArmApiBase
from utapi.common.socket_tcp import SocketTcp
from utapi.common.utrc import UtrcType, UtrcClient, UtrcDecode
import logging
import time
import socket


class UtraApiTcp(_ArmApiBase):
    def __init__(self, ip):
        """This is the API of Umbratek's UTRA series robot arm

        Args:
            ip (string): IP address of UTRA robotic arm
        """
        self.DB_FLG = "[UbotApiTc] "
        self.socket_fp = SocketTcp(ip, 502)
        if self.socket_fp.is_error() != 0:
            logging.error(self.DB_FLG + "Error: SocketTcp")
            return
        _ArmApiBase.__init__(self, self.socket_fp)
    def _reset_net_rs485(self, ip, tcp_port, udp_port):
        tx_utrc = UtrcType()
        tx_utrc.master_id = 0xAA
        tx_utrc.slave_id = 0x55
        tx_utrc.state = 0
        tx_utrc.len = 0x08
        tx_utrc.rw = 0
        tx_utrc.cmd = 0x7F
        tx_utrc.data[0:8] = [0x7F, 0x7F, 0x7F, 0x7F, 0x7F, 0x7F, 0x7F]
        buf = tx_utrc.pack()
        try:
            print(self.DB_FLG + "Reset Net Step1: connect to tcp")
            fp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            fp.connect((ip, tcp_port))
            fp.send(buf)
        except Exception as err:
            print(err)
        time.sleep(0.1)

        try:
            print(self.DB_FLG + "Reset Net Step2: connect to udp")
            addr = (ip, udp_port)
            fp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            fp.sendto(buf, addr)
        except Exception as err:
            print(err)
        self.__is_err = 0
        time.sleep(3)
