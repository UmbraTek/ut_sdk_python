# Copyright 2021 The UmbraTek Inc. All Rights Reserved.
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
    parser.description = 'ubot demo'
    parser.add_argument("--ip", help=" ", default="127.0.0.1", type=str)
    args = parser.parse_args()

    ubot = UtraApiTcp(args.ip)
    fixi = UtraFlxiE2Api(ubot, 101)

    ret = fixi.set_motion_mode(3)
    print("set_motion_mode: %d" % (ret))
    ret = fixi.set_motion_enable(1)
    print("set_motion_enable: %d" % (ret))
    ret = fixi.set_tau_target(-0.5)
    print("set_tau_target: %d" % (ret))
