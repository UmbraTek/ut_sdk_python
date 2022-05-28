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
from utapi.common import hex_data
from utapi.common.utcc import UtccClient, UtccType, UtccDecode
from utapi.common.socket_udp import SocketUDP
from utapi.common.socket_tcp import SocketTcp
from utapi.common.socket_serial import SocketSerial
from utapi.common import crc16


class DataLinkApiCan():
    def __init__(self, connect_type, argv, is_reset=1, baud=0xFFFFFFFF):
        u"""DataLinkApiCan is an API class for EtherNet to CAN modules.
        It can read and write CAN data using TCP/UDP/USB transparent transmission.

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
            baud (int, optional): Set the baud rate of the EtherNet to CAN module to be the same as that of the actuator.
                                  If the baud rate is set to 0xFFFFFFFF, the baud rate of the EtherNet to CAN module is not set.
                                  The default value is 0xFFFFFFFF.
        """
        self.DB_FLG = "[DataL CAN] "
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
        self.bus_decode = UtccDecode(0xAA, id)
        socket_fp = SocketTcp(ip, port, self.bus_decode)
        if socket_fp.is_error() != 0:
            print(self.DB_FLG + "Error: SocketTCP, ip:%s, port:%d" % (ip, port))
            self.__is_err = 1
            return
        socket_fp.flush()
        self.bus_client = UtccClient(socket_fp)
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
        self.bus_client = UtccClient(socket_fp)
        ret = self.bus_client.connect_device(baud)
        if ret != 0:
            print(self.DB_FLG + "Error: connect_device: ret = ", ret)
            self.__is_err = 1
            return
        return socket_fp

    def _connect_to_usb(self, port, baud):
        self.bus_decode = UtccDecode(0xAA, id)
        socket_fp = SocketSerial(port, baud, self.bus_decode)
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
        tx_utcc = UtccType()
        tx_utcc.head = 0xAA
        tx_utcc.id = 0x0055
        tx_utcc.state = 0
        tx_utcc.len = 0x08
        tx_utcc.rw = 0
        tx_utcc.cmd = 0x7F
        tx_utcc.data[0:8] = [0x7F, 0x7F, 0x7F, 0x7F, 0x7F, 0x7F, 0x7F]
        buf = tx_utcc.pack()

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

    def write(self, id, len, data):
        u"""Send data, Data is transmitted to CAN through TCP/UDP/USB in specific format.
        Format: 0xAA(uint8_t) + CAN_ID(uint16_t) + CAN_LEN(uint8_t) + CAN_DATA(uint8_t*CAN_LEN) + MODBUS_CRC(uint16_t)

        Args:
            id (int16_t): ID of CAN.
            len (int8_t): Len of CAN.
            data (bytes): Data of CAN.

        Returns:
            int: 1: Fails
                 0: Successful
        """
        buf = bytes([0xAA])
        buf += hex_data.uint16_to_bytes_big(id)
        buf += bytes([len])
        for i in range(len):
            buf += bytes([data[i]])
        crc = crc16.crc_modbus(buf)
        buf += crc
        return self.socket_fp.write(buf)

    def read(self, timeout_s=None):
        u"""Receiving data, Receives data from CAN in specific format.
        Format: 0xAA(uint8_t) + CAN_ID(uint16_t) + CAN_LEN(uint8_t) + CAN_DATA(uint8_t*CAN_LEN) + MODBUS_CRC(uint16_t)

        Args:
            timeout_s (float, optional): Block time (unit: second).
                      If set to 0, the system blocks for a long time until data is received.

        Returns:
            int or list: -1: No data is received.
                        Otherwise, list data is received. [can_id can_len can_data].
        """
        while 1:
            buf = self.socket_fp.read(timeout_s)
            if buf == -1:
                return -1

            buf_len = len(buf)
            crc1 = [buf[buf_len - 2], buf[buf_len - 1]]
            temp1 = hex_data.bytes_to_uint16_big(crc1)
            crc2 = crc16.crc_modbus(buf[0:buf_len - 2])
            temp2 = hex_data.bytes_to_uint16_big(crc2)
            if temp1 != temp2:
                print(self.DB_FLG + "Error, The CRC check of received data is incorrect.")
                continue

            can_id = hex_data.bytes_to_uint16_big(buf[1:3])
            can_len = buf[3]
            can_data = [0] * can_len
            for i in range(can_len):
                can_data[i] = buf[4 + i]
            return [can_id, can_len, can_data]
