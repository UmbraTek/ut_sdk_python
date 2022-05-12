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

sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))
from utapi.adra.adra_api_serial import AdraApiSerial
from utapi.adra.adra_api_tcp import AdraApiTcp
from utapi.adra.adra_api_udp import AdraApiUdp


def print_help():
    print("Select the communication interface and protocol type")
    print("./demo4_get_param arg1 arg2")
    print("    [arg1] 1: Serial COM")
    print("           2: Serial ACM")
    print("           3: TCP")
    print("           4: UDP")
    print("    [arg2] 0: RS485")
    print("           1: CAN")


def main():
    u"""
    This is demo to get the state and parameters of the actuator.
    The actuator ID is 1 and RS485 baud rate is 921600.
    Linux requires super user privileges to run code.
    """

    if len(sys.argv) != 3 and len(sys.argv) != 4:
        print_help()
        return

    bus_type = 0
    if int(sys.argv[2]) == 0 or int(sys.argv[2]) == 1:
        bus_type = int(sys.argv[2])
    else:
        print_help()
        return

    if int(sys.argv[1]) == 1:
        if len(sys.argv) == 4:
            com = "/dev/ttyUSB" + sys.argv[3]
        else:
            com = "/dev/ttyUSB0"
        adra = AdraApiSerial(com, 921600, bus_type)
        if adra.is_error():
            return

    elif int(sys.argv[1]) == 2:
        if len(sys.argv) == 4:
            com = "/dev/ttyACM" + sys.argv[3]
        else:
            com = "/dev/ttyACM0"

        adra = AdraApiSerial(com, 921600, bus_type)
        if adra.is_error():
            return
        adra.into_usb_pm()

    elif int(sys.argv[1]) == 3:
        if len(sys.argv) == 4:
            ip = "192.168.1." + sys.argv[3]
        else:
            ip = "192.168.1.168"

        adra = AdraApiTcp(ip, 6001, bus_type)
        if adra.is_error():
            return

    elif int(sys.argv[1]) == 4:
        if len(sys.argv) == 4:
            ip = "192.168.1." + sys.argv[3]
        else:
            ip = "192.168.1.168"

        adra = AdraApiUdp(ip, 5001, bus_type)
        if adra.is_error():
            return

    adra.connect_to_id(1)

    ret, uuid = adra.get_uuid()
    print("[%d]get_uuid: %d, uuid = %s" % (adra.virid, ret, uuid))
    ret, version = adra.get_sw_version()
    print("[%d]get_sw_version: %d, version = %s" % (adra.virid, ret, version))
    ret, version = adra.get_hw_version()
    print("[%d]get_hw_version: %d, version = %s" % (adra.virid, ret, version))
    ret, version = adra.get_multi_version()
    print("[%d]get_mt_version: %d, version = %s" % (adra.virid, ret, version))
    ret, value = adra.get_mech_ratio()
    print("[%d]get_mech_ratio: %d, value = %d" % (adra.virid, ret, value))
    print(" ")

    ret, value = adra.get_elec_ratio()
    print("[%d]get_elec_ratio: %d, value = %d" % (adra.virid, ret, value))
    ret, value = adra.get_motion_dir()
    print("[%d]get_motion_dir: %d, value = %d" % (adra.virid, ret, value))
    ret, value = adra.get_iwdg_cyc()
    print("[%d]set_iwdg_cyc  : %d, value = %d" % (adra.virid, ret, value))
    ret, min, max = adra.get_temp_limit()
    print("[%d]get_temp_limit: %d, value = %d %d" % (adra.virid, ret, min, max))
    ret, min, max = adra.get_volt_limit()
    print("[%d]get_volt_limit: %d, value = %d %d" % (adra.virid, ret, min, max))
    ret, max = adra.get_curr_limit()
    print("[%d]get_curr_limit: %d, value = %f" % (adra.virid, ret, max))
    print(" ")

    ret, value = adra.get_motion_mode()
    print("[%d]get_motion_mode  : %d, value = %d" % (adra.virid, ret, value))
    ret, value = adra.get_motion_enable()
    print("[%d]get_motion_enable: %d, value = %d" % (adra.virid, ret, value))
    ret, value = adra.get_brake_enable()
    print("[%d]get_brake_enable : %d, value = %d" % (adra.virid, ret, value))
    ret, value = adra.get_temp_driver()
    print("[%d]get_temp_driver  : %d, value = %.1f" % (adra.virid, ret, value))
    ret, value = adra.get_temp_motor()
    print("[%d]get_temp_motor   : %d, value = %.1f" % (adra.virid, ret, value))
    ret, value = adra.get_bus_volt()
    print("[%d]get_bus_volt     : %d, value = %.1f" % (adra.virid, ret, value))
    ret, value = adra.get_bus_curr()
    print("[%d]get_bus_curr     : %d, value = %.1f" % (adra.virid, ret, value))
    ret, value = adra.get_multi_volt()
    print("[%d]get_multi_volt   : %d, value = %.1f" % (adra.virid, ret, value))
    ret, value = adra.get_error_code()
    print("[%d]get_error_code   : %d, value = %d" % (adra.virid, ret, value))
    print(" ")

    ret, value = adra.get_pos_limit_min()
    print("[%d]get_pos_limit_min : %d, value = %f" % (adra.virid, ret, value))
    ret, value = adra.get_pos_limit_max()
    print("[%d]get_pos_limit_max : %d, value = %f" % (adra.virid, ret, value))
    ret, value = adra.get_pos_limit_diff()
    print("[%d]get_pos_limit_diff: %d, value = %f" % (adra.virid, ret, value))
    ret, value = adra.get_vel_limit_min()
    print("[%d]get_vel_limit_min : %d, value = %f" % (adra.virid, ret, value))
    ret, value = adra.get_vel_limit_max()
    print("[%d]get_vel_limit_max : %d, value = %f" % (adra.virid, ret, value))
    ret, value = adra.get_vel_limit_diff()
    print("[%d]get_vel_limit_diff: %d, value = %f" % (adra.virid, ret, value))
    ret, value = adra.get_tau_limit_min()
    print("[%d]get_tau_limit_min : %d, value = %f" % (adra.virid, ret, value))
    ret, value = adra.get_tau_limit_max()
    print("[%d]get_tau_limit_max : %d, value = %f" % (adra.virid, ret, value))
    ret, value = adra.get_tau_limit_diff()
    print("[%d]get_tau_limit_diff: %d, value = %f" % (adra.virid, ret, value))
    print(" ")

    ret, value = adra.get_pos_target()
    print("[%d]get_pos_target : %d, value = %f" % (adra.virid, ret, value))
    ret, value = adra.get_pos_current()
    print("[%d]get_pos_current: %d, value = %f" % (adra.virid, ret, value))
    ret, value = adra.get_vel_target()
    print("[%d]get_vel_target : %d, value = %f" % (adra.virid, ret, value))
    ret, value = adra.get_vel_current()
    print("[%d]get_vel_current: %d, value = %f" % (adra.virid, ret, value))
    ret, value = adra.get_tau_target()
    print("[%d]get_tau_target : %d, value = %f" % (adra.virid, ret, value))
    ret, value = adra.get_tau_current()
    print("[%d]get_tau_current: %d, value = %f" % (adra.virid, ret, value))

    ret, pid_p = adra.get_pos_pidp()
    print("[%d]get_pos_pid    : %d, pid_p = %f" % (adra.virid, ret, pid_p))
    ret, pid_p = adra.get_vel_pidp()
    ret, pid_i = adra.get_vel_pidi()
    print("[%d]get_vel_pid    : %d, pid_p = %f, pid_p = %f" % (adra.virid, ret, pid_p, pid_i))
    ret, pid_p = adra.get_tau_pidp()
    ret, pid_i = adra.get_tau_pidi()
    print("[%d]get_tau_pid    : %d, pid_p = %f, pid_p = %f\n" % (adra.virid, ret, pid_p, pid_i))

    ret, value = adra.get_pos_smooth_cyc()
    print("[%d]get_pos_smooth_cyc: %d, value = %f" % (adra.virid, ret, value))
    ret, value = adra.get_vel_smooth_cyc()
    print("[%d]get_vel_smooth_cyc: %d, value = %f" % (adra.virid, ret, value))
    ret, value = adra.get_tau_smooth_cyc()
    print("[%d]get_tau_smooth_cyc: %d, value = %f" % (adra.virid, ret, value))


if __name__ == "__main__":
    main()
