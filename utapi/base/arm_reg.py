#!/usr/bin/env python3
#
# Copyright (C) 2020 UmbraTek Inc. All Rights Reserved.
#
# Software License Agreement (BSD License)
#
# Author: Jimy Zhang <jimy.zhang@umbratek.com> <jimy92@163.com>
# =============================================================================


class RS485_LINE:
    SERVO = 92
    TGPIO = 2
    CGPIO = 3

    def __init__(self):
        pass


class ARM_REG:
    def __init__(self, axis):
        null = 0
        AXIS = axis

        # cmd的reg  读reg发送cmd的长度  读reg接收data的长度  写reg发送cmd的长度  写reg接收data的长度
        self.UUID = [0x01, 0, 17, null, null]
        self.SW_VERSION = [0x02, 0, 20, null, null]
        self.HW_VERSION = [0x03, 0, 20, null, null]
        self.UBOT_AXIS = [0x04, 0, 1, null, null]
        self.SYS_AUTORUN = [0x0A, 0, 1, 1, 0]
        self.SYS_SHUTDOWN = [0x0B, null, null, 1, 0]
        self.RESET_ERR = [0x0C, null, null, 1, 0]
        self.SYS_REBOOT = [0x0D, null, null, 1, 0]
        self.ERASE_PARM = [0x0E, null, null, 1, 0]
        self.SAVED_PARM = [0x0F, null, null, 1, 0]

        self.MOTION_MDOE = [0x20, 0, 1, 1, 0]
        self.MOTION_ENABLE = [0x21, 0, 4, 2, 0]
        self.BRAKE_ENABLE = [0x22, 0, 4, 2, 0]
        self.ERROR_CODE = [0x23, 0, 2, null, null]
        self.SERVO_MSG = [0x24, 0, (AXIS * 2), null, null]
        self.MOTION_STATUS = [0x25, 0, 1, 1, 0]
        self.CMD_NUM = [0x26, 0, 4, 4, 0]

        self.MOVET_LINE = [0x30, null, null, 36, 4]
        self.MOVET_LINEB = [0x31, null, null, 40, 4]
        self.MOVET_CIRCLE = [0x32, null, null, 64, 4]
        self.MOVET_P2P = [0x33, null, null, 36, 4]
        self.MOVET_P2PB = [0x34, null, null, null, null]
        self.MOVEJ_LINE = [0x35, null, null, (AXIS + 3) * 4, 4]
        self.MOVEJ_LINEB = [0x36, null, null, (AXIS + 4) * 4, 4]
        self.MOVEJ_CIRCLE = [0x37, null, null, (AXIS * 2 + 4) * 4, 4]
        self.MOVEJ_P2P = [0x38, null, null, (AXIS + 3) * 4, 4]
        self.MoveJ_P2PB = [0x39, null, null, null, null]
        self.MOVEJ_HOME = [0x3A, null, null, 12, 4]
        self.MOVE_SLEEP = [0x3B, null, null, 4, 4]
        self.MOVEJ_SERVO = [0x3D, null, null, 0x55, 4]
        self.MOVET_SERVO = [0x3E, null, null, 0x55, 4]
        self.PLAN_SLEEP = [0x3F, null, null, 4, 4]

        self.TCP_JERK = [0x40, 0, 4, 4, 4]
        self.TCP_MAXACC = [0x41, 0, 4, 4, 4]
        self.JOINT_JERK = [0x42, 0, 4, 4, 4]
        self.JOINT_MAXACC = [0x43, 0, 4, 4, 4]
        self.TCP_OFFSET = [0x44, 0, 24, 24, 0]
        self.LOAD_PARAM = [0x45, 0, 16, 16, 0]
        self.GRAVITY_DIR = [0x46, 0, 12, 12, 0]
        self.COLLIS_SENS = [0x47, 0, 1, 1, 0]
        self.TEACH_SENS = [0x48, 0, 1, 1, 0]
        self.LIMIT_FUN = [0x49, 0, 4, 4, 0]

        self.TCP_POS_CURR = [0x50, 0, 24, null, null]
        self.JOINT_POS_CURR = [0x51, 0, AXIS * 4, null, null]
        self.CAL_IK = [0x52, (6 + AXIS) * 4, AXIS * 4, null, null]
        self.CAL_FK = [0x53, AXIS * 4, 24, null, null]
        self.IS_JOINT_LIMIT = [0x54, AXIS * 4, 1, null, null]
        self.IS_TCP_LIMIT = [0x55, 24, 1, null, null]
        self.JOINT_VEL_CURR = [0x56, 0, AXIS * 4, null, null]

        # [line id reg] [ret value] [line id reg value] [ret]
        self.UTRC_INT8_NOW = [0x60, 3, 2, 4, 1]
        self.UTRC_INT32_NOW = [0x61, 3, 8, 7, 1]
        self.UTRC_FP32_NOW = [0x62, 3, 8, 7, 1]
        self.UTRC_INT8N_NOW = [0x63, 4, 0x55, 0x55, 1]

        # [line id reg] [ret value] [line id reg value] [ret]
        self.UTRC_INT8_QUE = [0x64, " ", " ", 4, 0]
        self.UTRC_INT32_QUE = [0x65, " ", " ", 7, 0]
        self.UTRC_FP32_QUE = [0x66, " ", " ", 7, 0]
        self.UTRC_INT8N_QUE = [0x67, " ", " ", 0x55, 0]

        self.PASS_RS485_NOW = [0x68, " ", " ", 0x55, 0x55]
        self.PASS_RS485_QUE = [0x69, " ", " ", 0x55, 0]

        # [line id reg num] [ret value] [line id reg num value] [ret]
        self.UTRC_U8FP32_NOW = [0x6A, 4, 8, 8, 1]
        self.UTRC_FP32N_NOW = [0x6B, 4, 0x55, 0x55, 1]
        self.GPIO_IN = [0x6E, 2, 0x55, " ", " "]
        self.GPIO_OU = [0x6F, 2, 0x55, " ", " "]

        self.FRICTION = [0x70, 2, 16, 2 + 16, 0]
