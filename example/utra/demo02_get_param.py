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
from utapi.common import print_msg

if __name__ == '__main__':
    u"""This is a demo to get ubot parameters, status and other information
    run command:
        python3 example/utra/demo02_get_param.py --ip 192.168.1.xxx
    """
    parser = argparse.ArgumentParser()
    parser.description = 'UTRA demo'
    parser.add_argument("--ip", help=" ", default="127.0.0.1", type=str)
    args = parser.parse_args()

    ubot = UtraApiTcp(args.ip)

    ret, uuid = ubot.get_uuid()
    print("get_uuid       : %d, uuid    = %s" % (ret, uuid))
    ret, version = ubot.get_sw_version()
    print("get_sw_version : %d, version = %10s %10s" % (ret, version[0:10], version[10:20]))
    ret, version = ubot.get_hw_version()
    print("get_hw_version : %d, version = %10s %10s" % (ret, version[0:10], version[10:20]))
    ret, axis = ubot.get_axis()
    print("get_axis       : %d, axis    = %d" % (ret, axis))
    ret, autorun = ubot.get_sys_autorun()
    print("get_sys_autorun: %d, autorun = %d" % (ret, autorun))
    print("")

    ret, mode = ubot.get_motion_mode()
    print("get_motion_mode  : %d, mode = %d" % (ret, mode))
    ret, value = ubot.get_motion_enable()
    print("get_motion_enable: %d, value = %d" % (ret, value))
    ret, value = ubot.get_brake_enable()
    print("get_brake_enable : %d, value = %d" % (ret, value))
    ret, value = ubot.get_error_code()
    print("get_error_code   : %d, value = %d %d" % (ret, value[0], value[1]))
    ret, value = ubot.get_servo_msg()
    print("get_servo_msg    : %d, value = %s" % (ret, value))
    ret, value = ubot.get_motion_status()
    print("get_motion_status: %d, value = %d" % (ret, value))
    ret, value = ubot.get_cmd_num()
    print("get_cmd_num      : %d, value = %d" % (ret, value))
    print("")

    ret, value = ubot.get_tcp_jerk()
    print("get_tcp_jerk    : %d, value = %f" % (ret, value))
    ret, value = ubot.get_tcp_maxacc()
    print("get_tcp_maxacc  : %d, value = %f" % (ret, value))
    ret, value = ubot.get_joint_jerk()
    print("get_joint_jerk  : %d, value = %f" % (ret, value))
    ret, value = ubot.get_joint_maxacc()
    print("get_joint_maxacc: %d, value = %f" % (ret, value))
    ret, value = ubot.get_tcp_offset()
    print_msg.nvect_03f("get_tcp_offset  : ", value, 6)
    ret, value = ubot.get_tcp_load()
    print_msg.nvect_03f("get_tcp_load    : ", value, 4)
    ret, value = ubot.get_gravity_dir()
    print_msg.nvect_03f("get_gravity_dir : ", value, 3)
    ret, value = ubot.get_collis_sens()
    print("get_collis_sens : %d, value = %d" % (ret, value))
    ret, value = ubot.get_teach_sens()
    print("get_teach_sens  : %d, value = %d" % (ret, value))
    ret, value = ubot.get_tcp_target_pos()
    print_msg.nvect_03f("get_tcp_target_pos   : ", value, 6)
    ret, value = ubot.get_joint_target_pos()
    print_msg.nvect_03f("get_joint_target_pos : ", value, axis)
    ret, value = ubot.get_joint_target_vel()
    print_msg.nvect_03f("get_joint_target_vel : ", value, axis)

    pos = [300, -300, 400, 3.14 * 0.5, 0, 3.14 * 0.5]
    joint = [1.8988, 0.1065, -1.9738, -2.0803, -0.3281, 0]

    ret, joints = ubot.get_ik(pos, joint)
    print("get_ik: %d, " % (ret), end="")
    print_msg.nvect_03f(" ", joints, axis)
    ret, pos = ubot.get_fk(joint)
    print("get_fk: %d, " % (ret), end="")
    print_msg.nvect_03f(" ", pos, 6)

    ret, limit = ubot.is_joint_limit(joint)
    print("is_joint_limit : %d, limit = %d " % (ret, limit))
    ret, limit = ubot.is_tcp_limit(pos)
    print("is_tcp_limit   : %d, limit = %d " % (ret, limit))
