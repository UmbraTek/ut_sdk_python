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


class AdraApiTcp(AdraApiBase):
    def __init__(self, ip, port=6001, bus_type=0):
        u"""AdraApiTcp is an interface class that controls the ADRA actuator through a EtherNet TCP.
        EtherNet-to-RS485 or EtherNet-to-CAN module hardware is required to connect the computer and the actuator.

        Args:
            ip (string): IP address of the EtherNet module.
            port (int): TCP port of EtherNet module. The default value is 6001.
            bus_type (int, optional): 0 indicates the actuator that uses the RS485 port.
                                      1 indicates the actuator that uses the CAN port.
                                      Defaults to 0.
        """
        self.DB_FLG = "[Adra Tcp] "
        self.__is_err = 0
        id = 1
        print(self.DB_FLG + "SocketTcp, ip:%s, port:%d" % (ip, port))

        if bus_type == 0:
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
