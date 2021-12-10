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
    """This is a demo of servo motion in joint space
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

    joint1 = [1.248, 1.416, 1.155, -0.252, -1.248, -0.003]
    joint2 = [0.990, 1.363, 1.061, -0.291, -0.990, -0.006]
    joint3 = [1.169, 1.022, 1.070, 0.058, -1.169, -0.004]
    time = [2, 2, 2]
    joint = [joint1, joint2, joint3]

    ret = ubot.moveto_servo_joint(3, joint, time)
    print("moveto_servo_joint   :%d" % (ret))
