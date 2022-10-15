#!/usr/bin/env python3
#
# Copyright (C) 2020 UmbraTek Inc. All Rights Reserved.
#
# Software License Agreement (BSD License)
#
# Author: Jimy Zhang <jimy.zhang@umbratek.com> <jimy92@163.com>
# =============================================================================
from utapi.base.arm_reg import RS485_LINE
from utapi.base.servo_reg import SERVO_REG as REG
from utapi.common import hex_data


class FLXIE_REG:
    null = 0
    UNLOCK_FUN = [0x22, 0, 1, 1, 0]
    SENSER1 = [0x60, 0, 16, null, null]


class UtraFlxiE2Api():
    def __init__(self, utra_api, id=101):
        u"""Please refer to utapi/flxie/flxie2_api_base.py for the manual.
        The function is the same, but this class is controlled through the transmission of the robot arm.

        Args:
            utra_api (_type_): The control class of the manipulator
            id (int, optional): The id number of FLXI E. Defaults to 101.
        """
        self.DB_FLG = '[UtraFlxiE2Api] '
        self.__is_err = 0
        self.utra = utra_api
        self.id = id
        self.line = RS485_LINE.TGPIO

    ############################################################
    #                       Basic Api
    ############################################################

    def get_uuid(self):
        ret, uuid = self.utra.get_utrc_int8n_now(self.line, self.id, REG.UUID[0], REG.UUID[2])
        uuid_str = ''
        for i in uuid:
            uuid_str += '{0:0>2}'.format(str(hex(i))[2:])
        return ret, uuid_str

    def get_sw_version(self):
        ret, version = self.utra.get_utrc_int8n_now(self.line, self.id, REG.SW_VERSION[0], REG.SW_VERSION[2])
        version = ''.join(chr(i) for i in version)
        return ret, version

    def get_hw_version(self):
        ret, version = self.utra.get_utrc_int8n_now(self.line, self.id, REG.HW_VERSION[0], REG.HW_VERSION[2])
        ver_str = ''
        for i in version:
            ver_str += '{0:0>2}'.format(str(hex(i))[2:])
        return ret, ver_str

    def reset_err(self):
        return self.utra.set_utrc_int8_now(self.line, self.id, REG.RESET_ERR[0], REG.RESET_ERR[0])

    def restart_driver(self):
        return self.utra.set_utrc_int8_now(self.line, self.id, REG.REBOOT_DRIVER[0], REG.REBOOT_DRIVER[0])

    def erase_parm(self):
        return self.utra.set_utrc_int8_now(self.line, self.id, REG.ERASE_PARM[0], REG.ERASE_PARM[0])

    def saved_parm(self):
        return self.utra.set_utrc_int8_now(self.line, self.id, REG.SAVED_PARM[0], REG.SAVED_PARM[0])

    ############################################################
    #                       Ectension Api
    ############################################################

    def get_temp_limit(self):
        ret, value = self.utra.get_utrc_int8n_now(self.line, self.id, REG.TEMP_LIMIT[0], REG.TEMP_LIMIT[2])
        value[0] = hex_data.bytes_to_int8(value[0])
        value[1] = hex_data.bytes_to_int8(value[1])
        return ret, value

    def set_temp_limit(self, min, max, now=True):
        txdata = hex_data.int8_to_bytes_big(int(min))
        txdata += hex_data.int8_to_bytes_big(int(max))
        if now:
            return self.utra.set_utrc_int8n_now(self.line, self.id, REG.TEMP_LIMIT[0], REG.TEMP_LIMIT[3], txdata)
        else:
            return self.utra.set_utrc_int8n_que(self.line, self.id, REG.TEMP_LIMIT[0], REG.TEMP_LIMIT[3], txdata)

    def get_volt_limit(self):
        ret, value = self.utra.get_utrc_int8n_now(self.line, self.id, REG.VOLT_LIMIT[0], REG.VOLT_LIMIT[2])
        value[0] = hex_data.bytes_to_int8(value[0])
        value[1] = hex_data.bytes_to_int8(value[1])
        return ret, value

    def set_volt_limit(self, min, max, now=True):
        txdata = hex_data.int8_to_bytes_big(int(min))
        txdata += hex_data.int8_to_bytes_big(int(max))
        if now:
            return self.utra.set_utrc_int8n_now(self.line, self.id, REG.VOLT_LIMIT[0], REG.VOLT_LIMIT[3], txdata)
        else:
            return self.utra.set_utrc_int8n_que(self.line, self.id, REG.VOLT_LIMIT[0], REG.VOLT_LIMIT[3], txdata)

    def get_curr_limit(self):
        return self.utra.get_utrc_float_now(self.line, self.id, REG.CURR_LIMIT[0])

    def set_curr_limit(self, value, now=True):
        if now:
            return self.utra.set_utrc_float_now(self.line, self.id, REG.CURR_LIMIT[0], value)
        else:
            return self.utra.set_utrc_float_que(self.line, self.id, REG.CURR_LIMIT[0], value)

    ############################################################
    #                       Control Api
    ############################################################

    def set_motion_mode(self, value, now=True):
        if now:
            return self.utra.set_utrc_int8_now(self.line, self.id, REG.MOTION_MDOE[0], value)
        else:
            return self.utra.set_utrc_int8_que(self.line, self.id, REG.MOTION_MDOE[0], value)

    def into_motion_mode_pos(self, now=True):
        return self.set_motion_mode(1, now)

    def into_motion_mode_vel(self, now=True):
        return self.set_motion_mode(2, now)

    def into_motion_mode_tau(self, now=True):
        return self.set_motion_mode(3, now)

    def get_motion_mode(self):
        return self.utra.get_utrc_int8_now(self.line, self.id, REG.MOTION_MDOE[0])

    def set_motion_enable(self, value, now=True):
        if now:
            return self.utra.set_utrc_int8_now(self.line, self.id, REG.MOTION_ENABLE[0], value)
        else:
            return self.utra.set_utrc_int8_que(self.line, self.id, REG.MOTION_ENABLE[0], value)

    def into_motion_enable(self, now=True):
        return self.set_motion_enable(1, now)

    def into_motion_disable(self, now=True):
        return self.set_motion_enable(0, now)

    def get_motion_enable(self):
        return self.utra.get_utrc_int8_now(self.line, self.id, REG.MOTION_ENABLE[0])

    def set_unlock_function(self, value):
        return self.utra.set_utrc_int8_now(self.line, self.id, FLXIE_REG.UNLOCK_FUN[0], value)

    def get_temp_motor(self):
        return self.utra.get_utrc_float_now(self.line, self.id, REG.TEMP_MOTOR[0])

    def get_temp_driver(self):
        return self.utra.get_utrc_float_now(self.line, self.id, REG.TEMP_DRIVER[0])

    def get_bus_volt(self):
        return self.utra.get_utrc_float_now(self.line, self.id, REG.BUS_VOLT[0])

    def get_bus_curr(self):
        return self.utra.get_utrc_float_now(self.line, self.id, REG.BUS_CURR[0])

    def get_error_code(self):
        return self.utra.get_utrc_int8_now(self.line, self.id, REG.ERROR_CODE[0])

    ############################################################
    #                       Position Api
    ############################################################

    def get_pos_target(self):
        return self.utra.get_utrc_float_now(self.line, self.id, REG.POS_TARGET[0])

    def set_pos_target(self, value, now=True):
        if now:
            return self.utra.set_utrc_float_now(self.line, self.id, REG.POS_TARGET[0], value)
        else:
            return self.utra.set_utrc_float_que(self.line, self.id, REG.POS_TARGET[0], value)

    def get_pos_current(self):
        return self.utra.get_utrc_float_now(self.line, self.id, REG.POS_CURRENT[0])

    def get_pos_pidp(self):
        return self.utra.get_utrc_float_now(self.line, self.id, REG.POS_PIDP[0])

    def set_pos_pidp(self, pid, now=True):
        if now:
            return self.utra.set_utrc_float_now(self.line, self.id, REG.POS_PIDP[0], pid)
        else:
            return self.utra.set_utrc_float_que(self.line, self.id, REG.POS_PIDP[0], pid)

    def get_pos_smooth_cyc(self):
        return self.utra.get_utrc_int8_now(self.line, self.id, REG.POS_SMOOTH_CYC[0])

    def set_pos_smooth_cyc(self, value, now=True):
        if now:
            return self.utra.set_utrc_int8_now(self.line, self.id, REG.POS_SMOOTH_CYC[0], value)
        else:
            return self.utra.set_utrc_int8_que(self.line, self.id, REG.POS_SMOOTH_CYC[0], value)

    def get_pos_adrc_param(self, i):
        return self.utra.get_utrc_u8float_now(self.line, self.id, REG.POS_ADRC_PARAM[0], i)

    def set_pos_adrc_param(self, i, value):
        return self.utra.set_utrc_u8float_now(self.line, self.id, REG.POS_ADRC_PARAM[0], i, value)

    def pos_cal_zero(self):
        return self.utra.set_utrc_int8_now(self.line, self.id, REG.POS_CAL_ZERO[0], REG.POS_CAL_ZERO[0])

    ############################################################
    #                       Speed Api
    ############################################################

    def get_vel_limit_min(self):
        return self.utra.get_utrc_float_now(self.line, self.id, REG.VEL_LIMIT_MIN[0])

    def set_vel_limit_min(self, vel, now=True):
        if now:
            return self.utra.set_utrc_float_now(self.line, self.id, REG.VEL_LIMIT_MIN[0], vel)
        else:
            return self.utra.set_utrc_float_que(self.line, self.id, REG.VEL_LIMIT_MIN[0], vel)

    def get_vel_limit_max(self):
        return self.utra.get_utrc_float_now(self.line, self.id, REG.VEL_LIMIT_MAX[0])

    def set_vel_limit_max(self, vel, now=True):
        if now:
            return self.utra.set_utrc_float_now(self.line, self.id, REG.VEL_LIMIT_MAX[0], vel)
        else:
            return self.utra.set_utrc_float_que(self.line, self.id, REG.VEL_LIMIT_MAX[0], vel)

    ############################################################
    #                       Current Api
    ############################################################

    def get_tau_target(self):
        return self.utra.get_utrc_float_now(self.line, self.id, REG.TAU_TARGET[0])

    def set_tau_target(self, tau, now=True):
        if now:
            return self.utra.set_utrc_float_now(self.line, self.id, REG.TAU_TARGET[0], tau)
        else:
            return self.utra.set_utrc_float_que(self.line, self.id, REG.TAU_TARGET[0], tau)

    def get_tau_current(self):
        return self.utra.get_utrc_float_now(self.line, self.id, REG.TAU_CURRENT[0])

    def get_tau_limit_min(self):
        return self.utra.get_utrc_float_now(self.line, self.id, REG.TAU_LIMIT_MIN[0])

    def set_tau_limit_min(self, tau, now=True):
        if now:
            return self.utra.set_utrc_float_now(self.line, self.id, REG.TAU_LIMIT_MIN[0], tau)
        else:
            return self.utra.set_utrc_float_que(self.line, self.id, REG.TAU_LIMIT_MIN[0], tau)

    def get_tau_limit_max(self):
        return self.utra.get_utrc_float_now(self.line, self.id, REG.TAU_LIMIT_MAX[0])

    def set_tau_limit_max(self, tau, now=True):
        if now:
            return self.utra.set_utrc_float_now(self.line, self.id, REG.TAU_LIMIT_MAX[0], tau)
        else:
            return self.utra.set_utrc_float_que(self.line, self.id, REG.TAU_LIMIT_MAX[0], tau)

    def get_tau_pidp(self):
        return self.utra.get_utrc_float_now(self.line, self.id, REG.TAU_PIDP[0])

    def set_tau_pidp(self, pid_p, now=True):
        if now:
            return self.utra.set_utrc_float_now(self.line, self.id, REG.TAU_PIDP[0], pid_p)
        else:
            return self.utra.set_utrc_float_que(self.line, self.id, REG.TAU_PIDP[0], pid_p)

    def get_tau_pidi(self):
        return self.utra.get_utrc_float_now(self.line, self.id, REG.TAU_PIDI[0])

    def set_tau_pidi(self, pid_i, now=True):
        if now:
            return self.utra.set_utrc_float_now(self.line, self.id, REG.TAU_PIDI[0], pid_i)
        else:
            return self.utra.set_utrc_float_que(self.line, self.id, REG.TAU_PIDI[0], pid_i)

    def get_tau_smooth_cyc(self):
        return self.utra.get_utrc_int8_now(self.line, self.id, REG.TAU_SMOOTH_CYC[0])

    def set_tau_smooth_cyc(self, value, now=True):
        if now:
            return self.utra.set_utrc_int8_now(self.line, self.id, REG.TAU_SMOOTH_CYC[0], value)
        else:
            return self.utra.set_utrc_int8_que(self.line, self.id, REG.TAU_SMOOTH_CYC[0], value)

    def get_tau_adrc_param(self, i):
        return self.utra.get_utrc_u8float_now(self.line, self.id, REG.TAU_ADRC_PARAM[0], i)

    def set_tau_adrc_param(self, i, value):
        return self.utra.set_utrc_u8float_now(self.line, self.id, REG.TAU_ADRC_PARAM[0], i, value)

    ############################################################
    #                       Senser Api
    ############################################################

    def get_senser(self):
        return self.utra.get_utrc_nfloat_now(self.line, self.id, FLXIE_REG.SENSER1[0], 4)
