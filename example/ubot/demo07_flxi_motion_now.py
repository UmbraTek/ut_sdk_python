# Copyright 2021 The UmbraTek Inc. All Rights Reserved.
#
# Software License Agreement (BSD License)
#
# Author: Jimy Zhang <jimy.zhang@umbratek.com> <jimy92@163.com>
# =============================================================================
import sys
import argparse

sys.path.append("./api/")
sys.path.append("../api/")
sys.path.append("./modules_lib/")
sys.path.append("../modules_lib/")
from ubot.ubot_api_tcp import UbotApiTcp
from ubot.ubot_flxi_api import UbotFlxiApi
from common import print_msg
from common import hex_data

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.description = 'ubot demo'
    parser.add_argument("--ip", help=" ", default="127.0.0.1", type=str)
    args = parser.parse_args()

    ubotapi = UbotApiTcp(args.ip)
    ret, value = ubotapi.get_motion_status()
    print("[Demo 07 ] get_motion_status :%d %d" % (ret, value))
    ret, value = ubotapi.get_error_code()
    print("[Demo 07 ] get_error_code    :%d %d %d" % (ret, value[0], value[1]))
    ret = ubotapi.reset_err()
    print("[Demo 07 ] reset_err    :%d" % (ret))
    ret = ubotapi.set_motion_enable(9, 1)
    print("[Demo 07 ] set_motion_enable :%d" % (ret))
    ret = ubotapi.set_motion_status(0)
    print("[Demo 07 ] set_motion_status :%d" % (ret))
    print(" ")

    fixiapi = UbotFlxiApi(ubotapi, 3)
    # ret = fixiapi.restart_driver()
    # print("[Demo 07 ]restart_driver: %d" % (ret))

    ret = fixiapi.set_temp_limit(-12, 65)
    print("[Demo 07 ]set_temp_limit: %d" % (ret))

    ret = fixiapi.set_volt_limit(21, 53)
    print("[Demo 07 ]set_volt_limit: %d" % (ret))

    ret = fixiapi.set_curr_limit(3.3)
    print("[Demo 07 ]set_curr_limit: %d" % (ret))

    ret = fixiapi.set_motion_mode(3)
    print("[Demo 07 ]set_motion_mode: %d" % (ret))

    ret = fixiapi.set_motion_enable(1)
    print("[Demo 07 ]set_motion_enable: %d" % (ret))

    ret = fixiapi.set_pos_pidp(790000)
    print("[Demo 07 ]set_pos_pidp: %d" % (ret))

    ret = fixiapi.set_tau_target(-0.5)
    print("[Demo 07 ]set_tau_target: %d" % (ret))
