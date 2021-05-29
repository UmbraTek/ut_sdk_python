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
    """This is a demo to get ubot parameters, status and other information
    """
    parser = argparse.ArgumentParser()
    parser.description = 'ubot demo'
    parser.add_argument("--ip", help=" ", default="127.0.0.1", type=str)
    args = parser.parse_args()

    ubotapi = UbotApiTcp(args.ip)

    ret, uuid = ubotapi.get_uuid()
    uuid_new = [chr(x) for x in uuid]
    print("get_uuid      : %d, uuid = %s" % (ret, "".join(uuid_new)))
    ret, version = ubotapi.get_sw_version()
    version = "".join([chr(x) for x in version])
    print("get_sw_version: %d, version = %10s %10s" % (ret, version[0:10], version[10:20]))
    ret, version = ubotapi.get_hw_version()
    version = "".join([chr(x) for x in version])
    print("get_hw_version: %d, version = %10s %10s" % (ret, version[0:10], version[10:20]))
    ret, axis = ubotapi.get_axis()
    print("get_axis      : %d, axis = %d" % (ret, axis))
    print("")

    ret, mode = ubotapi.get_motion_mode()
    print("get_motion_mode  : %d, mode = %d" % (ret, mode))
    ret, value = ubotapi.get_motion_enable()
    print("get_motion_enable: %d, value = %d" % (ret, value))
    ret, value = ubotapi.get_brake_enable()
    print("get_brake_enable : %d, value = %d" % (ret, value))
    ret, value = ubotapi.get_error_code()
    print("get_error_code   : %d, value = %d %d" % (ret, value[0], value[1]))
    ret, value = ubotapi.get_servo_msg()
    value_new = [str(x) for x in value]
    value_new = " ".join(value_new)
    print("get_servo_msg    : %d, value = %s" % (ret, value_new))
    ret, value = ubotapi.get_motion_status()
    print("get_motion_status: %d, value = %d" % (ret, value))
    ret, value = ubotapi.get_cmd_num()
    print("get_cmd_num      : %d, value = %d" % (ret, value))
    print("")

    ret, value = ubotapi.get_tcp_jerk()
    print("get_tcp_jerk    : %d, value = %d" % (ret, value))
    ret, value = ubotapi.get_tcp_maxacc()
    print("get_tcp_maxacc  : %d, value = %d" % (ret, value))
    ret, value = ubotapi.get_joint_jerk()
    print("get_joint_jerk  : %d, value = %d" % (ret, value))
    ret, value = ubotapi.get_joint_maxacc()
    print("get_joint_maxacc: %d, value = %d" % (ret, value))
    ret, value = ubotapi.get_tcp_offset()
    print_msg.nvect_03f("get_tcp_offset  : ", value, 6)
    ret, value = ubotapi.get_tcp_load()
    print_msg.nvect_03f("get_tcp_load    : ", value, 4)
    ret, value = ubotapi.get_gravity_dir()
    print_msg.nvect_03f("get_gravity_dir : ", value, 3)
    ret, value = ubotapi.get_collis_sens()
    print("get_collis_sens : %d, value = %d" % (ret, value))
    ret, value = ubotapi.get_teach_sens()
    print("get_teach_sens  : %d, value = %d" % (ret, value))
    ret, value = ubotapi.get_tcp_target_pos()
    print_msg.nvect_03f("get_tcp_target_pos    : ", value, 6)
    ret, value = ubotapi.get_joint_target_pos()
    print_msg.nvect_03f("get_joint_target_pos   : ", value, axis)
