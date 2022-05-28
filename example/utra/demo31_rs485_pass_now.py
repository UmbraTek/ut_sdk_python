#!/usr/bin/env python3
#
# Copyright (C) 2021 UmbraTek Inc. All Rights Reserved.
#
# Software License Agreement (BSD License)
#
# Author: Jimy Zhang <jimy.zhang@umbratek.com> <jimy92@163.com>
# =============================================================================
import sys
import argparse
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))
from utapi.utra.utra_api_tcp import UtraApiTcp
from utapi.base.arm_reg import RS485_LINE
from utapi.common import print_msg

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.description = 'UTRA demo'
    parser.add_argument("--ip", help=" ", default="127.0.0.1", type=str)
    args = parser.parse_args()

    ubot = UtraApiTcp(args.ip)

    ret = ubot.plan_sleep(1)
    print("[Demo 08 ] plan_sleep :%d" % (ret))

    tx_len = 7
    rx_len = 6
    tx_data = bytes([0xAA, 0x03, 0x02, 0xA0, 0x01, 0x24, 0x5C])
    ret, value = ubot.set_pass_rs485_now(RS485_LINE.TGPIO, 10, tx_len, rx_len, tx_data)
    print("[Demo 08 ] set_pass_rs485_now :%d" % (ret))
    print_msg.nhex("    ", value, rx_len + 1)

    tx_len = 7
    rx_len = 6
    tx_data = bytes([0xAA, 0x03, 0x02, 0xA1, 0x01, 0x25, 0xCC])
    ret, value = ubot.set_pass_rs485_now(RS485_LINE.TGPIO, 10, tx_len, rx_len, tx_data)
    print("[Demo 08 ] set_pass_rs485_now :%d" % (ret))
    print_msg.nhex("    ", value, rx_len + 1)

    tx_len = 10
    rx_len = 6
    tx_data = bytes([0xAA, 0x03, 0x05, 0xB0, 0x01, 0x31, 0x2D, 0x00, 0xF5, 0xE0])
    ret, value = ubot.set_pass_rs485_now(RS485_LINE.TGPIO, 10, tx_len, rx_len, tx_data)
    print("[Demo 08 ] set_pass_rs485_now :%d" % (ret))
    print_msg.nhex("    ", value, rx_len + 1)

    ret = ubot.plan_sleep(5)
    print("[Demo 08 ] plan_sleep :%d" % (ret))

    tx_len = 10
    rx_len = 6
    tx_data = bytes([0xAA, 0x03, 0x05, 0xB0, 0xFE, 0xCE, 0xD3, 0x00, 0xB5, 0xA4])
    ret, value = ubot.set_pass_rs485_now(RS485_LINE.TGPIO, 10, tx_len, rx_len, tx_data)
    print("[Demo 08 ] set_pass_rs485_now :%d" % (ret))
    print_msg.nhex("    ", value, rx_len + 1)

    ret = ubot.plan_sleep(10)
    print("[Demo 08 ] plan_sleep :%d" % (ret))

    tx_len = 7
    rx_len = 6
    tx_data = bytes([0xAA, 0x03, 0x02, 0xA0, 0x03, 0xA5, 0x9D])
    ret, value = ubot.set_pass_rs485_now(RS485_LINE.TGPIO, 10, tx_len, rx_len, tx_data)
    print("[Demo 08 ] set_pass_rs485_now :%d" % (ret))
    print_msg.nhex("    ", value, rx_len + 1)

    tx_len = 7
    rx_len = 6
    tx_data = bytes([0xAA, 0x03, 0x02, 0xA1, 0x01, 0x25, 0xCC])
    ret, value = ubot.set_pass_rs485_now(RS485_LINE.TGPIO, 10, tx_len, rx_len, tx_data)
    print("[Demo 08 ] set_pass_rs485_now :%d" % (ret))
    print_msg.nhex("    ", value, rx_len + 1)

    tx_len = 10
    rx_len = 6
    tx_data = bytes([0xAA, 0x03, 0x05, 0xD0, 0x00, 0x00, 0xC3, 0x50, 0x68, 0x47])
    ret, value = ubot.set_pass_rs485_now(RS485_LINE.TGPIO, 10, tx_len, rx_len, tx_data)
    print("[Demo 08 ] set_pass_rs485_now :%d" % (ret))
    print_msg.nhex("    ", value, rx_len + 1)
