#!/usr/bin/env python3
#
# Copyright (C) 2020 UmbraTek Inc. All Rights Reserved.
#
# Software License Agreement (BSD License)
#
# Author: Jimy Zhang <jimy.zhang@umbratek.com> <jimy92@163.com>
# =============================================================================
from utapi.adra.adra_api_base import AdraApiBase
from utapi.common.socket_serial import SocketSerial
from utapi.common.utcc import UtccClient, UtccDecode, UtccType
from utapi.common.utrc import UtrcClient, UtrcDecode, UtrcType


class AdraApiSerial(AdraApiBase):
    def __init__(self, port, baud, bus_type=0):
        """AdraApiSerial is an interface class that controls the ADRA actuator through a serial port.
        USB-to-RS485 or USB-to-CAN module hardware is required to connect the computer and the actuator.

        Args:
            port (string): USB serial port, The default port on Linux is "/dev/ttyUSB0" or "/dev/ttyACM0"
            baud (int): Baud rate of serial communication
            bus_type (int, optional): 0 indicates the actuator that uses the RS485 port.
                                      1 indicates the actuator that uses the CAN port.
                                      Defaults to 0.
        """
        self.DB_FLG = "[SApiSeri] "
        self.__is_err = 0
        id = 1
        print(self.DB_FLG + "SocketSerial, com:%s, baud:%d" % (port, baud))
        if bus_type == 0:
            self.bus_decode = UtrcDecode(0xAA, id)
            self.socket_fp = SocketSerial(port, baud, self.bus_decode)
            if self.socket_fp.is_error() != 0:
                print(self.DB_FLG + "Error: SocketSerial, port:%s, baud:%d" % (port, baud))
                self.__is_err = 1
                return

            self.socket_fp.flush()
            self.bus_client = UtrcClient(self.socket_fp)

            self.tx_data = UtrcType()
            self.tx_data.state = 0x00
            self.tx_data.slave_id = id

        elif bus_type == 1:
            self.bus_decode = UtccDecode(0xAA, id)
            self.socket_fp = SocketSerial(port, baud, self.bus_decode)
            if self.socket_fp.is_error() != 0:
                print(self.DB_FLG + "Error: SocketSerial, port:%s, baud:%d" % (port, baud))
                self.__is_err = 1
                return

            self.socket_fp.flush()
            self.bus_client = UtccClient(self.socket_fp)
            self.tx_data = UtccType()
            self.tx_data.state = 0x00
            self.tx_data.id = id

        self.id = id
        self.virid = id

        AdraApiBase.__init__(self, self.socket_fp, self.bus_client, self.tx_data)

    def is_error(self):
        return self.__is_err

    def into_usb_pm(self):
        """If use the USB of the EtherNet to RS485/CAN module to transmit RS485/CAN data,
        need to use this function to put the EtherNet to RS485/CAN module into USB transmission mode.
        After the EtherNet to RS485/CAN module is powered on, the transmission mode is TCP/UDP by default.
        Therefore, only need to set the transmission mode once you are powered on.
        """
        self.socket_fp.write("# INTO-USB-PM\n".encode("utf-8"))

    def close(self):
        try:
            self.socket_fp.close()
        except Exception:
            pass
