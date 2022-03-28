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
    Broadcast mode (one packet) sets 3 actuator target torque.
    The actuator ID is 1 2 3 and RS485 baud rate is 921600.
    Linux requires super user privileges to run code.
    """
    adra = AdraApiSerial("/dev/ttyUSB0", 921600)  # instantiate the adra executor api class

    number = 3
    id = [1, 2, 3]

    for i in range(number):
        adra.connect_to_id(id[i])  # Step 1: Connect an actuator
        ret = adra.into_motion_mode_tau()  # Step 2: Set the motion mode to torque mode.
        check_ret(ret, "into_motion_mode_tau")

        ret = adra.into_motion_enable()  # Step 3: Enable the actuator.
        check_ret(ret, "into_motion_enable")
    time.sleep(1)

    tau1 = [0.1, 0.05, 0]
    tau2 = [-0.1, -0.05, -0]

    while(1):
        ret = adra.set_ctau_target(id[0], id[number - 1], tau1)  # Step 4: Set the target torque of the actuators.
        check_ret(ret, "set_ctau_target")
        time.sleep(2)

        ret = adra.set_ctau_target(id[0], id[number - 1], tau2)
        check_ret(ret, "set_ctau_target")
        time.sleep(2)


if __name__ == '__main__':
    main()
