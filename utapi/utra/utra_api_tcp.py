#!/usr/bin/env python3
#
# Copyright (C) 2020 UmbraTek Inc. All Rights Reserved.
#
# Software License Agreement (BSD License)
#
# Author: Jimy Zhang <jimy.zhang@umbratek.com> <jimy92@163.com>
# =============================================================================

from utapi.base.arm_api_base import _ArmApiBase
from utapi.common.socket_tcp import SocketTcp
import logging


class UtraApiTcp(_ArmApiBase):
    def __init__(self, ip):
        """This is the API of Umbratek's UTRA series robot arm

        Args:
            ip (string): IP address of UTRA robotic arm
        """
        self.DB_FLG = "[UbotApiTc] "
        self.socket_fp = SocketTcp(ip, 502)
        if self.socket_fp.is_error() != 0:
            logging.error(self.DB_FLG + "Error: SocketTcp")
            return
        _ArmApiBase.__init__(self, self.socket_fp)
