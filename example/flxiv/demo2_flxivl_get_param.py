# Copyright 2021 The UmbraTek Inc. All Rights Reserved.
#
# Software License Agreement (BSD License)
#
# Author: Jimy Zhang <jimy.zhang@umbratek.com> <jimy92@163.com>
# =============================================================================
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))
from utapi.flxiv.flxivl_api_serial import FlxiVlApiSerial
from utapi.common import print_msg


def main():
    flxi = FlxiVlApiSerial("/dev/ttyUSB0", 921600)
    flxi.connect_to_id(102)

    ret, uuid = flxi.get_uuid()
    print("[%d]get_uuid: %d, uuid = %s" % (flxi.virid, ret, uuid))
    ret, version = flxi.get_sw_version()
    print("[%d]get_sw_version: %d, version = %s" % (flxi.virid, ret, version))
    ret, version = flxi.get_hw_version()
    print("[%d]get_hw_version: %d, version = %s" % (flxi.virid, ret, version))
    print(" ")

    ret, min, max = flxi.get_temp_limit()
    print("[%d]get_temp_limit: %d, value = %d %d" % (flxi.virid, ret, min, max))
    ret, min, max = flxi.get_volt_limit()
    print("[%d]get_volt_limit: %d, value = %d %d" % (flxi.virid, ret, min, max))
    print(" ")

    ret, value = flxi.get_motion_mode()
    print("[%d]get_motion_mode  : %d, value = %d" % (flxi.virid, ret, value))
    ret, value = flxi.get_motion_enable()
    print("[%d]get_motion_enable: %d, value = %d" % (flxi.virid, ret, value))
    ret, value = flxi.get_temp_driver()
    print("[%d]get_temp_driver  : %d, value = %.1f" % (flxi.virid, ret, value))
    ret, value = flxi.get_temp_motor()
    print("[%d]get_temp_motor   : %d, value = %.1f" % (flxi.virid, ret, value))
    ret, value = flxi.get_bus_volt()
    print("[%d]get_bus_volt     : %d, value = %.1f" % (flxi.virid, ret, value))
    ret, value = flxi.get_bus_curr()
    print("[%d]get_bus_curr     : %d, value = %.1f" % (flxi.virid, ret, value))
    ret, value = flxi.get_error_code()
    print("[%d]get_error_code   : %d, value = %d" % (flxi.virid, ret, value))
    print(" ")


if __name__ == '__main__':
    main()
