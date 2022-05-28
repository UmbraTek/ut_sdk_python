#!/usr/bin/env python3
#
# Copyright (C) 2020 UmbraTek Inc. All Rights Reserved.
#
# Software License Agreement (BSD License)
#
# Author: Jimy Zhang <jimy.zhang@umbratek.com> <jimy92@163.com>
# =============================================================================
from utapi.common.utrc import UtrcType, UtrcClient, UtrcDecode
from utapi.common.utcc import UtccType, UtccClient
from utapi.common.socket_file import SocketFile
from utapi.adra.adra_api_base import AdraApiBase


class AdraApiFile(AdraApiBase):
    def __init__(self, port, bus_type=0, baud=0):
        u"""AdraApiFile is an interface class that controls the ADRA actuator through a Pcie-serial port.
        NTRO Controller hardware is required to connect the actuator.

        Args:
            port (string): Pcie-Rs485 port, port on NTRO is "/dev/ttyUT0", "/dev/ttyUT1", "/dev/ttyUT2", "/dev/ttyUT3"
            baud (int): Reserved parameter. The baud rate is determined by the driver and cannot be set
            bus_type (int, optional): 0 indicates the actuator that uses the RS485 port.
                                      Defaults to 0.
        """
        self.DB_FLG = "[SApiFile] "
        self.__is_err = 0
        id = 1

        self.bus_decode = UtrcDecode(0xAA, id)
        self.socket_fp = SocketFile(port, 0, self.bus_decode)
        if self.socket_fp.is_error() != 0:
            print(self.DB_FLG + "Error: SocketFile, port:%s", port)
            self.__is_err = 1
            return

        if bus_type == 0:
            self.socket_fp.flush()
            self.bus_client = UtrcClient(self.socket_fp)

            self.tx_data = UtrcType()
            self.tx_data.state = 0x00
            self.tx_data.slave_id = id

        elif bus_type == 1:
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
