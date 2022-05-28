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
from utapi.utra.utra_flxie_api import UtraFlxiE2Api

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.description = 'UTRA demo'
    parser.add_argument("--ip", help=" ", default="127.0.0.1", type=str)
    args = parser.parse_args()

    ubot = UtraApiTcp(args.ip)
    fixie = UtraFlxiE2Api(ubot, 101)

    ret1, uuid = fixie.get_uuid()
    print("get_uuid: %d, uuid = %s" % (ret1, uuid))
    ret1, version = fixie.get_sw_version()
    print("get_sw_version: %d, version = %s" % (ret1, version))
    ret1, version = fixie.get_hw_version()
    print("get_hw_version: %d, version = %s" % (ret1, version))
    print(" ")

    ret1, value = fixie.get_temp_limit()
    print("get_temp_limit: %d, value = %d %d" % (ret1, value[0], value[1]))
    ret1, value = fixie.get_volt_limit()
    print("get_volt_limit: %d, value = %d %d" % (ret1, value[0], value[1]))
    ret1, value = fixie.get_curr_limit()
    print("get_curr_limit: %d, value = %f" % (ret1, value))
    print(" ")

    ret, value = fixie.get_motion_mode()
    print("get_motion_mode  : %d, value = %d" % (ret, value))
    ret, value = fixie.get_motion_enable()
    print("get_motion_enable: %d, value = %d" % (ret, value))
    ret, value = fixie.get_temp_driver()
    print("get_temp_driver  : %d, value = %.1f" % (ret, value))
    ret, value = fixie.get_temp_motor()
    print("get_temp_motor   : %d, value = %.1f" % (ret, value))
    ret, value = fixie.get_bus_volt()
    print("get_bus_volt     : %d, value = %.1f" % (ret, value))
    ret, value = fixie.get_bus_curr()
    print("get_bus_curr     : %d, value = %.1f" % (ret, value))
    ret, value = fixie.get_error_code()
    print("get_error_code   : %d, value = %d" % (ret, value))
    print(" ")

    ret, value = fixie.get_vel_limit_min()
    print("get_vel_limit_min : %d, value = %f" % (ret, value))
    ret, value = fixie.get_vel_limit_max()
    print("get_vel_limit_max : %d, value = %f" % (ret, value))
    ret, value = fixie.get_tau_limit_min()
    print("get_tau_limit_min : %d, value = %f" % (ret, value))
    ret, value = fixie.get_tau_limit_max()
    print("get_tau_limit_max : %d, value = %f" % (ret, value))
    print(" ")

    ret, value = fixie.get_pos_target()
    print("get_pos_target : %d, value = %f" % (ret, value))
    ret, value = fixie.get_pos_current()
    print("get_pos_current: %d, value = %f" % (ret, value))
    ret, value = fixie.get_tau_target()
    print("get_tau_target : %d, value = %f" % (ret, value))
    ret, value = fixie.get_tau_current()
    print("get_tau_current: %d, value = %f" % (ret, value))

    ret, pid_p = fixie.get_pos_pidp()
    print("get_pos_pid    : %d, pid_p = %d" % (ret, pid_p))
    ret, pid_p = fixie.get_tau_pidp()
    ret, pid_i = fixie.get_tau_pidi()
    print("get_tau_pid    : %d, pid_p = %d, pid_p = %d\n" % (ret, pid_p, pid_i))

    ret, value = fixie.get_pos_smooth_cyc()
    print("get_pos_smooth_cyc: %d, value = %d" % (ret, value))
    ret, value = fixie.get_tau_smooth_cyc()
    print("get_tau_smooth_cyc: %d, value = %d" % (ret, value))

    ret, acc = fixie.get_pos_adrc_param(3)
    ret, b2 = fixie.get_pos_adrc_param(9)
    ret, b3 = fixie.get_pos_adrc_param(10)
    ret, h1 = fixie.get_pos_adrc_param(12)
    ret, d = fixie.get_pos_adrc_param(14)
    print("get_pos_adrc_param: %d, value = %f %f %f %f %f" % (ret, acc, b2, b3, h1, d))
    ret, acc = fixie.get_tau_adrc_param(3)
    ret, b2 = fixie.get_tau_adrc_param(9)
    ret, b3 = fixie.get_tau_adrc_param(10)
    ret, h1 = fixie.get_tau_adrc_param(12)
    ret, d = fixie.get_tau_adrc_param(14)
    print("get_tau_adrc_param: %d, value = %f %f %f %f %f" % (ret, acc, b2, b3, h1, d))

    ret, value = fixie.get_senser()
    print("get_senser: %d, value = %f %f %f %f" % (ret, value[0], value[1], value[2], value[3]))
