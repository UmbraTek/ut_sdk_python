# Copyright 2021 The UmbraTek Inc. All Rights Reserved.
#
# Software License Agreement (BSD License)
#
# Author: Jimy Zhang <jimy.zhang@umbratek.com> <jimy92@163.com>
# =============================================================================
import sys
import argparse

sys.path.append("./api/")
sys.path.append("../api/")
sys.path.append("./modules_lib/")
sys.path.append("../modules_lib/")
from ubot.ubot_api_tcp import UbotApiTcp
from ubot.ubot_flxi_api import UbotFlxiApi
from common import print_msg
from common import hex_data

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.description = 'ubot demo'
    parser.add_argument("--ip", help=" ", default="127.0.0.1", type=str)
    args = parser.parse_args()

    ubotapi = UbotApiTcp(args.ip)
    ret, value = ubotapi.get_motion_status()
    print("[Demo 06 ] get_motion_status :%d %d" % (ret, value))
    ret, value = ubotapi.get_error_code()
    print("[Demo 06 ] get_error_code    :%d %d %d" % (ret, value[0], value[1]))
    print(" ")

    fixiapi = UbotFlxiApi(ubotapi, 3)
    ret1, uuid = fixiapi.get_uuid()
    print("[Demo 06 ]get_uuid: %d, uuid = " % (ret1))
    print_msg.nhex("    ", uuid, 12)
    ret1, version = fixiapi.get_sw_version()
    print("[Demo 06 ]get_sw_version: %d, version = %s" % (ret1, ''.join(chr(i) for i in version)))
    ret1, version = fixiapi.get_hw_version()

    elec_type = hex_data.bytes_to_uint24_big(version[0:3])
    mech_type = hex_data.bytes_to_uint24_big(version[3:6])
    argc_type = hex_data.bytes_to_uint24_big(version[6:9])
    ctrl_type = version[9]
    intf_type = version[10]
    print("[Demo 06 ]get_hw_version: %d, elec_type:%d mech_type:%x argc_type:%x ctrl_type:%x intf_type:%d" %
          (ret1, elec_type, mech_type, argc_type, ctrl_type, intf_type))
    print(" ")

    ret1, value = fixiapi.get_temp_limit()
    print("[Demo 06 ]get_temp_limit: %d, value = %d %d" % (ret1, value[0], value[1]))
    ret1, value = fixiapi.get_volt_limit()
    print("[Demo 06 ]get_volt_limit: %d, value = %d %d" % (ret1, value[0], value[1]))
    ret1, value = fixiapi.get_curr_limit()
    print("[Demo 06 ]get_curr_limit: %d, value = %f" % (ret1, value))
    print(" ")

    ret, value = fixiapi.get_motion_mode()
    print("[Demo 06 ]get_motion_mode  : %d, value = %d" % (ret, value))
    ret, value = fixiapi.get_motion_enable()
    print("[Demo 06 ]get_motion_enable: %d, value = %d" % (ret, value))
    ret, value = fixiapi.get_temp_driver()
    print("[Demo 06 ]get_temp_driver  : %d, value = %.1f" % (ret, value))
    ret, value = fixiapi.get_temp_motor()
    print("[Demo 06 ]get_temp_motor   : %d, value = %.1f" % (ret, value))
    ret, value = fixiapi.get_bus_volt()
    print("[Demo 06 ]get_bus_volt     : %d, value = %.1f" % (ret, value))
    ret, value = fixiapi.get_bus_curr()
    print("[Demo 06 ]get_bus_curr     : %d, value = %.1f" % (ret, value))
    ret, value = fixiapi.get_error_code()
    print("[Demo 06 ]get_error_code   : %d, value = %d" % (ret, value))
    print(" ")

    ret, value = fixiapi.get_vel_limit_min()
    print("[Demo 06 ]get_vel_limit_min : %d, value = %f" % (ret, value))
    ret, value = fixiapi.get_vel_limit_max()
    print("[Demo 06 ]get_vel_limit_max : %d, value = %f" % (ret, value))
    ret, value = fixiapi.get_tau_limit_min()
    print("[Demo 06 ]get_tau_limit_min : %d, value = %f" % (ret, value))
    ret, value = fixiapi.get_tau_limit_max()
    print("[Demo 06 ]get_tau_limit_max : %d, value = %f" % (ret, value))
    print(" ")

    ret, value = fixiapi.get_pos_target()
    print("[Demo 06 ]get_pos_target : %d, value = %f" % (ret, value))
    ret, value = fixiapi.get_pos_current()
    print("[Demo 06 ]get_pos_current: %d, value = %f" % (ret, value))
    ret, value = fixiapi.get_vel_target()
    print("[Demo 06 ]get_vel_target : %d, value = %f" % (ret, value))
    ret, value = fixiapi.get_vel_current()
    print("[Demo 06 ]get_vel_current: %d, value = %f" % (ret, value))
    ret, value = fixiapi.get_tau_target()
    print("[Demo 06 ]get_tau_target : %d, value = %f" % (ret, value))
    ret, value = fixiapi.get_tau_current()
    print("[Demo 06 ]get_tau_current: %d, value = %f" % (ret, value))

    ret, pid_p = fixiapi.get_pos_pidp()
    print("[Demo 06 ]get_pos_pid    : %d, pid_p = %d" % (ret, pid_p))
    ret, pid_p = fixiapi.get_vel_pidp()
    ret, pid_i = fixiapi.get_vel_pidi()
    print("[Demo 06 ]get_vel_pid    : %d, pid_p = %d, pid_p = %d" % (ret, pid_p, pid_i))
    ret, pid_p = fixiapi.get_tau_pidp()
    ret, pid_i = fixiapi.get_tau_pidi()
    print("[Demo 06 ]get_tau_pid    : %d, pid_p = %d, pid_p = %d\n" % (ret, pid_p, pid_i))

    ret, value = fixiapi.get_pos_smooth_cyc()
    print("[Demo 06 ]get_pos_smooth_cyc: %d, value = %d" % (ret, value))
    ret, value = fixiapi.get_vel_smooth_cyc()
    print("[Demo 06 ]get_vel_smooth_cyc: %d, value = %d" % (ret, value))
    ret, value = fixiapi.get_tau_smooth_cyc()
    print("[Demo 06 ]get_tau_smooth_cyc: %d, value = %d" % (ret, value))
