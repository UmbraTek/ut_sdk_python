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
    u"""This is a demo of movement in joint space.
    run command:
        python3 example/utra/demo09_motion_p2pb.py --ip 192.168.1.xxx
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
    joint = [0, 0, 0, 0, 0, 0]
    ret = ubot.moveto_joint_p2p(joint, speed, acc, 0)

    speed = 10 / 57.296
    acc = 3
    joint1 = [20 / 57.296, -30 / 57.296, 50 / 57.296, -10 / 57.296, 90 / 57.296, 40 / 57.296]
    joint2 = [20 / 57.296, -10 / 57.296, 100 / 57.296, 20 / 57.296, 90 / 57.296, -20 / 57.296]
    joint3 = [-20 / 57.296, -10 / 57.296, 100 / 57.296, 20 / 57.296, 90 / 57.296, -20 / 57.296]
    ret = ubot.plan_sleep(2)  # This function must be called if the desired speed is continuous
    print("move_sleep    :%d" % (ret))
    ret = ubot.moveto_joint_p2pb(joint3, speed, acc, 0, 0)
    print("moveto_joint_p2pb   :%d" % (ret))
    ret = ubot.moveto_joint_p2pb(joint1, speed, acc, 0, 0)
    print("moveto_joint_p2pb   :%d" % (ret))
    ret = ubot.moveto_joint_p2pb(joint2, speed, acc, 0, 0)
    print("moveto_joint_p2pb   :%d" % (ret))
    ret = ubot.moveto_joint_p2pb(joint3, speed, acc, 0, 0)
    print("moveto_joint_p2pb   :%d" % (ret))
    ret = ubot.moveto_joint_p2pb(joint1, speed, acc, 0, 50)
    print("moveto_joint_p2pb   :%d" % (ret))
    ret = ubot.moveto_joint_p2pb(joint2, speed, acc, 0, 50)
    print("moveto_joint_p2pb   :%d" % (ret))
    ret = ubot.moveto_joint_p2pb(joint3, speed, acc, 0, 50)
    print("moveto_joint_p2pb   :%d" % (ret))
    ret = ubot.moveto_joint_p2pb(joint1, speed, acc, 0, 50)
    print("moveto_joint_p2pb   :%d" % (ret))
    ret = ubot.moveto_joint_p2pb(joint2, speed, acc, 0, 50)
    print("moveto_joint_p2pb   :%d" % (ret))
    ret = ubot.moveto_joint_p2pb(joint3, speed, acc, 0, 50)
    print("moveto_joint_p2pb   :%d" % (ret))
