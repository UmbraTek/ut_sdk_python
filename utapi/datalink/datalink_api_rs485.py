#!/usr/bin/env python3
#
# Copyright (C) 2022 UmbraTek Inc. All Rights Reserved.
#
# Software License Agreement (BSD License)
#
# Author: Jimy Zhang <jimy.zhang@umbratek.com> <jimy92@163.com>
# =============================================================================
import time
import socket
from common.utrc import UtrcClient, UtrcType
from common.socket_udp import SocketUDP
from common.socket_tcp import SocketTcp
from common.socket_serial import SocketSerial


class DataLinkApiRs485():
    def __init__(self, connect_type, argv, is_reset=1, baud=0xFFFFFFFF):
        u"""DataLinkApiRs485 is an API class for EtherNet to RS485 modules.
        It can read and write RS485 data using TCP/UDP/USB transparent transmission.

        Args:
            connect_type (int): 1: Use TCP to transfer data.
                                2: Use UDP to transfer data.
                                3: Use USB to transfer data.
            argv (list): If TCP/UDP is used, argv is a list of three data. [IP tcp_port udp_port].
                                IP address and two port numbers of the EtherNet module.
                         If USB is used, argv is a list of two data, [port, baud].
                                USB virtual serial number and baud rate, which is fixed at 921600.
            is_reset (int, optional):  Defaults to 1. Whether to reset can be reset in the following situations.
                    1. If connection type is UDP and DataLink is connected to TCP after being powered on, reset is required.
                    2. If connection type is UDP and DataLink is not connected to TCP after being powered on, you do not need to reset.
                    3. If connection type is TCP and DataLink is connected to TCP or UDP after being powered on, reset is required.
                    4. If connection type is TCP and DataLink is not connected to TCP or UDP after being powered on, you do not need to reset.
                    5. If connection type is USB and DataLink is not connected to USB after being powered on, reset is required.
                    6. If connection type is USB and DataLink is connected to USB after being powered on, you do not need to reset.
                    Note: In any case, it is good to use reset, but the initialization time is about 3 seconds longer than that without reset.
                    Note: After DataLink is powered on and connected to USB, it needs to be powered on again to connect to TCP or UDP.
            baud (int, optional): Set the baud rate of the EtherNet to RS485 module to be the same as that of the actuator.
                                  If the baud rate is set to 0xFFFFFFFF, the baud rate of the EtherNet to RS485 module is not set.
                                  The default value is 0xFFFFFFFF.
        """
        self.DB_FLG = "[DataL RS ] "
        self.__is_err = 0

        if connect_type == 1:
            self.ip = argv[0]
            self.tcp_port = argv[1]
            self.udp_port = argv[2]
            print(self.DB_FLG + "Connect To TCP, IP: %s, PORT[TCP UDP]: [%d %d], baud:%d" %
                  (self.ip, self.tcp_port, self.udp_port, baud))
            if is_reset:
                self._reset_net(self.ip, self.tcp_port, self.udp_port)
            self.socket_fp = self._connect_to_tcp(self.ip, self.tcp_port, baud)

        elif connect_type == 2:
            self.ip = argv[0]
            self.tcp_port = argv[1]
            self.udp_port = argv[2]
            print(self.DB_FLG + "Connect To UDP, IP: %s, PORT[TCP UDP]: [%d %d], baud:%d" %
                  (self.ip, self.tcp_port, self.udp_port, baud))
            if is_reset:
                self._reset_net(self.ip, self.tcp_port, self.udp_port)
            self.socket_fp = self._connect_to_udp(self.ip, self.udp_port, baud)

        elif connect_type == 3:
            self.com = argv[0]
            self.baud = argv[1]
            print(self.DB_FLG + "Connect To USB, COM: %s, Baud: %d" % (self.com, self.baud))
            self.socket_fp = self._connect_to_usb(self.com, self.baud)
            if is_reset:
                self._into_usb_pm()
        else:
            self.__is_err = 1
            return

    def _connect_to_tcp(self, ip, port, baud):
        socket_fp = SocketTcp(ip, port)
        if socket_fp.is_error() != 0:
            print(self.DB_FLG + "Error: SocketTCP, ip:%s, port:%d" % (ip, port))
            self.__is_err = 1
            return
        socket_fp.flush()
        self.bus_client = UtrcClient(socket_fp)
        ret = self.bus_client.connect_device(baud)
        if ret != 0:
            print(self.DB_FLG + "Error: connect_device: ret = ", ret)
            self.__is_err = 1
            return
        return socket_fp

    def _connect_to_udp(self, ip, port, baud):
        socket_fp = SocketUDP(ip, port)
        if socket_fp.is_error() != 0:
            print(self.DB_FLG + "Error: SocketUDP, ip:%s, port:%d" % (ip, port))
            self.__is_err = 1
            return
        socket_fp.flush()
        self.bus_client = UtrcClient(socket_fp)
        ret = self.bus_client.connect_device(baud)
        if ret != 0:
            print(self.DB_FLG + "Error: connect_device: ret = ", ret)
            self.__is_err = 1
            return
        return socket_fp

    def _connect_to_usb(self, port, baud):
        socket_fp = SocketSerial(port, baud)
        if socket_fp.is_error() != 0:
            print(self.DB_FLG + "Error: SocketSerial, ip:%s, port:%d" % (port, baud))
            self.__is_err = 1
            return
        socket_fp.flush()
        return socket_fp

    def _into_usb_pm(self):
        self.socket_fp.write("# INTO-USB-PM\n".encode('utf-8'))
        time.sleep(1)

    def _reset_net(self, ip, tcp_port, udp_port):
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

    def is_error(self):
        u"""Gets the connection status of the DataLink.

        Returns:
            int: 1: The connection fails.
                 0: The connection is successful.
        """
        return self.__is_err

    def close(self):
        return self.socket_fp.close()

    def flush(self):
        u"""Clears received cached data.

        Returns:
            _type_: None
        """
        return self.socket_fp.flush()

    def write(self, data):
        u"""Send data, Data is transmitted to RS485 through TCP/UDP/USB in the original format.

        Args:
            data (bytes): Bytes Data.

        Returns:
            int: 1: Fails
                 0: Successful
        """
        return self.socket_fp.write(data)

    def read(self, timeout_s=None):
        u"""Receiving data, Receives data from RS485 in the original format.

        Args:
            timeout_s (float, optional): Block time (unit: second).
                      If set to 0, the system blocks for a long time until data is received.

        Returns:
            int or bytes: -1: No data is received. Otherwise, bytes data is received.
        """
        return self.socket_fp.read(timeout_s)
