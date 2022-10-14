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

if __name__ == '__main__':
    u"""This is a demo of pass-through data to rs485 at the end of the manipulator.
    The command to pass-through data will wait for the preceding robot motion command to be executed before taking effect.
    run command:
        python3 example/utra/demo32_rs485_pass_que.py --ip 192.168.1.xxx
    """
    parser = argparse.ArgumentParser()
    parser.description = 'UTRA demo'
    parser.add_argument("--ip", help=" ", default="127.0.0.1", type=str)
    args = parser.parse_args()

    ubot = UtraApiTcp(args.ip)
    ret, value = ubot.get_motion_status()
    print("[Demo 08 ] get_motion_status :%d %d" % (ret, value))
    ret, value = ubot.get_error_code()
    print("[Demo 08 ] get_error_code    :%d %d %d" % (ret, value[0], value[1]))
    ret = ubot.reset_err()
    print("[Demo 08 ] reset_err    :%d" % (ret))
    ret = ubot.set_motion_enable(9, 1)
    print("[Demo 08 ] set_motion_enable :%d" % (ret))
    ret = ubot.set_motion_status(0)
    print("[Demo 08 ] set_motion_status :%d" % (ret))
    print(" ")

    ret = ubot.plan_sleep(1)
    print("[Demo 08 ] plan_sleep :%d" % (ret))

    tx_len = 7
    tx_data = bytes([0xAA, 0x03, 0x02, 0xA0, 0x01, 0x24, 0x5C])
    ret = ubot.set_pass_rs485_que(RS485_LINE.TGPIO, tx_len, tx_data)
    print("[Demo 08 ] set_pass_rs485_que :%d" % (ret))

    tx_len = 7
    tx_data = bytes([0xAA, 0x03, 0x02, 0xA1, 0x01, 0x25, 0xCC])
    ret = ubot.set_pass_rs485_que(RS485_LINE.TGPIO, tx_len, tx_data)
    print("[Demo 08 ] set_pass_rs485_que :%d" % (ret))

    tx_len = 10
    tx_data = bytes([0xAA, 0x03, 0x05, 0xB0, 0x01, 0x31, 0x2D, 0x00, 0xF5, 0xE0])
    ret = ubot.set_pass_rs485_que(RS485_LINE.TGPIO, tx_len, tx_data)
    print("[Demo 08 ] set_pass_rs485_que :%d" % (ret))

    ret = ubot.plan_sleep(5)
    print("[Demo 08 ] plan_sleep :%d" % (ret))

    tx_len = 10
    tx_data = bytes([0xAA, 0x03, 0x05, 0xB0, 0xFE, 0xCE, 0xD3, 0x00, 0xB5, 0xA4])
    ret = ubot.set_pass_rs485_que(RS485_LINE.TGPIO, tx_len, tx_data)
    print("[Demo 08 ] set_pass_rs485_que :%d" % (ret))

    ret = ubot.plan_sleep(10)
    print("[Demo 08 ] plan_sleep :%d" % (ret))

    tx_len = 7
    tx_data = bytes([0xAA, 0x03, 0x02, 0xA0, 0x03, 0xA5, 0x9D])
    ret = ubot.set_pass_rs485_que(RS485_LINE.TGPIO, tx_len, tx_data)
    print("[Demo 08 ] set_pass_rs485_que :%d" % (ret))

    tx_len = 7
    tx_data = bytes([0xAA, 0x03, 0x02, 0xA1, 0x01, 0x25, 0xCC])
    ret = ubot.set_pass_rs485_que(RS485_LINE.TGPIO, tx_len, tx_data)
    print("[Demo 08 ] set_pass_rs485_que :%d" % (ret))

    tx_len = 10
    tx_data = bytes([0xAA, 0x03, 0x05, 0xD0, 0x00, 0x00, 0xC3, 0x50, 0x68, 0x47])
    ret = ubot.set_pass_rs485_que(RS485_LINE.TGPIO, tx_len, tx_data)
    print("[Demo 08 ] set_pass_rs485_now :%d" % (ret))
