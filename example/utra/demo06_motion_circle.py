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
    u"""This is a demo of circular motion in tool space.
    run command:
        python3 example/utra/demo06_motion_circle.py --ip 192.168.1.xxx
    """
    parser = argparse.ArgumentParser()
    parser.description = 'UTRA demo'
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

    speed = 30 / 57.296
    acc = 3
    ret = ubot.moveto_home_p2p(speed, acc, 0)

    joint1 = [0 / 57.296, -30 / 57.296, 50 / 57.296, -10 / 57.296, 90 / 57.296, 0 / 57.296]
    ret = ubot.moveto_joint_p2p(joint1, speed, acc, 0)
    print("moveto_joint_p2p   :%d" % (ret))

    speed = 50.0
    acc = 100.0
    pos1 = [418, 56, 186, 3.14, 0.0, 1.5]
    pos2 = [418, -256, 186, 3.14, 0.0, 1.5]
    pos3 = [418, -256, 486, 3.14, 0.0, 1.5]
    ret = ubot.moveto_cartesian_line(pos3, speed, acc, 0)
    print("moveto_cartesian_line   :%d" % (ret))
    ret = ubot.moveto_cartesian_circle(pos1, pos2, speed, acc, 0, 50)
    print("moveto_cartesian_circle   :%d" % (ret))
    ret = ubot.moveto_cartesian_circle(pos2, pos3, speed, acc, 0, 90)
    print("moveto_cartesian_circle   :%d" % (ret))
    ret = ubot.moveto_cartesian_circle(pos2, pos3, speed, acc, 0, 130)
    print("moveto_cartesian_circle   :%d" % (ret))

    joint1 = [170.5 / 57.296, 3.5 / 57.296, -125.6 / 57.296, -39.1 / 57.296, -90 / 57.296, -9.5 / 57.296]
    joint2 = [133.8 / 57.296, 13.1 / 57.296, -114.3 / 57.296, -37.3 / 57.296, -90 / 57.296, -46.2 / 57.296]
    joint3 = [133.8 / 57.296, 3 / 57.296, -75.9 / 57.296, 11.1 / 57.296, -90 / 57.296, -46.2 / 57.296]
    # ret = ubot.plan_sleep(5)
    ret = ubot.moveto_joint_line(joint3, speed, acc, 5.0)
    print("moveto_joint_line   :%d" % (ret))
    ret = ubot.moveto_joint_circle(joint1, joint2, speed, acc, 0, 50)
    print("moveto_joint_circle   :%d" % (ret))
    ret = ubot.moveto_joint_circle(joint2, joint3, speed, acc, 0, 100)
    print("moveto_joint_circle   :%d" % (ret))
    ret = ubot.moveto_joint_circle(joint2, joint3, speed, acc, 0, 130)
    print("moveto_joint_circle   :%d" % (ret))
