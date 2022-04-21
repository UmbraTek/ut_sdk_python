# Copyright 2020 The UmbraTek Inc. All Rights Reserved.
#
# Software License Agreement (BSD License)
#
# Author: Jimy Zhang <jimy.zhang@umbratek.com> <jimy92@163.com>
# =============================================================================
from common.utrc import UtrcType, UtrcClient
from common.utcc import UtccType, UtccClient
from common.socket_udp import SocketUDP
from adra.adra_api_base import AdraApiBase


class AdraApiUdp(AdraApiBase):
    def __init__(self, ip, port=5001, bus_type=0):
        u"""AdraApiUdp is an interface class that controls the ADRA actuator through a EtherNet UDP.
        EtherNet-to-RS485 or EtherNet-to-CAN module hardware is required to connect the computer and the actuator.

        Args:
            ip (string): IP address of the EtherNet module.
            port (int): UDP port of EtherNet module. The default value is 5001.
            bus_type (int, optional): 0 indicates the actuator that uses the RS485 port.
                                      1 indicates the actuator that uses the CAN port.
                                      Defaults to 0.
        """
        self.DB_FLG = "[Adra Udp] "
        self.__is_err = 0
        id = 1
        print(self.DB_FLG + "SocketUDP, ip:%s, port:%d" % (ip, port))
        self.socket_fp = SocketUDP(ip, port)
        if self.socket_fp.is_error() != 0:
            print(self.DB_FLG + "Error: SocketUDP, ip:%s, port:%d" % (ip, port))
            self.__is_err = 1
            return

        if bus_type == 1:
            self.socket_fp.flush()
            self.bus_client = UtccClient(self.socket_fp)
            ret = self.bus_client.connect_device()
            if ret != 0:
                self.__is_err = 1
                print(self.DB_FLG + "Error: connect_device: ret = ", ret)

            self.tx_data = UtccType()
            self.tx_data.state = 0x00
            self.tx_data.id = id

        elif bus_type == 0:
            self.socket_fp.flush()
            self.bus_client = UtrcClient(self.socket_fp)
            ret = self.bus_client.connect_device()
            if ret != 0:
                self.__is_err = 1
                print(self.DB_FLG + "Error: connect_device: ret = ", ret)

            self.tx_data = UtrcType()
            self.tx_data.state = 0x00
            self.tx_data.slave_id = id

        self.id = id
        self.virid = id

        AdraApiBase.__init__(self, self.socket_fp, self.bus_client, self.tx_data)

    def is_error(self):
        return self.__is_err
