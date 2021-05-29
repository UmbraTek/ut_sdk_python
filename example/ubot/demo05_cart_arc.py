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
    """This is a demo of circular motion in tool space
    """
    parser = argparse.ArgumentParser()
    parser.description = 'ubot demo'
    parser.add_argument("--ip", help=" ", default="127.0.0.1", type=str)
    args = parser.parse_args()

    ubotapi = UbotApiTcp(args.ip)
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
    speed = 50.0
    acc = 100.0

    ret = ubotapi.moveto_cartesian_line(pos1, speed, acc, 5.0)
    print("moveto_cartesian_line   :%d" % (ret))
    ret = ubotapi.moveto_cartesian_line(pos2, speed, acc, 5.0)
    print("moveto_cartesian_line   :%d" % (ret))
    ret = ubotapi.moveto_cartesian_line(pos3, speed, acc, 5.0)
    print("moveto_cartesian_line   :%d" % (ret))

    ret = ubotapi.moveto_cartesian_circle(pos1, pos2, speed, acc, 5, 50)
    print("moveto_cartesian_circle   :%d" % (ret))

    ret = ubotapi.moveto_cartesian_circle(pos2, pos3, speed, acc, 5, 100)
    print("moveto_cartesian_circle   :%d" % (ret))

    ret = ubotapi.moveto_cartesian_circle(pos2, pos1, speed, acc, 5, 100)
    print("moveto_cartesian_circle   :%d" % (ret))
