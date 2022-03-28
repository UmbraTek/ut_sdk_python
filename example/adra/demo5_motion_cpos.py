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
    u"""
    Broadcast mode (one packet) sets 3 actuator target positions.
    The actuator ID is 1 2 3 and RS485 baud rate is 921600.
    For better test results, make sure the actuator's current position is within ±100 radians.
    Linux requires super user privileges to run code.
    """
    adra = AdraApiSerial("/dev/ttyUSB0", 921600)  # instantiate the adra executor api class

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
