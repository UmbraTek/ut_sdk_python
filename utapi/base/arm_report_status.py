# Copyright 2020 The UmbraTek Inc. All Rights Reserved.
#
# Software License Agreement (BSD License)
#
# Author: Jimy Zhang <jimy.zhang@umbratek.com> <jimy92@163.com>
# =============================================================================
import struct
import threading
from common import print_msg
from common.socket_tcp import SocketTcp
import logging


class ArmReportStatus(threading.Thread):
    def __init__(self, ip, port):
        self.__is_err = 0
        self.__rxcnt = 0
        self.__is_update = 0

        self.axis = 0
        self.motion_status = 0
        self.motion_mode = 0
        self.mt_brake = 0
        self.mt_able = 0
        self.err_code = 0
        self.war_code = 0
        self.cmd_num = 0
        self.joint = [0] * 32
        self.pose = [0] * 6
        self.tau = [0] * 32

        self.__socekt_fp = SocketTcp(ip, port, 32)
        if self.__socekt_fp.is_error() != 0:
            logging.error("[UbotRStat] Error: SocketTcp failed, ip: %s, port: %d" % (ip, port))
            return -1
        logging.info("[UbotRStat] Tcp Report Status connection successful")

        threading.Thread.__init__(self)
        self.daemon = True
        self.start()

    def run(self):

        while self.__is_err == 0:
            rx_data = self.__socekt_fp.read()
            if rx_data == -1 or len(rx_data) <= 5:
                continue

            self.__rxcnt += 1
            self.flush_data(rx_data)

        if self.__socekt_fp:
            self.__socekt_fp.close()
            logging.info('ubot report status close')

    def close(self):
        self.__is_err = -1

    def is_err(self):
        return self.__is_err

    def flush_data(self, rx_data):
        if len(rx_data) % 89 != 0:
            logging.info("[UbotRStat] Error: rx_data len = %d" % len(rx_data))
            self.__is_err = 1
            return

        k = (int)(len(rx_data) / 89) - 1
        k *= 89

        temp1 = struct.unpack("<HBBBIIBBH", rx_data[k:k + 17])
        self.axis = temp1[1]
        self.motion_status = temp1[2]
        self.motion_mode = temp1[3]
        self.mt_brake = temp1[4]
        self.mt_able = temp1[5]
        self.err_code = temp1[6]
        self.war_code = temp1[7]
        self.cmd_num = temp1[8]
        for i in range(self.axis):
            j1 = k + 17 + i * 4
            j2 = j1 + self.axis * 4
            j3 = j2 + self.axis * 4
            self.joint[i] = struct.unpack("<f", rx_data[j1:j1 + 4])
            self.pose[i] = struct.unpack("<f", rx_data[j2:j2 + 4])
            self.tau[i] = struct.unpack("<f", rx_data[j3:j3 + 4])
        self.__is_update = 1

    def is_update(self):
        """Query whether the automatically reported data has been updated

        Returns:
            bool: 1 already updated, 0 not updated yet
        """
        temp = self.__is_update
        self.__is_update = 0
        return temp

    def print_data(self):
        """Print the reported data currently obtained
        """
        print("rxcnt    = %d" % self.__rxcnt)
        print("axis     = %d" % self.axis)
        print("status   = %d" % self.motion_status)
        print("mode     = %d" % self.motion_mode)
        print("mt_brake = %s" % bin(self.mt_brake))
        print("mt_able  = %s" % bin(self.mt_able))
        print("err_code = %d" % self.err_code)
        print("war_code = %d" % self.war_code)
        print("cmd_num  = %d" % self.cmd_num)
        print_msg.nvect_03f("joint   = ", self.joint, self.axis)
        print_msg.nvect_03f("pose    = ", self.pose, 6)
        print_msg.nvect_03f("tau     = ", self.tau, self.axis)
        print("")
