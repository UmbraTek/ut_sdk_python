# Copyright 2021 The UmbraTek Inc. All Rights Reserved.
#
# Software License Agreement (BSD License)
#
# Author: Jimy Zhang <jimy.zhang@umbratek.com> <jimy92@163.com>
# =============================================================================
import sys
import time
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))
from utapi.flxiv.flxivl_api_serial import FlxiVlApiSerial


def check_ret(ret, fun):
    if ret == 0:
        print("Good! successfully %s" % fun)
    else:
        print("Error! Failed %s %d" % (fun, ret))


def main():
    flxi = FlxiVlApiSerial("/dev/ttyUSB0", 921600)  # instantiate the flxi executor api class
    flxi.connect_to_id(102)  # The ID of the connected target actuator, where the ID is 1

    ret = flxi.set_motion_mode(1)  # Set actuator motion mode 1: position mode
    check_ret(ret, "set_motion_mode")
    ret = flxi.set_motion_enable(1)  # Enable actuator
    check_ret(ret, "set_motion_enable")
    time.sleep(3)
    ret = flxi.set_motion_enable(0)  # Disable actuator
    check_ret(ret, "set_motion_enable")

    while 1:
        time.sleep(0.01)


if __name__ == '__main__':
    main()
