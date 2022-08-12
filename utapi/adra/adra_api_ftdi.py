#!/usr/bin/env python3
#
# Copyright (C) 2020 UmbraTek Inc. All Rights Reserved.
#
# Software License Agreement (BSD License)
#
# Author: Jimy Zhang <jimy.zhang@umbratek.com> <jimy92@163.com>
# =============================================================================
from utapi.common.utrc import UtrcType, UtrcClient, UtrcDecode
from utapi.common.utcc import UtccType, UtccClient, UtccDecode
from utapi.common.socket_ftdi import SocketFtdi

from utapi.adra.adra_api_base import AdraApiBase


class AdraApiFtdi(AdraApiBase):
    def __init__(self, bus, address, baud, bus_type=0):
        u"""AdraApiFtdi is an interface class that controls the ADRA actuator through a serial port.
        USB-to-RS485 or USB-to-CAN module hardware is required to connect the computer and the actuator.

        Args:
            bus (int): USB bus
            address (int): USB address on bus
            baud (int): Baud rate of serial communication
            bus_type (int, optional): 0 indicates the actuator that uses the RS485 port.
                                      1 indicates the actuator that uses the CAN port.
                                      Defaults to 0.
        """
        self.DB_FLG = "[SApiFtdi] "
        self.__is_err = 0
        id = 1
        print(self.DB_FLG + "SocketFtdi, bus:%d, address:%d, baud:%d" % (bus, address, baud))
        if bus_type == 0:
            self.bus_decode = UtrcDecode(0xAA, id)
            self.socket_fp = SocketFtdi(bus, address, baud, self.bus_decode)
            if self.socket_fp.is_error() != 0:
                print(self.DB_FLG + "Error: SocketFtdi, bus:%d, address:%d, baud:%d" % (bus, address, baud))
                self.__is_err = 1
                return

            self.socket_fp.flush()
            self.bus_client = UtrcClient(self.socket_fp)

            self.tx_data = UtrcType()
            self.tx_data.state = 0x00
            self.tx_data.slave_id = id

        self.id = id
        self.virid = id

        AdraApiBase.__init__(self, self.socket_fp, self.bus_client, self.tx_data)

    def is_error(self):
        return self.__is_err

    def into_usb_pm(self):
        pass
