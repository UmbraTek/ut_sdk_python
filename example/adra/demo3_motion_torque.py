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
    This demo controls the actuator running at a constant torque in torque mode.
    The actuator ID is 1 and RS485 baud rate is 921600.
    Linux requires super user privileges to run code.
    """
    adra = AdraApiSerial("/dev/ttyUSB0", 921600)  # instantiate the adra executor api class
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
