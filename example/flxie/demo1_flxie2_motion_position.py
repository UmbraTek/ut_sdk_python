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
from utapi.flxie.flxie2_api_serial import FlxiE2ApiSerial


def check_ret(ret, fun):
    if ret == 0:
        print("Good! successfully %s" % fun)
    else:
        print("Error! Failed %s %d" % (fun, ret))


def main():
    flxi = FlxiE2ApiSerial("/dev/ttyUSB0", 921600)  # instantiate the flxi executor api class
    flxi.connect_to_id(101)  # The ID of the connected target actuator, where the ID is 1

    ret = flxi.set_motion_mode(1)  # Set actuator motion mode 1: position mode
    check_ret(ret, "set_motion_mode")
    ret = flxi.set_motion_enable(1)  # Enable actuator
    check_ret(ret, "set_motion_enable")
    ret = flxi.set_pos_target(0.5)  # Set the actuator to move to a position of 0.5 radians
    check_ret(ret, "set_pos_target")
    time.sleep(5)
    ret = flxi.set_pos_target(0.1)  # Set the actuator to move to 0.1 rad
    check_ret(ret, "set_pos_target")

    while 1:
        time.sleep(0.01)


if __name__ == '__main__':
    main()
