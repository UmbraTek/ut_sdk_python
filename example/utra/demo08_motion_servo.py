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
    u"""This is a demo of servo motion in joint space
    run command:
        python3 example/utra/demo08_motion_servo.py --ip 192.168.1.xxx
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
    ret = ubot.moveto_home_p2p(speed, acc, 60)

    joint1 = [20 / 57.296, -30 / 57.296, 50 / 57.296, -10 / 57.296, 90 / 57.296, 40 / 57.296]
    joint2 = [20 / 57.296, -10 / 57.296, 100 / 57.296, 20 / 57.296, 90 / 57.296, -20 / 57.296]
    joint3 = [-20 / 57.296, -10 / 57.296, 100 / 57.296, 20 / 57.296, 90 / 57.296, -20 / 57.296]
    time = [20, 20, 20]
    joint = [joint1, joint2, joint3]

    ret = ubot.plan_sleep(5)
    ret = ubot.moveto_joint_servo(3, joint, time)
    print("moveto_joint_servo   :%d" % (ret))

    pos1 = [418, 56, 186, 3.14, 0.0, 1.5]
    pos2 = [418, -256, 186, 3.14, 0.0, 1.5]
    pos3 = [418, -256, 486, 3.14, 0.0, 1.5]
    time = [20, 20, 20]
    pose = [pos1, pos2, pos3]

    ret = ubot.plan_sleep(5)
    ret = ubot.moveto_cartesian_servo(3, pose, time)
    print("moveto_cartesian_servo   :%d" % (ret))
    ret = ubot.moveto_cartesian_servo(3, pose, time)
    print("moveto_cartesian_servo   :%d" % (ret))
    ret = ubot.moveto_cartesian_servo(3, pose, time)
    print("moveto_cartesian_servo   :%d" % (ret))
