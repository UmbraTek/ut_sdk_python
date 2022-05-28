#!/usr/bin/env python3
#
# Copyright (C) 2022 UmbraTek Inc. All Rights Reserved.
#
# Software License Agreement (BSD License)
#
# Author: Jimy Zhang <jimy.zhang@umbratek.com> <jimy92@163.com>
# =============================================================================
import sys
import os
import time

sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))
from utapi.cgpio.cgpio_api_file import CgpioApiFile


def main():
    u"""
    This is demo to get the state and parameters of the NTRO GPIO Modules.
    The  Modules ID is 1 and RS485 baud rate is 921600.
    The device port is "/dev/ttyUT2"
    Linux requires super user privileges to run code.
    """

    adra = CgpioApiFile()

    ret = adra.set_out_digit(0, 0)
    ret += adra.open_dc48()
    print("set_frame_ou: %d" % (ret))
    time.sleep(3)

    ret = adra.set_out_digit(0, 1)
    ret += adra.button_led_blink()
    print("set_frame_ou: %d" % (ret))
    time.sleep(3)

    ret = adra.set_out_digit(0, 0)
    ret += adra.button_led_breathing()
    print("set_frame_ou: %d" % (ret))
    time.sleep(3)

    ret = adra.set_out_digit(1, 0)
    ret += adra.button_led_on()
    print("set_frame_ou: %d" % (ret))
    time.sleep(3)

    ret = adra.set_out_digit(0, 0)
    ret += adra.button_led_breathing()
    print("set_frame_ou: %d" % (ret))
    time.sleep(3)

    ret = adra.set_out_digit(1, 0)
    ret += adra.button_led_blink()
    ret += adra.set_auto_startup()
    print("set_frame_ou: %d" % (ret))
    time.sleep(3)

    ret = adra.set_out_digit(1, 1)
    ret += adra.sys_shutdown()
    print("set_frame_ou: %d" % (ret))


if __name__ == "__main__":
    main()
