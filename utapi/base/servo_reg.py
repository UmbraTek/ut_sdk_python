# Copyright 2020 The UmbraTek Inc. All Rights Reserved.
#
# Software License Agreement (BSD License)
#
# Author: Jimy Zhang <jimy.zhang@umbratek.com> <jimy92@163.com>
# =============================================================================


class SERVO_REG:
    null = 0

    # cmd的reg  读reg发送cmd的长度  读reg接收data的长度  写reg发送cmd的长度  写reg接收data的长度
    UUID = [0x01, 0, 12, null, null]
    SW_VERSION = [0x02, 0, 12, null, null]
    HW_VERSION = [0x03, 0, 12, null, null]
    MULTI_VERSION = [0x04, 0, 12, null, null]
    MECH_RATIO = [0x05, 0, 4, 4, 0]
    COM_ID = [0x08, null, null, 1, 0]
    COM_BAUD = [0x09, null, null, 4, 0]
    RESET_ERR = [0x0C, null, null, 1, 0]
    REBOOT_DRIVER = [0x0D, null, null, 1, 0]
    ERASE_PARM = [0x0E, null, null, 1, 0]
    SAVED_PARM = [0x0F, null, null, 1, 0]

    ELEC_RATIO = [0x10, 0, 4, 4, 0]
    MOTION_DIR = [0x11, 0, 1, 1, 0]
    TEMP_LIMIT = [0x18, 0, 2, 2, 0]
    VOLT_LIMIT = [0x19, 0, 2, 2, 0]
    CURR_LIMIT = [0x1A, 0, 4, 4, 0]
    BRAKE_PWM = [0x1F, 0, 1, 1, 0]

    MOTION_MDOE = [0x20, 0, 1, 1, 0]
    MOTION_ENABLE = [0x21, 0, 1, 1, 0]
    BRAKE_ENABLE = [0x22, 0, 1, 1, 0]
    TEMP_DRIVER = [0x28, 0, 4, null, null]
    TEMP_MOTOR = [0x29, 0, 4, null, null]
    BUS_VOLT = [0x2A, 0, 4, null, null]
    BUS_CURR = [0x2B, 0, 4, null, null]
    MULTI_VOLT = [0x2C, 0, 4, null, null]
    ERROR_CODE = [0x2F, 0, 1, null, null]

    POS_TARGET = [0x30, 0, 4, 4, 0]
    POS_CURRENT = [0x31, 0, 4, null, null]
    POS_LIMIT_MIN = [0x32, 0, 4, 4, 0]
    POS_LIMIT_MAX = [0x33, 0, 4, 4, 0]
    POS_LIMIT_DIFF = [0x34, 0, 4, 4, 0]
    POS_PIDP = [0x35, 0, 4, 4, 0]
    POS_SMOOTH_CYC = [0x36, 0, 1, 1, 0]
    POS_CAL_ZERO = [0x3F, null, null, 1, 0]

    VEL_TARGET = [0x40, 0, 4, 4, 0]
    VEL_CURRENT = [0x41, 0, 4, null, null]
    VEL_LIMIT_MIN = [0x42, 0, 4, 4, 0]
    VEL_LIMIT_MAX = [0x43, 0, 4, 4, 0]
    VEL_LIMIT_DIFF = [0x44, 0, 4, 4, 0]
    VEL_PIDP = [0x45, 0, 4, 4, 0]
    VEL_PIDI = [0x46, 0, 4, 4, 0]
    VEL_SMOOTH_CYC = [0x47, 0, 1, 1, 0]

    TAU_TARGET = [0x50, 0, 4, 4, 0]
    TAU_CURRENT = [0x51, 0, 4, null, null]
    TAU_LIMIT_MIN = [0x52, 0, 4, 4, 0]
    TAU_LIMIT_MAX = [0x53, 0, 4, 4, 0]
    TAU_LIMIT_DIFF = [0x54, 0, 4, 4, 0]
    TAU_PIDP = [0x55, 0, 4, 4, 0]
    TAU_PIDI = [0x56, 0, 4, 4, 0]
    TAU_SMOOTH_CYC = [0x57, 0, 1, 1, 0]


def rad_to_int(a):
    return int(a * 100000)


def int_to_rad(a):
    return float(a) * 0.00001
