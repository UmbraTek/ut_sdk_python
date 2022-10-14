#!/usr/bin/env python3
#
# Copyright (C) 2021 UmbraTek Inc. All Rights Reserved.
#
# Software License Agreement (BSD License)
#
# Author: Jimy Zhang <jimy.zhang@umbratek.com> <jimy92@163.com>
# =============================================================================
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))
from utapi.flxie.flxie2_api_serial import FlxiE2ApiSerial


def main():
    u"""
    This is demo to get the state and parameters of the gripper.
    The gripper ID is 101 and RS485 baud rate is 921600.
    Linux requires super user privileges to run code.
    run command(USB-To-RS485 + COM:/dev/ttyUSB0):
        python3 example/flxie/demo3_flxie2_get_param.py
    """
    flxi = FlxiE2ApiSerial("/dev/ttyUSB0", 921600)
    flxi.connect_to_id(101)

    ret, uuid = flxi.get_uuid()
    print("[%d]get_uuid: %d, uuid = %s" % (flxi.virid, ret, uuid))
    ret, version = flxi.get_sw_version()
    print("[%d]get_sw_version: %d, version = %s" % (flxi.virid, ret, version))
    ret, version = flxi.get_hw_version()
    print("[%d]get_hw_version: %d, version = %s" % (flxi.virid, ret, version))
    print(" ")

    ret, min, max = flxi.get_temp_limit()
    print("[%d]get_temp_limit: %d, value = %d %d" % (flxi.virid, ret, min, max))
    ret, min, max = flxi.get_volt_limit()
    print("[%d]get_volt_limit: %d, value = %d %d" % (flxi.virid, ret, min, max))
    ret, max = flxi.get_curr_limit()
    print("[%d]get_curr_limit: %d, value = %f" % (flxi.virid, ret, max))
    print(" ")

    ret, value = flxi.get_motion_mode()
    print("[%d]get_motion_mode  : %d, value = %d" % (flxi.virid, ret, value))
    ret, value = flxi.get_motion_enable()
    print("[%d]get_motion_enable: %d, value = %d" % (flxi.virid, ret, value))
    ret, value = flxi.get_temp_driver()
    print("[%d]get_temp_driver  : %d, value = %.1f" % (flxi.virid, ret, value))
    ret, value = flxi.get_temp_motor()
    print("[%d]get_temp_motor   : %d, value = %.1f" % (flxi.virid, ret, value))
    ret, value = flxi.get_bus_volt()
    print("[%d]get_bus_volt     : %d, value = %.1f" % (flxi.virid, ret, value))
    ret, value = flxi.get_bus_curr()
    print("[%d]get_bus_curr     : %d, value = %.1f" % (flxi.virid, ret, value))
    ret, value = flxi.get_error_code()
    print("[%d]get_error_code   : %d, value = %d" % (flxi.virid, ret, value))
    print(" ")

    ret, value = flxi.get_pos_limit_min()
    print("[%d]get_pos_limit_min : %d, value = %f" % (flxi.virid, ret, value))
    ret, value = flxi.get_pos_limit_max()
    print("[%d]get_pos_limit_max : %d, value = %f" % (flxi.virid, ret, value))
    ret, value = flxi.get_vel_limit_min()
    print("[%d]get_vel_limit_min : %d, value = %f" % (flxi.virid, ret, value))
    ret, value = flxi.get_vel_limit_max()
    print("[%d]get_vel_limit_max : %d, value = %f" % (flxi.virid, ret, value))
    ret, value = flxi.get_tau_limit_min()
    print("[%d]get_tau_limit_min : %d, value = %f" % (flxi.virid, ret, value))
    ret, value = flxi.get_tau_limit_max()
    print("[%d]get_tau_limit_max : %d, value = %f" % (flxi.virid, ret, value))
    print(" ")

    ret, value = flxi.get_debug_mode()
    print("[%d]get_debug_mode: %d, value = %d" % (flxi.virid, ret, value))
    print(" ")

    ret, value = flxi.get_pos_target()
    print("[%d]get_pos_target : %d, value = %f" % (flxi.virid, ret, value))
    ret, value = flxi.get_pos_current()
    print("[%d]get_pos_current: %d, value = %f" % (flxi.virid, ret, value))
    ret, value = flxi.get_vel_current()
    print("[%d]get_vel_current: %d, value = %f" % (flxi.virid, ret, value))
    ret, value = flxi.get_tau_target()
    print("[%d]get_tau_target : %d, value = %f" % (flxi.virid, ret, value))
    ret, value = flxi.get_tau_current()
    print("[%d]get_tau_current: %d, value = %f" % (flxi.virid, ret, value))

    ret, pid_p = flxi.get_pos_pidp()
    print("[%d]get_pos_pid    : %d, pid_p = %f" % (flxi.virid, ret, pid_p))
    ret, pid_p = flxi.get_vel_pidp()
    ret, pid_i = flxi.get_vel_pidi()
    print("[%d]get_vel_pid    : %d, pid_p = %f, pid_p = %f" % (flxi.virid, ret, pid_p, pid_i))
    ret, pid_p = flxi.get_tau_pidp()
    ret, pid_i = flxi.get_tau_pidi()
    print("[%d]get_tau_pid    : %d, pid_p = %f, pid_p = %f\n" % (flxi.virid, ret, pid_p, pid_i))

    ret, value = flxi.get_pos_smooth_cyc()
    print("[%d]get_pos_smooth_cyc: %d, value = %f" % (flxi.virid, ret, value))
    ret, value = flxi.get_vel_smooth_cyc()
    print("[%d]get_vel_smooth_cyc: %d, value = %f" % (flxi.virid, ret, value))
    ret, value = flxi.get_tau_smooth_cyc()
    print("[%d]get_tau_smooth_cyc: %d, value = %f" % (flxi.virid, ret, value))


if __name__ == '__main__':
    main()
