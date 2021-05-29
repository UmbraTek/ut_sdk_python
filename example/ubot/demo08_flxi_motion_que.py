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
    print("[Demo 08 ] get_motion_status :%d %d" % (ret, value))
    ret, value = ubotapi.get_error_code()
    print("[Demo 08 ] get_error_code    :%d %d %d" % (ret, value[0], value[1]))
    ret = ubotapi.reset_err()
    print("[Demo 08 ] reset_err    :%d" % (ret))
    ret = ubotapi.set_motion_enable(9, 1)
    print("[Demo 08 ] set_motion_enable :%d" % (ret))
    ret = ubotapi.set_motion_status(0)
    print("[Demo 08 ] set_motion_status :%d" % (ret))
    print(" ")

    fixiapi = UbotFlxiApi(ubotapi, 3)

    ret = ubotapi.move_sleep(1)
    print("[Demo 08 ] move_sleep :%d" % (ret))

    ret = fixiapi.set_motion_mode(1, False)
    print("[Demo 08 ]set_motion_mode: %d" % (ret))

    ret = fixiapi.set_motion_enable(1, False)
    print("[Demo 08 ]set_motion_enable: %d" % (ret))

    ret = fixiapi.set_pos_target(200, False)
    print("[Demo 08 ]set_pos_target: %d" % (ret))

    ret = ubotapi.move_sleep(5)
    print("[Demo 08 ] move_sleep :%d" % (ret))

    ret = fixiapi.set_pos_target(-200, False)
    print("[Demo 08 ]set_pos_target: %d" % (ret))

    ret = ubotapi.move_sleep(10)
    print("[Demo 08 ] move_sleep :%d" % (ret))

    ret = fixiapi.set_motion_mode(3, False)
    print("[Demo 08 ]set_motion_mode: %d" % (ret))

    ret = fixiapi.set_motion_enable(1, False)
    print("[Demo 08 ]set_motion_enable: %d" % (ret))

    ret = fixiapi.set_tau_target(0.5, False)
    print("[Demo 08 ]set_tau_target: %d" % (ret))
