#!/usr/bin/env python3
#
# Copyright (C) 2023 UmbraTek Inc. All Rights Reserved.
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


if __name__ == '__main__':
    u"""This is a demo of servo motion in joint space. And test to clear the cache instruction during motion.
    When multiple motion commands are sent to the controller, the commands enter the queue stack and run one by one.
    If you want to discard the commands cached in the queue,
    you can call the API interface to clear the current queue cache and then send new motion commands.
    run command:
        python3 example/utra/demo11_motion_realtime.py --ip 192.168.1.xxx
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
    print("moveto_home_p2p  :%d" % (ret))

    joint1 = [20 / 57.296, -30 / 57.296, 50 / 57.296, -10 / 57.296, 90 / 57.296, 40 / 57.296]
    joint2 = [20 / 57.296, -10 / 57.296, 100 / 57.296, 20 / 57.296, 90 / 57.296, -20 / 57.296]
    joint3 = [-20 / 57.296, -10 / 57.296, 100 / 57.296, 20 / 57.296, 90 / 57.296, -20 / 57.296]
    run_time = [20, 20, 20]
    joint = [joint1, joint2, joint3]

    # ret = ubot.plan_sleep(5)
    ret = ubot.moveto_joint_servo(3, joint, run_time)
    print("moveto_joint_servo   :%d" % (ret))
    ret = ubot.moveto_joint_servo(3, joint, run_time)
    print("moveto_joint_servo   :%d" % (ret))
    ret = ubot.moveto_joint_servo(3, joint, run_time)
    print("moveto_joint_servo   :%d" % (ret))

    time.sleep(2)
    ret = ubot.set_cmd_num()
    print("set_cmd_num  :%d" % (ret))

    ret = ubot.moveto_home_p2p(speed, acc, 0)
    print("moveto_home_p2p  :%d" % (ret))
