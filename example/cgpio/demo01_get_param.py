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

sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))
from utapi.cgpio.cgpio_api_file import CgpioApiFile
from utapi.common import print_msg


def main():
    u"""
    This is demo to get the state and parameters of the NTRO GPIO Modules.
    The  Modules ID is 1 and RS485 baud rate is 921600.
    The device port is "/dev/ttyUT2"
    Linux requires super user privileges to run code.
    """

    nrto_gpio = CgpioApiFile()

    ret, uuid = nrto_gpio.get_uuid()
    print("get_uuid: %d, uuid = %s" % (ret, uuid))
    ret, version = nrto_gpio.get_sw_version()
    print("get_sw_version: %d, version = %s" % (ret, version))
    ret, version = nrto_gpio.get_hw_version()
    print("get_hw_version: %d, version = %s" % (ret, version))
    print(" ")

    ret, fun, digitin, adc_v, adc_n = nrto_gpio.get_frame_in()
    print("get_frame_in  : %d, fun: 0x%x,  digitin: 0x%x, adc_n: %d" % (ret, fun, digitin, adc_n))
    print_msg.nvect_03f("    : ", adc_v, adc_n)

    ret, fun, digitou, dac_v, dac_n = nrto_gpio.get_frame_ou()
    print("get_frame_ou  : %d, fun: 0x%x,  digitou: 0x%x, adc_n: %d" % (ret, fun, digitou, dac_n))


if __name__ == "__main__":
    main()
