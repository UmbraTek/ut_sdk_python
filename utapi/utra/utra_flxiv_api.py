# Copyright 2021 The UmbraTek Inc. All Rights Reserved.
#
# Software License Agreement (BSD License)
#
# Author: Jimy Zhang <jimy.zhang@umbratek.com> <jimy92@163.com>
# =============================================================================
from base.arm_reg import RS485_LINE
from base.servo_reg import SERVO_REG as REG
from common import hex_data


class FLXIV_REG:
    null = 0
    # cmd的reg  读reg发送cmd的长度  读reg接收data的长度  写reg发送cmd的长度  写reg接收data的长度
    SENSER1 = [0x60, 0, 16, null, null]


class UtraFlxiVApi():
    def __init__(self, utra_api, id=102):
        self.DB_FLG = '[UtraFlxiVApi] '
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

    ############################################################
    #                       Control Api
    ############################################################

    def set_motion_mode(self, value, now=True):
        if now:
            return self.utra.set_utrc_int8_now(self.line, self.id, REG.MOTION_MDOE[0], value)
        else:
            return self.utra.set_utrc_int8_que(self.line, self.id, REG.MOTION_MDOE[0], value)

    def get_motion_mode(self):
        return self.utra.get_utrc_int8_now(self.line, self.id, REG.MOTION_MDOE[0])

    def set_motion_enable(self, value, now=True):
        if now:
            return self.utra.set_utrc_int8_now(self.line, self.id, REG.MOTION_ENABLE[0], value)
        else:
            return self.utra.set_utrc_int8_que(self.line, self.id, REG.MOTION_ENABLE[0], value)

    def get_motion_enable(self):
        return self.utra.get_utrc_int8_now(self.line, self.id, REG.MOTION_ENABLE[0])

    def get_temp_motor(self):
        return self.utra.get_utrc_float_now(self.line, self.id, REG.TEMP_MOTOR[0])

    def get_temp_driver(self):
        return self.utra.get_utrc_float_now(self.line, self.id, REG.TEMP_DRIVER[0])

    def get_bus_volt(self):
        return self.utra.get_utrc_float_now(self.line, self.id, REG.BUS_VOLT[0])

    def get_error_code(self):
        return self.utra.get_utrc_int8_now(self.line, self.id, REG.ERROR_CODE[0])

    ############################################################
    #                       Senser Api
    ############################################################

    def get_senser(self):
        return self.utra.get_utrc_nfloat_now(self.line, self.id, FLXIV_REG.SENSER1[0], 4)
