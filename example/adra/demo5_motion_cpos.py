#!/usr/bin/env python3
#
# Copyright (C) 2021 UmbraTek Inc. All Rights Reserved.
#
# Software License Agreement (BSD License)
#
# Author: Jimy Zhang <jimy.zhang@umbratek.com> <jimy92@163.com>
# =============================================================================
import sys
import time
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))
from utapi.adra.adra_api_serial import AdraApiSerial
from utapi.adra.adra_api_tcp import AdraApiTcp
from utapi.adra.adra_api_udp import AdraApiUdp
from utapi.adra.adra_api_file import AdraApiFile


def print_help():
    print("Select the communication interface and protocol type")
    print("./demo1_motion_position arg1 arg2")
    print("    [arg1] PC physical connection interface")
    print("           1: USB-To-RS485/CAN /dev/ttyUSBx")
    print("           2: USB-To-RS485/CAN /dev/ttyACMx")
    print("           3: EtherNet-To-RS485/CAN TCP")
    print("           4: EtherNet-To-RS485/CAN UDP")
    print("           5: PCIe-To-RS485/CAN /dev/ttyUT0")
    print("    [arg2] Parameters(optional), such as serial port number, TCP/UDP IP address,")


def check_ret(ret, fun):
    if ret == 0:
        print("Good! successfully %s" % fun)
    else:
        print("Error! Failed %s %d" % (fun, ret))


def main():
    u"""
    Broadcast mode (one packet) sets 3 actuator target positions.
    This function only supports actuators with RS485 ports.
    The actuator ID is 1 2 3 and RS485 baud rate is 921600.
    For better test results, make sure the actuator's current position is within ±100 radians.
    Linux requires super user privileges to run code.
    """

    if len(sys.argv) != 2 and len(sys.argv) != 3:
        print_help()
        return

    bus_type = 0

    if int(sys.argv[1]) == 1:
        if len(sys.argv) == 3:
            com = "/dev/ttyUSB" + sys.argv[2]
        else:
            com = "/dev/ttyUSB0"
        adra = AdraApiSerial(com, 921600, bus_type)
        if adra.is_error():
            return

    elif int(sys.argv[1]) == 2:
        if len(sys.argv) == 3:
            com = "/dev/ttyACM" + sys.argv[2]
        else:
            com = "/dev/ttyACM0"

        adra = AdraApiSerial(com, 921600, bus_type)
        if adra.is_error():
            return
        adra.into_usb_pm()

    elif int(sys.argv[1]) == 3:
        if len(sys.argv) == 3:
            ip = "192.168.1." + sys.argv[2]
        else:
            ip = "192.168.1.168"

        adra = AdraApiTcp(ip, 6001, bus_type)
        if adra.is_error():
            return

    elif int(sys.argv[1]) == 4:
        if len(sys.argv) == 3:
            ip = "192.168.1." + sys.argv[2]
        else:
            ip = "192.168.1.168"

        adra = AdraApiUdp(ip, 5001, bus_type)
        if adra.is_error():
            return

    elif int(sys.argv[1]) == 5:
        if len(sys.argv) == 4:
            com = "/dev/ttyUT" + sys.argv[2]
        else:
            com = "/dev/ttyUT0"

        adra = AdraApiFile(com)
        if adra.is_error():
            return

    number = 3
    id = [1, 2, 3]

    for i in range(number):
        adra.connect_to_id(id[i])  # Step 1: Connect an actuator
        ret = adra.into_motion_mode_pos()  # Step 2: Set the motion mode to position mode.
        check_ret(ret, "into_motion_mode_pos")

        ret = adra.into_motion_enable()  # Step 3: Enable the actuator.
        check_ret(ret, "into_motion_enable")
    time.sleep(1)

    pos1 = [31.4, 62.8, 15.7]
    pos2 = [-31.4, -62.8, -15.7]
    while(1):
        ret = adra.set_cpos_target(id[0], id[number - 1], pos1)  # Step 4: Set the target position of the actuators.
        check_ret(ret, "set_cpos_target")
        time.sleep(3)

        ret = adra.set_cpos_target(id[0], id[number - 1], pos2)
        check_ret(ret, "set_cpos_target")
        time.sleep(3)


if __name__ == '__main__':
    main()
