# Copyright 2021 The UmbraTek Inc. All Rights Reserved.
#
# Software License Agreement (BSD License)
#
# Author: Jimy Zhang <jimy.zhang@umbratek.com> <jimy92@163.com>
# =============================================================================
import sys
import argparse

sys.path.append("./api/")
sys.path.append("./modules_lib/")
from ubot.ubot_api_tcp import UbotApiTcp
from common import print_msg

if __name__ == '__main__':
    """This is a demo of movement in joint space/ Tool space 
    """
    parser = argparse.ArgumentParser()
    parser.description = 'ubot demo'
    parser.add_argument("--ip", help=" ", default="127.0.0.1", type=str)
    args = parser.parse_args()

    ubotapi = UbotApiTcp(args.ip)

    ret = ubotapi.reset_err()
    print("reset_error   :%d" % (ret))
    ret = ubotapi.set_motion_mode(1)
    print("set_motion_mode   :%d" % (ret))
    ret = ubotapi.set_motion_enable(8, 1)
    print("set_motion_enable :%d" % (ret))
    ret = ubotapi.set_motion_status(0)
    print("set_motion_status :%d" % (ret))
    ret, value = ubotapi.get_motion_status()
    print("get_motion_status :%d %d" % (ret, value))
    ret, value = ubotapi.get_error_code()
    print("get_error_code    :%d %d %d" % (ret, value[0], value[1]))

    ret, value = ubotapi.get_tcp_pose()
    print_msg.nvect_03f("[Demo 03 ] get_tcp_pose      : ", value, 6)

    joint3 = [0, 0, 0, 0, 0, 0]
    speed = 0.1
    acc = 3
    ret = ubotapi.moveto_joint_p2p(joint3, speed, acc, 60)

    pos1 = [-0.0, -360.0, 800.0, 1.58, 0.0, 0.0]
    pos2 = [-8.0, -560.0, 600.0, 1.58, 0.0, 0.0]
    pos3 = [-180.0, -560.0, 600.0, 1.58, 0.0, 0.0]
    speed = 20.0
    acc = 10000.0

    ret = ubotapi.moveto_cartesian_line(pos1, speed, acc, 5.0)
    print("moveto_cartesian_line   :%d" % (ret))
    ret = ubotapi.moveto_cartesian_line(pos2, speed, acc, 5.0)
    print("moveto_cartesian_line   :%d" % (ret))
    ret = ubotapi.moveto_cartesian_line(pos3, speed, acc, 5.0)
    print("moveto_cartesian_line   :%d" % (ret))

    ret = ubotapi.move_sleep(1)
    print("move_sleep    :%d" % (ret))
    ret = ubotapi.moveto_cartesian_lineb(pos1, speed, acc, 5.0, 80)
    print("moveto_cartesian_lineb   :%d" % (ret))
    ret = ubotapi.moveto_cartesian_lineb(pos2, speed, acc, 5.0, 60)
    print("moveto_cartesian_lineb   :%d" % (ret))
    ret = ubotapi.moveto_cartesian_lineb(pos3, speed, acc, 5.0, 30)
    print("moveto_cartesian_lineb   :%d" % (ret))
    ret = ubotapi.moveto_cartesian_lineb(pos1, speed, acc, 5.0, 80)
    print("moveto_cartesian_lineb   :%d" % (ret))
    ret = ubotapi.moveto_cartesian_lineb(pos2, speed, acc, 5.0, 60)
    print("moveto_cartesian_lineb   :%d" % (ret))
    ret = ubotapi.moveto_cartesian_lineb(pos3, speed, acc, 5.0, 30)
    print("moveto_cartesian_lineb   :%d" % (ret))

    joint1 = [1.248, 1.416, 1.155, -0.252, -1.248, -0.003]
    joint2 = [0.990, 1.363, 1.061, -0.291, -0.990, -0.006]
    joint3 = [1.169, 1.022, 1.070, 0.058, -1.169, -0.004]
    speed = 0.02
    acc = 3
    ret = ubotapi.moveto_joint_p2p(joint3, speed, acc, 60)
    print("moveto_joint_p2p   :%d" % (ret))
    ret = ubotapi.moveto_joint_p2p(joint1, speed, acc, 60)
    print("moveto_joint_p2p   :%d" % (ret))
    ret = ubotapi.moveto_joint_p2p(joint2, speed, acc, 60)
    print("moveto_joint_p2p   :%d" % (ret))
    ret = ubotapi.moveto_joint_p2p(joint3, speed, acc, 60)
    print("moveto_joint_p2p   :%d" % (ret))
    ret = ubotapi.moveto_joint_p2p(joint1, speed, acc, 60)
    print("moveto_joint_p2p   :%d" % (ret))
    ret = ubotapi.moveto_joint_p2p(joint2, speed, acc, 60)
    print("moveto_joint_p2p   :%d" % (ret))

    joint3 = [0, 0, 0, 0, 0, 0]
    speed = 0.02
    acc = 3
    ret = ubotapi.moveto_joint_p2p(joint3, speed, acc, 60)
