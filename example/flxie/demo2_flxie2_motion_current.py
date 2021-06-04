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
from utapi.flxie.flxie2_api_serial import FlxiE2ApiSerial


def check_ret(ret, fun):
    if ret == 0:
        print("Good! successfully %s" % fun)
    else:
        print("Error! Failed %s %d" % (fun, ret))


def main():
    flxi = FlxiE2ApiSerial("/dev/ttyUSB0", 921600)  # instantiate the flxi executor api class
    flxi.connect_to_id(101)  # The ID of the connected target actuator, where the ID is 1

    ret = flxi.set_motion_mode(3)  # Set actuator motion mode 3: current mode
    check_ret(ret, "set_motion_mode")
    ret = flxi.set_motion_enable(1)  # Enable actuator
    check_ret(ret, "set_motion_enable")
    ret = flxi.set_tau_target(0.8)  # Set actuator motion current 0.8A
    check_ret(ret, "set_tau_target")

    while 1:
        time.sleep(0.01)


if __name__ == '__main__':
    main()
