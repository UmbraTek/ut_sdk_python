# Copyright 2020 The UmbraTek Inc. All Rights Reserved.
#
# Software License Agreement (BSD License)
#
# Author: Jimy Zhang <jimy.zhang@umbratek.com> <jimy92@163.com>
# =============================================================================
from common.utrc import UtrcType, UtrcClient, UtrcDecode
from common.utcc import UtccType, UtccClient
from common.socket_serial import SocketSerial

from adra.adra_api_base import AdraApiBase


class AdraApiSerial(AdraApiBase):
    def __init__(self, port, baud, bus_type=0):
        u"""AdraApiSerial is an interface class that controls the ADRA actuator through a serial port.
        USB-to-RS485 or USB-to-CAN module hardware is required to connect the computer and the actuator.

        Args:
            port (string): USB serial port, The default port on Linux is "/dev/ttyUSB0"
            baud (int): Baud rate of serial communication
            bus_type (int, optional): 0 indicates the actuator that uses the RS485 port.
                                      1 indicates the actuator that uses the CAN port.
                                      Defaults to 0.
        """
        self.DB_FLG = "[SApiSeri] "
        self.__is_err = 0
        id = 1

        self.bus_decode = UtrcDecode(0xAA, id)
        self.socket_fp = SocketSerial(port, baud, self.bus_decode)
        if self.socket_fp.is_error() != 0:
            print(self.DB_FLG + "Error: SocketSerial, port:%s, baud:%d" % (port, baud))
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

        AdraApiBase.__init__(self, self.socket_fp, self.bus_client, self.tx_data)
