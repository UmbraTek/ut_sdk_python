#!/usr/bin/env python3
#
# Copyright (C) 2021 UmbraTek Inc. All Rights Reserved.
#
# Software License Agreement (BSD License)
#
# Author: Jimy Zhang <jimy.zhang@umbratek.com> <jimy92@163.com>
# =============================================================================
import sys
import argparse
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))
from utapi.utra.utra_api_tcp import UtraApiTcp
from utapi.utra.utra_flxiv_api import UtraFlxiVApi

if __name__ == '__main__':
    u"""This is a demo to get the parameters, status and other information of FLXI V on the robot.
    run command:
        python3 example/utra/demo24_flxiv_get_param.py --ip 192.168.1.xxx
    """
    parser = argparse.ArgumentParser()
    parser.description = 'UTRA demo'
    parser.add_argument("--ip", help=" ", default="127.0.0.1", type=str)
    args = parser.parse_args()

    ubot = UtraApiTcp(args.ip)
    fixiv = UtraFlxiVApi(ubot, 102)

    ret1, uuid = fixiv.get_uuid()
    print("get_uuid: %d, uuid = %s" % (ret1, uuid))
    ret1, version = fixiv.get_sw_version()
    print("get_sw_version: %d, version = %s" % (ret1, version))
    ret1, version = fixiv.get_hw_version()
    print("get_hw_version: %d, version = %s" % (ret1, version))
    print(" ")

    ret1, value = fixiv.get_temp_limit()
    print("get_temp_limit: %d, value = %d %d" % (ret1, value[0], value[1]))
    ret1, value = fixiv.get_volt_limit()
    print("get_volt_limit: %d, value = %d %d" % (ret1, value[0], value[1]))
    print(" ")

    ret, value = fixiv.get_motion_mode()
    print("get_motion_mode  : %d, value = %d" % (ret, value))
    ret, value = fixiv.get_motion_enable()
    print("get_motion_enable: %d, value = %d" % (ret, value))
    ret, value = fixiv.get_temp_driver()
    print("get_temp_driver  : %d, value = %.1f" % (ret, value))
    ret, value = fixiv.get_temp_motor()
    print("get_temp_motor   : %d, value = %.1f" % (ret, value))
    ret, value = fixiv.get_bus_volt()
    print("get_bus_volt     : %d, value = %.1f" % (ret, value))
    ret, value = fixiv.get_error_code()
    print("get_error_code   : %d, value = %d" % (ret, value))
    print(" ")

    ret, value = fixiv.get_senser()
    print("get_senser: %d, value = %f %f %f %f" % (ret, value[0], value[1], value[2], value[3]))
    print(" ")
