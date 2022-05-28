#!/usr/bin/env python3
#
# Copyright (C) 2020 UmbraTek Inc. All Rights Reserved.
#
# Software License Agreement (BSD License)
#
# Author: Jimy Zhang <jimy.zhang@umbratek.com> <jimy92@163.com>
# =============================================================================
from utapi.common.utrc import UtrcType, UtrcClient, UtrcDecode
from utapi.common.socket_file import SocketFile
from utapi.cgpio.cgpio_api_base import CgpioApiBase


class CgpioApiFile(CgpioApiBase):
    def __init__(self, port="/dev/ttyUT2", baud=921600):
        u"""CgpioApiFile is an interface class that controls the NTRO GPIO through a Pcie-serial port.

        Args:
            port (string): Fixed is "/dev/ttyUT2"
            baud (int): Fixed is 921600
        """
        self.DB_FLG = "[CApiFile] "
        self.__is_err = 0
        id = 1

        self.bus_decode = UtrcDecode(0xAA, id)
        self.socket_fp = SocketFile(port, 0, self.bus_decode)
        if self.socket_fp.is_error() != 0:
            print(self.DB_FLG + "Error: SocketFile, port:%s", port)
            self.__is_err = 1
            return

        self.socket_fp.flush()
        self.bus_client = UtrcClient(self.socket_fp)

        self.tx_data = UtrcType()
        self.tx_data.state = 0x00
        self.tx_data.slave_id = id

        self.id = id
        self.virid = id

        CgpioApiBase.__init__(self, self.socket_fp, self.bus_client, self.tx_data)
