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
    """This is a demo to get ubot parameters, status and other information
    """
    parser = argparse.ArgumentParser()
    parser.description = 'ubot demo'
    parser.add_argument("--ip", help=" ", default="127.0.0.1", type=str)
    args = parser.parse_args()

    ubot = UtraApiTcp(args.ip)

    ret, uuid = ubot.get_uuid()
    print("get_uuid      : %d, uuid = %s" % (ret, uuid))
    ret, version = ubot.get_sw_version()
    print("get_sw_version: %d, version = %10s %10s" % (ret, version[0:10], version[10:20]))
    ret, version = ubot.get_hw_version()
    print("get_hw_version: %d, version = %10s %10s" % (ret, version[0:10], version[10:20]))
    ret, axis = ubot.get_axis()
    print("get_axis      : %d, axis = %d" % (ret, axis))
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
    print("get_tcp_jerk    : %d, value = %d" % (ret, value))
    ret, value = ubot.get_tcp_maxacc()
    print("get_tcp_maxacc  : %d, value = %d" % (ret, value))
    ret, value = ubot.get_joint_jerk()
    print("get_joint_jerk  : %d, value = %d" % (ret, value))
    ret, value = ubot.get_joint_maxacc()
    print("get_joint_maxacc: %d, value = %d" % (ret, value))
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
    print_msg.nvect_03f("get_tcp_target_pos    : ", value, 6)
    ret, value = ubot.get_joint_target_pos()
    print_msg.nvect_03f("get_joint_target_pos   : ", value, axis)
