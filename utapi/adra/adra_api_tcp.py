# Copyright 2020 The UmbraTek Inc. All Rights Reserved.
#
# Software License Agreement (BSD License)
#
# Author: Jimy Zhang <jimy.zhang@umbratek.com> <jimy92@163.com>
# =============================================================================
from common.utrc import UtrcType, UtrcClient, UtrcDecode
from common.utcc import UtccType, UtccClient, UtccDecode
from common.socket_tcp import SocketTcp
from adra.adra_api_base import AdraApiBase
import time
import socket


class AdraApiTcp(AdraApiBase):
    def __init__(self, ip, port=6001, bus_type=0, is_reset=1, udp_port=5001):
        u"""AdraApiTcp is an interface class that controls the ADRA actuator through a EtherNet TCP.
        EtherNet-to-RS485 or EtherNet-to-CAN module hardware is required to connect the computer and the actuator.

        Args:
            ip (string): IP address of the EtherNet module.
            port (int): TCP port of EtherNet module. The default value is 6001.
            bus_type (int, optional): 0 indicates the actuator that uses the RS485 port.
                                      1 indicates the actuator that uses the CAN port.
                                      Defaults to 0.
            is_reset (int, optional): Defaults to 1. Whether to reset can be reset in the following situations.
                    1. If connection type is UDP and DataLink is connected to TCP after being powered on, reset is required.
                    2. If connection type is UDP and DataLink is not connected to TCP after being powered on, you do not need to reset.
                    3. If connection type is TCP and DataLink is connected to TCP or UDP after being powered on, reset is required.
                    4. If connection type is TCP and DataLink is not connected to TCP or UDP after being powered on, you do not need to reset.
                    Note: In any case, it is good to use reset, but the initialization time is about 3 seconds longer than that without reset.
                    Note: After DataLink is powered on and connected to USB, it needs to be powered on again to connect to TCP or UDP.
            udp_port (int, optional): UDP port of EtherNet module. The default value is 5001.
        """
        self.DB_FLG = "[Adra Tcp] "
        self.__is_err = 0
        id = 1
        print(self.DB_FLG + "SocketTcp, ip:%s, port:%d" % (ip, port))

        if bus_type == 0:
            if is_reset:
                self._reset_net_rs485(ip, port, udp_port)
            self.bus_decode = UtrcDecode(0xAA, id)
            self.socket_fp = SocketTcp(ip, port, self.bus_decode)
            if self.socket_fp.is_error() != 0:
                print(self.DB_FLG + "Error: SocketTcp, ip:%s, port:%d" % (ip, port))
                self.__is_err = 1
                return

            self.socket_fp.flush()
            self.bus_client = UtrcClient(self.socket_fp)
            ret = self.bus_client.connect_device()
            if ret != 0:
                self.__is_err = 1
                print(self.DB_FLG + "Error: connect_device: ret = ", ret)

            self.tx_data = UtrcType()
            self.tx_data.state = 0x00
            self.tx_data.slave_id = id
        elif bus_type == 1:
            if is_reset:
                self._reset_net_can(ip, port, udp_port)
            self.bus_decode = UtccDecode(0xAA, id)
            self.socket_fp = SocketTcp(ip, port, self.bus_decode)
            if self.socket_fp.is_error() != 0:
                print(self.DB_FLG + "Error: SocketTcp, ip:%s, port:%d" % (ip, port))
                self.__is_err = 1
                return

            self.socket_fp.flush()
            self.bus_client = UtccClient(self.socket_fp)
            ret = self.bus_client.connect_device()
            if ret != 0:
                self.__is_err = 1
                print(self.DB_FLG + "Error: connect_device: ret = ", ret)

            self.tx_data = UtccType()
            self.tx_data.state = 0x00
            self.tx_data.id = id

        self.id = id
        self.virid = id

        AdraApiBase.__init__(self, self.socket_fp, self.bus_client, self.tx_data)

    def is_error(self):
        return self.__is_err

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
            pass
        time.sleep(0.1)

        try:
            print(self.DB_FLG + "Reset Net Step2: connect to udp")
            addr = (ip, udp_port)
            fp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            fp.sendto(buf, addr)
        except Exception as err:
            pass
        self.__is_err = 0
        time.sleep(3)

    def _reset_net_can(self, ip, tcp_port, udp_port):
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
            pass
        time.sleep(0.1)

        try:
            print(self.DB_FLG + "Reset Net Step2: connect to udp")
            addr = (ip, udp_port)
            fp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            fp.sendto(buf, addr)
        except Exception as err:
            pass
        self.__is_err = 0
        time.sleep(3)
