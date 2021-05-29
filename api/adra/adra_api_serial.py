# Copyright 2020 The UmbraTek Inc. All Rights Reserved.
#
# Software License Agreement (BSD License)
#
# Author: Jimy Zhang <jimy.zhang@umbratek.com> <jimy92@163.com>
# =============================================================================
from common.utrc import UtrcType, UtrcClient, UtrcDecode
from common.utcc import UtccType, UtccClient
from common.socket_serial import SocketSerial
from adra.adra_api_base import _AdraApiBase


class AdraApiSerial(_AdraApiBase):
    def __init__(self, port, baud, is_can=0):
        """The AdraApiSerial class is an interface class for controlling ADRA connectors through the serial port. 
        It needs to connect the serial port to RS485 module or TCP/IP to CAN module

        Args:
            port (string): the port of the serial port, generally linux defaults to "/dev/ttyUSB0"
            baud (int): communication baud rate
            is_can (int, optional): 0 means RS485 communication; 1 means CAN communication. Defaults to 0.
        """
        self.DB_FLG = '[SApiSeri] '
        self.__is_err = 0
        id = 1

        self.bus_decode = UtrcDecode(0xAA, id)
        self.socket_fp = SocketSerial(port, baud, self.bus_decode)
        if self.socket_fp.is_error() != 0:
            print(self.DB_FLG + "Error: SocketSerial, port:%s, baud:%d" % (port, baud))
            self.__is_err = 1
            return

        if is_can:
            self.socket_fp.flush()
            self.bus_client = UtccClient(self.socket_fp)
            ret = self.bus_client.connect_device()
            if (ret != 0):
                self.__is_err = 1
                print(self.DB_FLG + "Error: connect_device: ret = ", ret)

            self.tx_data = UtccType()
            self.tx_data.state = 0x00
            self.tx_data.id = id
        else:
            self.socket_fp.flush()
            self.bus_client = UtrcClient(self.socket_fp)

            self.tx_data = UtrcType()
            self.tx_data.state = 0x00
            self.tx_data.slave_id = id

        _AdraApiBase.__init__(self, self.socket_fp, self.bus_client, self.tx_data)
