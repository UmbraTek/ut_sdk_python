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
from utapi.adra.adra_api_serial import AdraApiSerial


def check_ret(ret, fun):
    if ret == 0:
        print("Good! successfully %s" % fun)
    else:
        print("Error! Failed %s %d" % (fun, ret))


def main():
    adra = AdraApiSerial("/dev/ttyUSB0", 921600)  # instantiate the adra executor api class
    adra.connect_to_id(1)  # The ID of the connected target actuator, where the ID is 1

    ret = adra.set_motion_mode(1)  # Set actuator motion mode 1: position mode
    check_ret(ret, "set_motion_mode")
    ret = adra.set_motion_enable(1)  # Enable actuator
    check_ret(ret, "set_motion_enable")
    ret = adra.set_pos_target(50)  # Set the actuator to move to a position of 50 radians
    check_ret(ret, "set_pos_target")
    time.sleep(3)
    ret = adra.set_pos_target(-50)  # Set the actuator to move to -50 rad
    check_ret(ret, "set_pos_target")

    while 1:
        time.sleep(0.01)


if __name__ == '__main__':
    main()
