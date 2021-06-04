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
from common import print_msg

if __name__ == '__main__':
    """This is a demo of circular motion in tool space
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

    speed = 0.1
    acc = 3
    ret = ubot.moveto_home_p2p(speed, acc, 60)

    pos1 = [-0.0, -360.0, 800.0, 1.58, 0.0, 0.0]
    pos2 = [-8.0, -560.0, 600.0, 1.58, 0.0, 0.0]
    pos3 = [-180.0, -560.0, 600.0, 1.58, 0.0, 0.0]
    speed = 50.0
    acc = 100.0

    ret = ubot.moveto_cartesian_line(pos3, speed, acc, 5.0)
    print("moveto_cartesian_line   :%d" % (ret))

    ret = ubot.moveto_cartesian_circle(pos1, pos2, speed, acc, 5, 50)
    print("moveto_cartesian_circle   :%d" % (ret))
    ret = ubot.moveto_cartesian_circle(pos2, pos3, speed, acc, 5, 100)
    print("moveto_cartesian_circle   :%d" % (ret))
    ret = ubot.moveto_cartesian_circle(pos2, pos1, speed, acc, 5, 125)
    print("moveto_cartesian_circle   :%d" % (ret))
