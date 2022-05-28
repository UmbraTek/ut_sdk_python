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
from utapi.utra.utra_flxie_api import UtraFlxiE2Api

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.description = 'UTRA demo'
    parser.add_argument("--ip", help=" ", default="127.0.0.1", type=str)
    args = parser.parse_args()

    ubot = UtraApiTcp(args.ip)
    fixi = UtraFlxiE2Api(ubot, 101)

    ret = ubot.reset_err()  # Reset error
    print("reset_error   :%d" % (ret))
    ret = ubot.set_motion_mode(0)  # Set the operating mode of the arm, 0: position control mode
    print("set_motion_mode   :%d" % (ret))
    ret = ubot.set_motion_enable(8, 1)  # Set the enable state of the arm
    print("set_motion_enable :%d" % (ret))
    ret = ubot.set_motion_status(0)  # Set the running status of the arm, 0: Set to ready
    print("set_motion_status :%d" % (ret))

    ret = ubot.move_sleep(1)
    print("move_sleep :%d" % (ret))
    ret = fixi.set_motion_mode(1, False)
    print("set_motion_mode: %d" % (ret))
    ret = fixi.set_motion_enable(1, False)
    print("set_motion_enable: %d" % (ret))

    ret = fixi.set_pos_target(0, False)
    print("set_pos_target: %d" % (ret))
    ret = ubot.move_sleep(5)
    print("move_sleep :%d" % (ret))

    ret = fixi.set_pos_target(20, False)
    print("set_pos_target: %d" % (ret))
    ret = ubot.move_sleep(10)
    print("move_sleep :%d" % (ret))

    ret = fixi.set_pos_target(0, False)
    print("set_pos_target: %d" % (ret))
