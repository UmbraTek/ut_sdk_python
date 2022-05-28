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
from utapi.utra.utra_flxie_api import UtraFlxiE2Api

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.description = 'UTRA demo'
    parser.add_argument("--ip", help=" ", default="127.0.0.1", type=str)
    args = parser.parse_args()

    ubot = UtraApiTcp(args.ip)
    fixi = UtraFlxiE2Api(ubot, 101)

    ret = fixi.set_motion_mode(1)
    print("set_motion_mode: %d" % (ret))
    ret = fixi.set_motion_enable(1)
    print("set_motion_enable: %d" % (ret))

    ret = fixi.set_pos_target(0)
    print("set_pos_target: %d" % (ret))
    time.sleep(3)
    ret = fixi.set_pos_target(20)
    print("set_pos_target: %d" % (ret))
