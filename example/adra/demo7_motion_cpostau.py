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


def print_help():
    print("Select the communication interface and protocol type")
    print("./demo7_motion_cpostau arg1")
    print("    [arg1] 1: Serial COM")
    print("           2: Serial ACM")
    print("           3: TCP")
    print("           4: UDP")


def check_ret(ret, fun):
    if ret == 0:
        print("Good! successfully %s" % fun)
    else:
        print("Error! Failed %s %d" % (fun, ret))


def main():
    u"""
    Set the maximum interval of broadcast read commands.
    Broadcast mode (one packet) sets 3 actuator target positions and feedforward torques.
    The broadcast mode (a packet) gets the current position and current torque of the three actuators.
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

    number = 3
    id = [1, 2, 3]

    for i in range(number):
        adra.connect_to_id(id[i])  # Step 1: Connect an actuator

        ret = adra.into_motion_mode_pos()  # Step 2: Set the motion mode to position mode.
        check_ret(ret, "into_motion_mode_pos")

        ret = adra.into_motion_enable()  # Step 3: Enable the actuator.
        check_ret(ret, "into_motion_enable")

        # Step 4: Set the time to 200000 current loop cycles,
        # because the current loop is 20K, so it is a 10-second interval
        ret = adra.set_iwdg_cyc(200000)
        check_ret(ret, "set_iwdg_cyc")

    time.sleep(1)

    pos1 = [31.4, 62.8, 15.7]
    pos2 = [-31.4, -62.8, -15.7]
    tau1 = [0.1, 0.05, 0]
    tau2 = [-0.1, -0.05, -0]
    while(1):
        # Step 5: Sets the current positions and feedforward torques of the three actuators
        ret = adra.set_cpostau_target(id[0], id[number - 1], pos1, tau1)
        check_ret(ret, "set_cpostau_target")

        # Step 6: Read the current position and torque of the three actuators
        rets, broadcast_num, pos, tau = adra.get_cpostau_current(id[0], id[number - 1])
        print("get_cpostau_current: pos: %f %f %f, tau: %f %f %f" % (pos[0], pos[1], pos[2], tau[0], tau[1], tau[2]))
        print("get_cpostau_current: broadcast_num:%d %d %d, ret:%d %d %d\n" %
              (broadcast_num[0], broadcast_num[1], broadcast_num[2], rets[0], rets[1], rets[2]))
        time.sleep(4)

        ret = adra.set_cpostau_target(id[0], id[number - 1], pos2, tau2)
        check_ret(ret, "set_cpostau_target")

        rets, broadcast_num, pos, tau = adra.get_cpostau_current(id[0], id[number - 1])
        print("get_cpostau_current: pos: %f %f %f, tau: %f %f %f" % (pos[0], pos[1], pos[2], tau[0], tau[1], tau[2]))
        print("get_cpostau_current: broadcast_num:%d %d %d, ret:%d %d %d\n" %
              (broadcast_num[0], broadcast_num[1], broadcast_num[2], rets[0], rets[1], rets[2]))
        time.sleep(4)


if __name__ == '__main__':
    main()
