#!/usr/bin/env python3
#
# Copyright (C) 2024 UmbraTek Inc. All Rights Reserved.
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
    print("./demo10_motion_cvel arg1 arg2")
    print("    [arg1] PC physical connection interface")
    print("           1: USB-To-RS485 /dev/ttyUSBx")
    print("           2: USB-To-RS485 /dev/ttyACMx")
    print("           3: EtherNet-To-RS485 TCP")
    print("           4: EtherNet-To-RS485 UDP")
    print("           5: PCIe-To-RS485 /dev/ttyUT0")
    print("    [arg2] Parameters(optional), such as serial port number, TCP/UDP IP address,")


def check_ret(ret, fun):
    if ret == 0:
        print("Good! successfully %s" % fun)
    else:
        print("Error! Failed %s %d" % (fun, ret))


def main():
    u"""
    This is a demo of setting the target speed of 3 actuators simultaneously in broadcast mode (one packet).
    This function only supports actuators with RS485 ports.
    The actuator ID is 1 2 3 and RS485 baud rate is 921600.
    Linux requires super user privileges to run code.
    run command(USB-To-RS485 + COM:/dev/ttyUSB0):
        python3 example/adra/demo10_motion_cvel.py 1 0
    run command(EtherNet-To-RS485 + IP:192.168.1.16):
        python3 example/adra/demo10_motion_cvel.py 3 16
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
        ret = adra.into_motion_mode_vel()  # Step 2: Set the motion mode to speed mode.
        check_ret(ret, "into_motion_mode_vel")

        ret = adra.into_motion_enable()  # Step 3: Enable the actuator.
        check_ret(ret, "into_motion_enable")
    time.sleep(1)

    vel1 = [50, 100, 150]
    vel2 = [-50, -100, -150]
    while(1):
        ret = adra.set_cvel_target(id[0], id[number - 1], vel1)  # Step 4: Set the target speed of the actuators.
        check_ret(ret, "set_cvel_target")
        time.sleep(3)

        ret = adra.set_cvel_target(id[0], id[number - 1], vel2)
        check_ret(ret, "set_cvel_target")
        time.sleep(3)


if __name__ == '__main__':
    main()
