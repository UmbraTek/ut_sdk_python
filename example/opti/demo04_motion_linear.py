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
    """This is a demo of movement in Tool space.
    run command:
        python3 example/opti/demo04_motion_linear.py --ip 192.168.1.xxx
    """
    parser = argparse.ArgumentParser()
    parser.description = 'OPTI demo'
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

    joint3 = [0, 0, 0, 0, 0, 0, 0]
    speed = 30 / 57.296
    acc = 3
    ret = ubot.moveto_joint_p2p(joint3, speed, acc, 0)

    pos1 = [200, 0, 700.0, 0.0, 0.0, 0]
    pos2 = [200, -460.0, 700.0, 0.0, 0.0, 0]
    pos3 = [300, 200.0, 600.0, 0.0, 0.0, 0]
    speed = 60.0
    acc = 200.0

    ret = ubot.moveto_cartesian_line(pos1, speed, acc, 0)
    print("moveto_cartesian_line   :%d" % (ret))
    ret = ubot.moveto_cartesian_line(pos2, speed, acc, 0)
    print("moveto_cartesian_line   :%d" % (ret))
    ret = ubot.moveto_cartesian_line(pos3, speed, acc, 0)
    print("moveto_cartesian_line   :%d" % (ret))
    ret = ubot.moveto_cartesian_line(pos1, speed, acc, 0)
    print("moveto_cartesian_line   :%d" % (ret))
