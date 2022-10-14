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


if __name__ == '__main__':
    """"This is a demo of movement in joint space.
    run command:
        python3 example/opti/demo03_motion_p2p.py --ip 192.168.1.xxx
    """
    parser = argparse.ArgumentParser()
    parser.description = 'OPTI demo'
    parser.add_argument("--ip", help=" ", default="127.0.0.1", type=str)
    args = parser.parse_args()

    ubot = UtraApiTcp(args.ip)

    ret, ver_hw = ubot.get_hw_version()  # Set the running status of the arm, 0: Set to ready
    print("get_hw_version :%d" % (ret))
    print(ver_hw)

    ret = ubot.reset_err()  # Reset error
    print("reset_error   :%d" % (ret))
    ret = ubot.set_motion_mode(0)  # Set the operating mode of the arm, 0: position control mode
    print("set_motion_mode   :%d" % (ret))
    ret = ubot.set_motion_enable(8, 1)  # Set the enable state of the arm
    print("set_motion_enable :%d" % (ret))
    ret = ubot.set_motion_status(0)  # Set the running status of the arm, 0: Set to ready
    print("set_motion_status :%d" % (ret))

    joint = [0, 0, 0, 0, 0, 0, 0]
    speed = 30 / 57.296
    acc = 3
    ret = ubot.moveto_joint_p2p(joint, speed, acc, 0)

    if "0001308001" in ver_hw:
        joint1 = [0, 56 / 57.296, 30 / 57.296, 126 / 57.296, 30 / 57.296, 70 / 57.296, 0]
        joint2 = [40 / 57.296, -62 / 57.296, -30 / 57.296, 56 / 57.296, 30 / 57.296, -62 / 57.296, 40 / 57.296]
        joint3 = [-30 / 57.296, -45 / 57.296, 0, 90 / 57.296, 0, -45 / 57.296, -30 / 57.296]
        print("0001308001")

    elif "0001408001" in ver_hw:
        joint1 = [10 / 57.296, 50 / 57.296, 110 / 57.296, 90 / 57.296, 0 / 57.296, 10 / 57.296]
        joint2 = [40 / 57.296, -62 / 57.296, 56 / 57.296, 0 / 57.296, -62 / 57.296, 40 / 57.296]
        joint3 = [-30 / 57.296, -45 / 57.296, 90 / 57.296, 0, -45 / 57.296, -30 / 57.296]
        print("0001408001")

    speed = 30 / 57.296
    acc = 3
    ret = ubot.moveto_joint_p2p(joint3, speed, acc, 0)
    print("moveto_joint_p2p   :%d" % (ret))
    ret = ubot.moveto_joint_p2p(joint1, speed, acc, 0)
    print("moveto_joint_p2p   :%d" % (ret))
    ret = ubot.moveto_joint_p2p(joint2, speed, acc, 0)
    print("moveto_joint_p2p   :%d" % (ret))
    ret = ubot.moveto_joint_p2p(joint3, speed, acc, 0)
    print("moveto_joint_p2p   :%d" % (ret))
