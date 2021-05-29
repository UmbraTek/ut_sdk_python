# Copyright 2020 The UmbraTek Inc. All Rights Reserved.
#
# Software License Agreement (BSD License)
#
# Author: Jimy Zhang <jimy.zhang@umbratek.com> <jimy92@163.com>
# =============================================================================

import time
import sys
import argparse

sys.path.append("./api/")
sys.path.append("../api/")
sys.path.append("./modules_lib/")
sys.path.append("../modules_lib/")
from ubot.ubot_report_debug import UbotReportDebug800HZ


class ReportDebugFun:
    def __init__(self):
        self.fo = 0

    def irq_run(self, ubot):
        if self.fo == 0:
            name = "data/report_debug_" + str(ubot.axis) + "axis.txt"
            self.fo = open(name, encoding='utf-8', mode='w+')

        data = ' '
        for i in range(ubot.axis):
            data += str(round(ubot.pos_target[i], 5)) + ' '
        for i in range(ubot.axis):
            data += str(round(ubot.pos_curr[i], 5)) + ' '
        for i in range(ubot.axis):
            data += str(round(ubot.vel_target[i], 5)) + ' '
        for i in range(ubot.axis):
            data += str(round(ubot.vel_curr[i], 5)) + ' '
        for i in range(ubot.axis):
            data += str(round(ubot.tau_target[i], 5)) + ' '
        for i in range(ubot.axis):
            data += str(round(ubot.tau_curr[i], 5)) + ' '

        for i in range(ubot.axis):
            data += str(round(ubot.q_filter[i], 5)) + ' '
        for i in range(ubot.axis):
            data += str(round(ubot.dq_filter[i], 5)) + ' '
        for i in range(ubot.axis):
            data += str(round(ubot.ddq_filter[i], 5)) + ' '
        for i in range(ubot.axis):
            data += str(round(ubot.tau_filter[i], 5)) + ' '

        for i in range(ubot.axis):
            data += str(round(ubot.tau_gra[i], 5)) + ' '
        for i in range(ubot.axis):
            data += str(round(ubot.tau_fri[i], 5)) + ' '
        for i in range(ubot.axis):
            data += str(round(ubot.tau_teach[i], 5)) + ' '
        for i in range(ubot.axis):
            data += str(round(ubot.tau_forward[i], 5)) + ' '
        for i in range(ubot.axis):
            data += str(round(ubot.collision[i], 5)) + ' '

        data += str(ubot.cnt) + ' '
        data += "\n"

        # print("%s" % data)
        self.fo.write(data)
        self.fo.flush()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.description = 'ubot report test'
    parser.add_argument("--ip", help=" ", default="127.0.0.1", type=str)
    args = parser.parse_args()

    report_fun = ReportDebugFun()
    ubot = UbotReportDebug800HZ(args.ip, report_fun)

    while 1:
        time.sleep(0.00001)
