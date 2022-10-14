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
    print("./demo3_motion_torque arg1 arg2")
    print("    [arg1] PC physical connection interface")
    print("           1: USB-To-RS485/CAN /dev/ttyUSBx")
    print("           2: USB-To-RS485/CAN /dev/ttyACMx")
    print("           3: EtherNet-To-RS485/CAN TCP")
    print("           4: EtherNet-To-RS485/CAN UDP")
    print("           5: PCIe-To-RS485/CAN /dev/ttyUT0")
    print("    [arg2] Actuator interface")
    print("           0: RS485")
    print("           1: CAN")
    print("    [arg3] Parameters(optional), such as serial port number, TCP/UDP IP address,")


def check_ret(ret, fun):
    if ret == 0:
        print("Good! successfully %s" % fun)
    else:
        print("Error! Failed %s %d" % (fun, ret))


def main():
    u"""
    This demo controls the actuator running at a constant torque in torque mode.
    The actuator ID is 1 and RS485 baud rate is 921600.
    Linux requires super user privileges to run code.
    run command(USB-To-RS485 + COM:/dev/ttyUSB0):
        python3 example/adra/demo3_motion_torque.py 1 0 0
    run command(EtherNet-To-RS485 + IP:192.168.1.16):
        python3 example/adra/demo3_motion_torque.py 3 0 16
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

    # instantiate the adra executor api class
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

    elif int(sys.argv[1]) == 5:
        if len(sys.argv) == 4:
            com = "/dev/ttyUT" + sys.argv[3]
        else:
            com = "/dev/ttyUT0"

        adra = AdraApiFile(com)
        if adra.is_error():
            return

    adra.connect_to_id(1)  # Step 1: Connect an actuator

    ret = adra.into_motion_mode_tau()  # Step 1: Set the motion mode to torque mode.
    check_ret(ret, "into_motion_mode_tau")

    ret = adra.into_motion_enable()  # Step 2: Enable the actuator.
    check_ret(ret, "into_motion_enable")

    while(1):
        ret = adra.set_tau_target(0.1)  # Step 3: Set the target torque of the actuator.
        check_ret(ret, "set_tau_target")
        time.sleep(4)

        ret = adra.set_tau_target(-0.1)  # Step 3: Set the target torque of the actuator.
        check_ret(ret, "set_tau_target")
        time.sleep(4)


if __name__ == '__main__':
    main()
