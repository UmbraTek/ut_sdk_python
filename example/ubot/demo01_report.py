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
sys.path.append("./modules_lib/")
from ubot.ubot_report_status import UbotReportStatus100HZ
from ubot.ubot_report_status import UbotReportStatus10HZ
from ubot.ubot_report_config import UbotReportConfig
from ubot.ubot_report_debug import UbotReportDebug800HZ

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.description = 'ubot report test'
    parser.add_argument("--m", help="[1: status10hz] [2: status100hz] [3: config]", default=1, type=int)
    parser.add_argument("--ip", help=" ", default="127.0.0.1", type=str)
    args = parser.parse_args()

    if args.m == 1:
        ubot = UbotReportStatus10HZ(args.ip)
    elif args.m == 2:
        ubot = UbotReportStatus100HZ(args.ip)
    elif args.m == 3:
        ubot = UbotReportConfig(args.ip)
    elif args.m == 4:
        ubot = UbotReportDebug800HZ(args.ip)

    while 1:
        time.sleep(0.001)
        if ubot.is_update():
            ubot.print_data()
"""
python3 example/ubot/example_01_report.py --ip 192.168.1.175 --m 4
"""
