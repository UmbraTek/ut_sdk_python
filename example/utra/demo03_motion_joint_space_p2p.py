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
    """This is a demo of movement in joint space.
    """
    parser = argparse.ArgumentParser()
    parser.description = 'ubot demo'
    parser.add_argument("--ip", help=" ", default="127.0.0.1", type=str)
    args = parser.parse_args()

    ubot = UtraApiTcp(args.ip)

    ret = ubot.reset_err()  # Reset error
    print("reset_error   :%d" % (ret))
    ret = ubot.set_motion_mode(0)  # Set the operating mode of the arm, 0: position control mode
    print("set_motion_mode   :%d" % (ret))
    ret = ubot.set_motion_enable(8, 1)  # Set the enable state of the arm
    print("set_motion_enable :%d" % (ret))
    ret = ubot.set_motion_status(0)  # Set the running status of the arm, 0: Set to ready
    print("set_motion_status :%d" % (ret))

    joint = [0, 0, 0, 0, 0, 0]
    speed = 30 / 57.296
    acc = 3
    ret = ubot.moveto_joint_p2p(joint, speed, acc, 60)

    joint1 = [20 / 57.296, -30 / 57.296, 50 / 57.296, -10 / 57.296, 90 / 57.296, 40 / 57.296]
    joint2 = [20 / 57.296, -10 / 57.296, 100 / 57.296, 20 / 57.296, 90 / 57.296, -20 / 57.296]
    joint3 = [-20 / 57.296, -10 / 57.296, 100 / 57.296, 20 / 57.296, 90 / 57.296, -20 / 57.296]
    speed = 30 / 57.296
    acc = 3
    ret = ubot.moveto_joint_p2p(joint3, speed, acc, 60)
    print("moveto_joint_p2p   :%d" % (ret))
    ret = ubot.moveto_joint_p2p(joint1, speed, acc, 60)
    print("moveto_joint_p2p   :%d" % (ret))
    ret = ubot.moveto_joint_p2p(joint2, speed, acc, 60)
    print("moveto_joint_p2p   :%d" % (ret))
    ret = ubot.moveto_joint_p2p(joint3, speed, acc, 60)
    print("moveto_joint_p2p   :%d" % (ret))
