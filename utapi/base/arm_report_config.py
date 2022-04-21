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


class ArmReportConfig(threading.Thread):
    def __init__(self, ip, port=30003):

        self.__is_err = 0
        self.__rxcnt = 0
        self.__is_update = 0

        self.trs_maxacc = 0
        self.trs_jerk = 0
        self.rot_maxacc = 0
        self.rot_jerk = 0
        self.p2p_maxacc = 0
        self.p2p_jerk = 0
        self.tcp_offset = [0] * 6
        self.tcp_load = [0] * 4
        self.gravity_dir = [0] * 3
        self.collis_sens = 0
        self.teach_sens = 0

        self.__socekt_fp = SocketTcp(ip, port, -1, 32)
        if self.__socekt_fp.is_error() != 0:
            print("[UbotRConf] Error: SocketTcp failed, ip: %s, port: %d" % (ip, port))
            return -1
        print("[UbotRConf] Tcp Report Status connection successful")

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

    def close(self):
        self.__is_err = 0

    def is_err(self):
        return self.__is_err

    def flush_data(self, rx_data):
        if len(rx_data) % 80 != 0:
            print("[UbotRConf] Error: rx_data len = %d" % len(rx_data))
            # self.__is_err = 1

        k = (int)(len(rx_data) / 80) - 1
        k *= 80

        temp1 = struct.unpack("<HfffffffffffffffffffBB", rx_data[k:k + 80])
        self.trs_maxacc = temp1[1]
        self.trs_jerk = temp1[2]
        self.rot_maxacc = temp1[3]
        self.rot_jerk = temp1[4]
        self.p2p_maxacc = temp1[5]
        self.p2p_jerk = temp1[6]
        self.tcp_offset = temp1[7:13]
        self.tcp_load = temp1[13:17]
        self.gravity_dir = temp1[17:20]
        self.collis_sens = temp1[20]
        self.teach_sens = temp1[21]
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
        print("rxcnt      = %d" % self.__rxcnt)
        print("trs_maxacc = %f" % self.trs_maxacc)
        print("trs_jerk   = %f" % self.trs_jerk)
        print("rot_maxacc = %f" % self.rot_maxacc)
        print("rot_jerk   = %f" % self.rot_jerk)
        print("p2p_maxacc = %f" % self.p2p_maxacc)
        print("p2p_jerk   = %f" % self.p2p_jerk)
        print("colli_sens = %d" % self.collis_sens)
        print("teach_sens = %d" % self.teach_sens)
        print_msg.nvect_03f("tcp_offset = ", self.tcp_offset, 6)
        print_msg.nvect_03f("tcp_load   = ", self.tcp_load, 4)
        print_msg.nvect_03f("gravity_dir= ", self.gravity_dir, 3)
        print("")
