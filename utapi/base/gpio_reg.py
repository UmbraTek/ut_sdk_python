#!/usr/bin/env python3
#
# Copyright (C) 2020 UmbraTek Inc. All Rights Reserved.
#
# Software License Agreement (BSD License)
#
# Author: Jimy Zhang <jimy.zhang@umbratek.com> <jimy92@163.com>
# =============================================================================


class GPIO_REG:
    null = 0
    digitin_num = 0
    digitou_num = 0
    analogin_num = 0
    analogou_num = 0

    # cmd的reg  读reg发送cmd的长度  读reg接收data的长度  写reg发送cmd的长度  写reg接收data的长度
    UUID = [0x01, 0, 12, null, null]
    SW_VERSION = [0x02, 0, 12, null, null]
    HW_VERSION = [0x03, 0, 12, null, null]
    GPIO_NUM = [0x04, 0, 4, null, null]

    COM_ID = [0x08, null, null, 1, 0]
    COM_BAUD = [0x09, null, null, 4, 0]
    RESET_ERR = [0x0C, null, null, 1, 0]
    REBOOT_DRIVER = [0x0D, null, null, 1, 0]
    ERASE_PARM = [0x0E, null, null, 1, 0]
    SAVED_PARM = [0x0F, null, null, 1, 0]

    FUNCTRL = [0x10, 0, 4, 4, 0]
    FUNGPIO = [0x11, 0, 4, 4, 0]
    DIGITIN = [0x12, 0, 4, 4, 0]
    DIGITOU = [0x13, 0, 4, 4, 0]
    TEMP_LIMIT = [0x18, 0, 2, 2, 0]
    VOLT_LIMIT = [0x19, 0, 2, 2, 0]
    CURR_LIMIT = [0x1A, 0, 4, 4, 0]

    TEMP_DRIVER = [0x28, 0, 4, null, null]
    BUS_VOLT = [0x2A, 0, 4, null, null]
    BUS_CURR = [0x2B, 0, 4, null, null]
    ERROR_CODE = [0x2F, 0, 1, null, null]

    # GETFRAME1 = [0x40, 0, (1 + 2 + analogin_num) * 4, null, null]
    # SETFRAME2 = [0x41, null, null, (1 + 2 + analogou_num) * 4, 0]

    FRAME_IN = [0x60, 0, 0x55, null, null]
    FRAME_OU = [0x61, 0, 0x55, 0x55, 0]

    SAVED_PROD = [0x78, null, null, 1, 0]
    INTO_BOOT = [0x7A, null, null, 1, 0]
    BOOT_ING = [0x7F, null, null, 7, 1]
    BOOT_END = [0x7F, null, null, 1, 1]
