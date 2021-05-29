# Copyright 2021 The UmbraTek Inc. All Rights Reserved.
#
# Software License Agreement (BSD License)
#
# Author: Jimy Zhang <jimy.zhang@umbratek.com> <jimy92@163.com>
# =============================================================================
import sys
import argparse

sys.path.append("./api/")
sys.path.append("../api/")
sys.path.append("./modules_lib/")
sys.path.append("../modules_lib/")
from ubot.ubot_api_tcp import UbotApiTcp
from ubot.ubot_reg import RS485_LINE
from common import print_msg

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.description = 'ubot demo'
    parser.add_argument("--ip", help=" ", default="127.0.0.1", type=str)
    args = parser.parse_args()

    ubotapi = UbotApiTcp(args.ip)
    ret, value = ubotapi.get_motion_status()
    print("[Demo 08 ] get_motion_status :%d %d" % (ret, value))
    ret, value = ubotapi.get_error_code()
    print("[Demo 08 ] get_error_code    :%d %d %d" % (ret, value[0], value[1]))
    ret = ubotapi.reset_err()
    print("[Demo 08 ] reset_err    :%d" % (ret))
    ret = ubotapi.set_motion_enable(9, 1)
    print("[Demo 08 ] set_motion_enable :%d" % (ret))
    ret = ubotapi.set_motion_status(0)
    print("[Demo 08 ] set_motion_status :%d" % (ret))
    print(" ")

    ret = ubotapi.move_sleep(1)
    print("[Demo 08 ] move_sleep :%d" % (ret))

    tx_len = 7
    rx_len = 6
    tx_data = bytes([0xAA, 0x03, 0x02, 0xA0, 0x01, 0x24, 0x5C])
    ret, value = ubotapi.set_pass_rs485_now(RS485_LINE.TGPIO, 10, tx_len, rx_len, tx_data)
    print("[Demo 08 ] set_pass_rs485_now :%d" % (ret))
    print_msg.nhex("    ", value, rx_len + 1)

    tx_len = 7
    rx_len = 6
    tx_data = bytes([0xAA, 0x03, 0x02, 0xA1, 0x01, 0x25, 0xCC])
    ret, value = ubotapi.set_pass_rs485_now(RS485_LINE.TGPIO, 10, tx_len, rx_len, tx_data)
    print("[Demo 08 ] set_pass_rs485_now :%d" % (ret))
    print_msg.nhex("    ", value, rx_len + 1)

    tx_len = 10
    rx_len = 6
    tx_data = bytes([0xAA, 0x03, 0x05, 0xB0, 0x01, 0x31, 0x2D, 0x00, 0xF5, 0xE0])
    ret, value = ubotapi.set_pass_rs485_now(RS485_LINE.TGPIO, 10, tx_len, rx_len, tx_data)
    print("[Demo 08 ] set_pass_rs485_now :%d" % (ret))
    print_msg.nhex("    ", value, rx_len + 1)

    ret = ubotapi.move_sleep(5)
    print("[Demo 08 ] move_sleep :%d" % (ret))

    tx_len = 10
    rx_len = 6
    tx_data = bytes([0xAA, 0x03, 0x05, 0xB0, 0xFE, 0xCE, 0xD3, 0x00, 0xB5, 0xA4])
    ret, value = ubotapi.set_pass_rs485_now(RS485_LINE.TGPIO, 10, tx_len, rx_len, tx_data)
    print("[Demo 08 ] set_pass_rs485_now :%d" % (ret))
    print_msg.nhex("    ", value, rx_len + 1)

    ret = ubotapi.move_sleep(10)
    print("[Demo 08 ] move_sleep :%d" % (ret))

    tx_len = 7
    rx_len = 6
    tx_data = bytes([0xAA, 0x03, 0x02, 0xA0, 0x03, 0xA5, 0x9D])
    ret, value = ubotapi.set_pass_rs485_now(RS485_LINE.TGPIO, 10, tx_len, rx_len, tx_data)
    print("[Demo 08 ] set_pass_rs485_now :%d" % (ret))
    print_msg.nhex("    ", value, rx_len + 1)

    tx_len = 7
    rx_len = 6
    tx_data = bytes([0xAA, 0x03, 0x02, 0xA1, 0x01, 0x25, 0xCC])
    ret, value = ubotapi.set_pass_rs485_now(RS485_LINE.TGPIO, 10, tx_len, rx_len, tx_data)
    print("[Demo 08 ] set_pass_rs485_now :%d" % (ret))
    print_msg.nhex("    ", value, rx_len + 1)

    tx_len = 10
    rx_len = 6
    tx_data = bytes([0xAA, 0x03, 0x05, 0xD0, 0x00, 0x00, 0xC3, 0x50, 0x68, 0x47])
    ret, value = ubotapi.set_pass_rs485_now(RS485_LINE.TGPIO, 10, tx_len, rx_len, tx_data)
    print("[Demo 08 ] set_pass_rs485_now :%d" % (ret))
    print_msg.nhex("    ", value, rx_len + 1)
