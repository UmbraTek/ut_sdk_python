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
import time

sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))
from utapi.utra.utra_api_tcp import UtraApiTcp
from utapi.utra.utra_flxiv_api import UtraFlxiVApi

if __name__ == '__main__':
    u"""This is a demo of controlling a FLXI V on robot. 
    The command to control the FLXI V takes effect immediately whether the robot is moving or not.
    run command:
        python3 example/utra/demo22_flxie2_motion_now.py --ip 192.168.1.xxx
    """
    parser = argparse.ArgumentParser()
    parser.description = 'UTRA demo'
    parser.add_argument("--ip", help=" ", default="127.0.0.1", type=str)
    args = parser.parse_args()

    ubot = UtraApiTcp(args.ip)
    fixiv = UtraFlxiVApi(ubot, 102)

    ret = fixiv.set_motion_mode(1)
    print("set_motion_mode: %d" % (ret))
    ret = fixiv.set_motion_enable(1)
    print("set_motion_enable: %d" % (ret))

    time.sleep(3)

    ret = fixiv.set_motion_enable(0)
    print("set_motion_enable: %d" % (ret))
    ret = fixiv.set_motion_mode(0)
    print("set_motion_mode: %d" % (ret))
