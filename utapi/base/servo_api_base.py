# Copyright 2020 The UmbraTek Inc. All Rights Reserved.
#
# Software License Agreement (BSD License)
#
# Author: Jimy Zhang <jimy.zhang@umbratek.com> <jimy92@163.com>
# =============================================================================
from common.utrc import UTRC_RW
from common import hex_data
from base.servo_reg import SERVO_REG, rad_to_int, int_to_rad


class _ServoApiBase():
    def __init__(self, socket_fp, bus_client, tx_data):
        self.DB_FLG = '[AdraApiB] '
        self.socket_fp = socket_fp
        self.bus_client = bus_client
        self.tx_data = tx_data
        self.__is_err = 0

        id = 1
        self.id = id
        self.virid = id

    def _close(self):
        if self.socket_fp:
            self.socket_fp.close()

    def _connect_to_id(self, id, virtual_id=0):
        self.id = int(id)
        self.virid = int(virtual_id)
        self.tx_data.id = self.id
        self.tx_data.slave_id = self.id

    def __send(self, rw, cmd, cmd_data, len_tx=0):
        if self.__is_err:
            return 0

        if rw == UTRC_RW.R:
            data_wlen = cmd[1]
        else:
            data_wlen = cmd[3]
        if len_tx != 0:
            data_wlen = len_tx

        self.tx_data.rw = rw
        self.tx_data.cmd = cmd[0]
        self.tx_data.len = data_wlen + 1

        for i in range(data_wlen):
            self.tx_data.data[i] = cmd_data[i]

        # self.tx_data.print_pack()
        self.bus_client.send(self.tx_data)

    def __pend(self, rw, cmd, timeout_s=1):
        if self.__is_err:
            return -999, self.tx_data

        if rw == UTRC_RW.R:
            data_rlen = cmd[2]
        else:
            data_rlen = cmd[4]
        return self.bus_client.pend(self.tx_data, data_rlen, timeout_s)

    def is_err(self):
        return self.__is_err

############################################################
#                       Basic Api
############################################################

    def _get_uuid(self):
        self.__send(UTRC_RW.R, SERVO_REG.UUID, None)
        ret, bus_rmsg = self.__pend(UTRC_RW.R, SERVO_REG.UUID)
        uuid = bus_rmsg.data[0:12]
        string = ''
        for i in uuid:
            string += '{0:0>2}'.format(str(hex(i))[2:])
        return ret, string

    def _get_sw_version(self):
        self.__send(UTRC_RW.R, SERVO_REG.SW_VERSION, None)
        ret, bus_rmsg = self.__pend(UTRC_RW.R, SERVO_REG.SW_VERSION)
        version = bus_rmsg.data[0:12]
        version = ''.join(chr(i) for i in version)
        return ret, version

    def _get_hw_version(self):
        self.__send(UTRC_RW.R, SERVO_REG.HW_VERSION, None)
        ret, bus_rmsg = self.__pend(UTRC_RW.R, SERVO_REG.HW_VERSION)
        version = bus_rmsg.data[0:12]
        string = ''
        for i in version:
            string += '{0:0>2}'.format(str(hex(i))[2:])
        return ret, string

    def _get_multi_version(self):
        self.__send(UTRC_RW.R, SERVO_REG.MULTI_VERSION, None)
        ret, bus_rmsg = self.__pend(UTRC_RW.R, SERVO_REG.MULTI_VERSION)
        version = hex_data.bytes_to_int32_big(bus_rmsg.data[0:4])
        version = "0000000000" + str(version)
        return ret, version[len(version) - 12:len(version)]

    def _get_mech_ratio(self):
        self.__send(UTRC_RW.R, SERVO_REG.MECH_RATIO, None)
        ret, bus_rmsg = self.__pend(UTRC_RW.R, SERVO_REG.MECH_RATIO)
        ratio = hex_data.bytes_to_int32_big(bus_rmsg.data[0:4])
        ratio = int_to_rad(ratio)
        return ret, ratio

    def _set_mech_ratio(self, ratio):
        ratio = rad_to_int(ratio)
        txdata = hex_data.int32_to_bytes_big(ratio)
        self.__send(UTRC_RW.W, SERVO_REG.MECH_RATIO, txdata)
        ret, bus_rmsg = self.__pend(UTRC_RW.W, SERVO_REG.MECH_RATIO)
        return ret

    def _set_com_id(self, id):
        txdata = [0]
        txdata[0] = int(id)
        self.__send(UTRC_RW.W, SERVO_REG.COM_ID, txdata)
        ret, bus_rmsg = self.__pend(UTRC_RW.W, SERVO_REG.COM_ID)
        return ret

    def _set_com_baud(self, baud):
        txdata = hex_data.int32_to_bytes_big(int(baud))
        self.__send(UTRC_RW.W, SERVO_REG.COM_BAUD, txdata)
        ret, bus_rmsg = self.__pend(UTRC_RW.W, SERVO_REG.COM_BAUD)
        return ret

    def _reset_err(self):
        txdata = [0]
        txdata[0] = SERVO_REG.RESET_ERR[0]
        self.__send(UTRC_RW.W, SERVO_REG.RESET_ERR, txdata)
        ret, bus_rmsg = self.__pend(UTRC_RW.W, SERVO_REG.RESET_ERR)
        return ret

    def _restart_driver(self):
        txdata = [0]
        txdata[0] = SERVO_REG.REBOOT_DRIVER[0]
        self.__send(UTRC_RW.W, SERVO_REG.REBOOT_DRIVER, txdata)
        ret, bus_rmsg = self.__pend(UTRC_RW.W, SERVO_REG.REBOOT_DRIVER)
        return ret

    def _erase_parm(self):
        txdata = [0]
        txdata[0] = SERVO_REG.ERASE_PARM[0]
        self.__send(UTRC_RW.W, SERVO_REG.ERASE_PARM, txdata)
        ret, bus_rmsg = self.__pend(UTRC_RW.W, SERVO_REG.ERASE_PARM, 3)
        return ret

    def _saved_parm(self):
        txdata = [0]
        txdata[0] = SERVO_REG.SAVED_PARM[0]
        self.__send(UTRC_RW.W, SERVO_REG.SAVED_PARM, txdata)
        ret, bus_rmsg = self.__pend(UTRC_RW.W, SERVO_REG.SAVED_PARM, 3)
        return ret

############################################################
#                       Ectension Api
############################################################

    def _get_elec_ratio(self):
        self.__send(UTRC_RW.R, SERVO_REG.ELEC_RATIO, None)
        ret, bus_rmsg = self.__pend(UTRC_RW.R, SERVO_REG.ELEC_RATIO)
        ratio = hex_data.bytes_to_int32_big(bus_rmsg.data[0:4])
        ratio = int_to_rad(ratio)
        return ret, ratio

    def _set_elec_ratio(self, ratio):
        ratio = rad_to_int(ratio)
        txdata = hex_data.int32_to_bytes_big(ratio)
        self.__send(UTRC_RW.W, SERVO_REG.ELEC_RATIO, txdata)
        ret, bus_rmsg = self.__pend(UTRC_RW.W, SERVO_REG.ELEC_RATIO)
        return ret

    def _get_motion_dir(self):
        self.__send(UTRC_RW.R, SERVO_REG.MOTION_DIR, None)
        ret, bus_rmsg = self.__pend(UTRC_RW.R, SERVO_REG.MOTION_DIR)
        dir = hex_data.bytes_to_int8(bus_rmsg.data[0])
        return ret, dir

    def _set_motion_dir(self, dir):
        txdata = [0]
        txdata[0] = int(dir)
        self.__send(UTRC_RW.W, SERVO_REG.MOTION_DIR, txdata)
        ret, bus_rmsg = self.__pend(UTRC_RW.W, SERVO_REG.MOTION_DIR)
        return ret

    def _get_temp_limit(self):
        self.__send(UTRC_RW.R, SERVO_REG.TEMP_LIMIT, None)
        ret, bus_rmsg = self.__pend(UTRC_RW.R, SERVO_REG.TEMP_LIMIT)
        min = hex_data.bytes_to_int8(bus_rmsg.data[0])
        max = hex_data.bytes_to_int8(bus_rmsg.data[1])
        return ret, min, max

    def _set_temp_limit(self, min, max):
        txdata = hex_data.int8_to_bytes_big(int(min))
        txdata += hex_data.int8_to_bytes_big(int(max))
        self.__send(UTRC_RW.W, SERVO_REG.TEMP_LIMIT, txdata)
        ret, bus_rmsg = self.__pend(UTRC_RW.W, SERVO_REG.TEMP_LIMIT)
        return ret

    def _get_volt_limit(self):
        self.__send(UTRC_RW.R, SERVO_REG.VOLT_LIMIT, None)
        ret, bus_rmsg = self.__pend(UTRC_RW.R, SERVO_REG.VOLT_LIMIT)
        min = hex_data.bytes_to_int8(bus_rmsg.data[0])
        max = hex_data.bytes_to_int8(bus_rmsg.data[1])
        return ret, min, max

    def _set_volt_limit(self, min, max):
        txdata = hex_data.int8_to_bytes_big(int(min))
        txdata += hex_data.int8_to_bytes_big(int(max))
        self.__send(UTRC_RW.W, SERVO_REG.VOLT_LIMIT, txdata)
        ret, bus_rmsg = self.__pend(UTRC_RW.W, SERVO_REG.VOLT_LIMIT)
        return ret

    def _get_curr_limit(self):
        self.__send(UTRC_RW.R, SERVO_REG.CURR_LIMIT, None)
        ret, bus_rmsg = self.__pend(UTRC_RW.R, SERVO_REG.CURR_LIMIT)
        value = hex_data.bytes_to_int32_big(bus_rmsg.data[0:4])
        value = int_to_rad(value)
        return ret, value

    def _set_curr_limit(self, value):
        value = rad_to_int(value)
        txdata = hex_data.int32_to_bytes_big(value)
        self.__send(UTRC_RW.W, SERVO_REG.CURR_LIMIT, txdata)
        ret, bus_rmsg = self.__pend(UTRC_RW.W, SERVO_REG.CURR_LIMIT)
        return ret

    def _get_brake_pwm(self):
        self.__send(UTRC_RW.R, SERVO_REG.BRAKE_PWM, None)
        ret, bus_rmsg = self.__pend(UTRC_RW.R, SERVO_REG.BRAKE_PWM)
        brake_pwm = hex_data.bytes_to_int8(bus_rmsg.data[0])
        return ret, brake_pwm

    def _set_brake_pwm(self, brake_pwm):
        txdata = [0]
        txdata[0] = int(brake_pwm)
        self.__send(UTRC_RW.W, SERVO_REG.BRAKE_PWM, txdata)
        ret, bus_rmsg = self.__pend(UTRC_RW.W, SERVO_REG.BRAKE_PWM)
        return ret

############################################################
#                       Control Api
############################################################

    def _get_motion_mode(self):
        self.__send(UTRC_RW.R, SERVO_REG.MOTION_MDOE, None)
        ret, bus_rmsg = self.__pend(UTRC_RW.R, SERVO_REG.MOTION_MDOE)
        return ret, bus_rmsg.data[0]

    def _set_motion_mode(self, mode):
        txdata = [0]
        txdata[0] = int(mode)
        self.__send(UTRC_RW.W, SERVO_REG.MOTION_MDOE, txdata)
        ret, bus_rmsg = self.__pend(UTRC_RW.W, SERVO_REG.MOTION_MDOE)
        return ret

    def _get_motion_enable(self):
        self.__send(UTRC_RW.R, SERVO_REG.MOTION_ENABLE, None)
        ret, bus_rmsg = self.__pend(UTRC_RW.R, SERVO_REG.MOTION_ENABLE)
        return ret, bus_rmsg.data[0]

    def _set_motion_enable(self, enable):
        txdata = [0]
        txdata[0] = int(enable)
        self.__send(UTRC_RW.W, SERVO_REG.MOTION_ENABLE, txdata)
        ret, bus_rmsg = self.__pend(UTRC_RW.W, SERVO_REG.MOTION_ENABLE)
        return ret

    def _get_brake_enable(self):
        self.__send(UTRC_RW.R, SERVO_REG.BRAKE_ENABLE, None)
        ret, bus_rmsg = self.__pend(UTRC_RW.R, SERVO_REG.BRAKE_ENABLE)
        return ret, bus_rmsg.data[0]

    def _set_brake_enable(self, able):
        txdata = [0]
        txdata[0] = int(able)
        self.__send(UTRC_RW.W, SERVO_REG.BRAKE_ENABLE, txdata)
        ret, bus_rmsg = self.__pend(UTRC_RW.W, SERVO_REG.BRAKE_ENABLE)
        return ret

    def _get_temp_driver(self):
        self.__send(UTRC_RW.R, SERVO_REG.TEMP_DRIVER, None)
        ret, bus_rmsg = self.__pend(UTRC_RW.R, SERVO_REG.TEMP_DRIVER)
        temp = hex_data.bytes_to_int32_big(bus_rmsg.data[0:4])
        return ret, int_to_rad(temp)

    def _get_temp_motor(self):
        self.__send(UTRC_RW.R, SERVO_REG.TEMP_MOTOR, None)
        ret, bus_rmsg = self.__pend(UTRC_RW.R, SERVO_REG.TEMP_MOTOR)
        temp = hex_data.bytes_to_int32_big(bus_rmsg.data[0:4])
        return ret, int_to_rad(temp)

    def _get_bus_volt(self):
        self.__send(UTRC_RW.R, SERVO_REG.BUS_VOLT, None)
        ret, bus_rmsg = self.__pend(UTRC_RW.R, SERVO_REG.BUS_VOLT)
        volt = hex_data.bytes_to_int32_big(bus_rmsg.data[0:4])
        return ret, int_to_rad(volt)

    def _get_bus_curr(self):
        self.__send(UTRC_RW.R, SERVO_REG.BUS_CURR, None)
        ret, bus_rmsg = self.__pend(UTRC_RW.R, SERVO_REG.BUS_CURR)
        current = hex_data.bytes_to_int32_big(bus_rmsg.data[0:4])
        return ret, int_to_rad(current)

    def _get_multi_volt(self):
        self.__send(UTRC_RW.R, SERVO_REG.MULTI_VOLT, None)
        ret, bus_rmsg = self.__pend(UTRC_RW.R, SERVO_REG.MULTI_VOLT)
        volt = hex_data.bytes_to_int32_big(bus_rmsg.data[0:4])
        volt = int_to_rad(volt)
        return ret, volt

    def _get_error_code(self):
        self.__send(UTRC_RW.R, SERVO_REG.ERROR_CODE, None)
        ret, bus_rmsg = self.__pend(UTRC_RW.R, SERVO_REG.ERROR_CODE)
        return ret, hex_data.bytes_to_int8(bus_rmsg.data[0])

############################################################
#                       Position Api
############################################################

    def _get_pos_target(self):
        self.__send(UTRC_RW.R, SERVO_REG.POS_TARGET, None)
        ret, bus_rmsg = self.__pend(UTRC_RW.R, SERVO_REG.POS_TARGET)
        pos = hex_data.bytes_to_int32_big(bus_rmsg.data[0:4])
        pos = int_to_rad(pos)
        return ret, pos

    def _set_pos_target(self, pos):
        pos = rad_to_int(pos)
        txdata = hex_data.int32_to_bytes_big(pos)
        self.__send(UTRC_RW.W, SERVO_REG.POS_TARGET, txdata)
        ret, bus_rmsg = self.__pend(UTRC_RW.W, SERVO_REG.POS_TARGET)
        return ret

    def _get_pos_current(self):
        self.__send(UTRC_RW.R, SERVO_REG.POS_CURRENT, None)
        ret, bus_rmsg = self.__pend(UTRC_RW.R, SERVO_REG.POS_CURRENT)
        pos = hex_data.bytes_to_int32_big(bus_rmsg.data[0:4])
        pos = int_to_rad(pos)
        return ret, pos

    def _get_pos_limit_min(self):
        self.__send(UTRC_RW.R, SERVO_REG.POS_LIMIT_MIN, None)
        ret, bus_rmsg = self.__pend(UTRC_RW.R, SERVO_REG.POS_LIMIT_MIN)
        pos = hex_data.bytes_to_int32_big(bus_rmsg.data[0:4])
        pos = int_to_rad(pos)
        return ret, pos

    def _set_pos_limit_min(self, pos):
        pos = rad_to_int(pos)
        txdata = hex_data.int32_to_bytes_big(pos)
        self.__send(UTRC_RW.W, SERVO_REG.POS_LIMIT_MIN, txdata)
        ret, bus_rmsg = self.__pend(UTRC_RW.W, SERVO_REG.POS_LIMIT_MIN)
        return ret

    def _get_pos_limit_max(self):
        self.__send(UTRC_RW.R, SERVO_REG.POS_LIMIT_MAX, None)
        ret, bus_rmsg = self.__pend(UTRC_RW.R, SERVO_REG.POS_LIMIT_MAX)
        pos = hex_data.bytes_to_int32_big(bus_rmsg.data[0:4])
        pos = int_to_rad(pos)
        return ret, pos

    def _set_pos_limit_max(self, pos):
        pos = rad_to_int(pos)
        txdata = hex_data.int32_to_bytes_big(pos)
        self.__send(UTRC_RW.W, SERVO_REG.POS_LIMIT_MAX, txdata)
        ret, bus_rmsg = self.__pend(UTRC_RW.W, SERVO_REG.POS_LIMIT_MAX)
        return ret

    def _get_pos_limit_diff(self):
        self.__send(UTRC_RW.R, SERVO_REG.POS_LIMIT_DIFF, None)
        ret, bus_rmsg = self.__pend(UTRC_RW.R, SERVO_REG.POS_LIMIT_DIFF)
        pos = hex_data.bytes_to_int32_big(bus_rmsg.data[0:4])
        pos = int_to_rad(pos)
        return ret, pos

    def _set_pos_limit_diff(self, pos):
        pos = rad_to_int(pos)
        txdata = hex_data.int32_to_bytes_big(pos)
        self.__send(UTRC_RW.W, SERVO_REG.POS_LIMIT_DIFF, txdata)
        ret, bus_rmsg = self.__pend(UTRC_RW.W, SERVO_REG.POS_LIMIT_DIFF)
        return ret

    def _get_pos_pidp(self):
        self.__send(UTRC_RW.R, SERVO_REG.POS_PIDP, None)
        ret, bus_rmsg = self.__pend(UTRC_RW.R, SERVO_REG.POS_PIDP)
        p = hex_data.bytes_to_int32_big(bus_rmsg.data[0:4])
        return ret, p

    def _set_pos_pidp(self, p):
        p = int(p)
        txdata = hex_data.int32_to_bytes_big(p)
        self.__send(UTRC_RW.W, SERVO_REG.POS_PIDP, txdata)
        ret, bus_rmsg = self.__pend(UTRC_RW.W, SERVO_REG.POS_PIDP)
        return ret

    def _get_pos_smooth_cyc(self):
        self.__send(UTRC_RW.R, SERVO_REG.POS_SMOOTH_CYC, None)
        ret, bus_rmsg = self.__pend(UTRC_RW.R, SERVO_REG.POS_SMOOTH_CYC)
        return ret, bus_rmsg.data[0]

    def _set_pos_smooth_cyc(self, cyc):
        txdata = [0]
        txdata[0] = int(cyc)
        self.__send(UTRC_RW.W, SERVO_REG.POS_SMOOTH_CYC, txdata)
        ret, bus_rmsg = self.__pend(UTRC_RW.W, SERVO_REG.POS_SMOOTH_CYC)
        return ret

    def _pos_cal_zero(self):
        txdata = [0]
        txdata[0] = SERVO_REG.POS_CAL_ZERO[0]
        self.__send(UTRC_RW.W, SERVO_REG.POS_CAL_ZERO, txdata)
        ret, bus_rmsg = self.__pend(UTRC_RW.W, SERVO_REG.POS_CAL_ZERO)
        return ret

############################################################
#                       Speed Api
############################################################

    def _get_vel_target(self):
        self.__send(UTRC_RW.R, SERVO_REG.VEL_TARGET, None)
        ret, bus_rmsg = self.__pend(UTRC_RW.R, SERVO_REG.VEL_TARGET)
        vel = hex_data.bytes_to_int32_big(bus_rmsg.data[0:4])
        vel = int_to_rad(vel)
        return ret, vel

    def _set_vel_target(self, vel):
        vel = rad_to_int(vel)
        txdata = hex_data.int32_to_bytes_big(vel)
        self.__send(UTRC_RW.W, SERVO_REG.VEL_TARGET, txdata)
        ret, bus_rmsg = self.__pend(UTRC_RW.W, SERVO_REG.VEL_TARGET)
        return ret

    def _get_vel_current(self):
        self.__send(UTRC_RW.R, SERVO_REG.VEL_CURRENT, None)
        ret, bus_rmsg = self.__pend(UTRC_RW.R, SERVO_REG.VEL_CURRENT)
        vel = hex_data.bytes_to_int32_big(bus_rmsg.data[0:4])
        vel = int_to_rad(vel)
        return ret, vel

    def _get_vel_limit_min(self):
        self.__send(UTRC_RW.R, SERVO_REG.VEL_LIMIT_MIN, None)
        ret, bus_rmsg = self.__pend(UTRC_RW.R, SERVO_REG.VEL_LIMIT_MIN)
        vel = hex_data.bytes_to_int32_big(bus_rmsg.data[0:4])
        vel = int_to_rad(vel)
        return ret, vel

    def _set_vel_limit_min(self, vel):
        vel = rad_to_int(vel)
        txdata = hex_data.int32_to_bytes_big(vel)
        self.__send(UTRC_RW.W, SERVO_REG.VEL_LIMIT_MIN, txdata)
        ret, bus_rmsg = self.__pend(UTRC_RW.W, SERVO_REG.VEL_LIMIT_MIN)
        return ret

    def _get_vel_limit_max(self):
        self.__send(UTRC_RW.R, SERVO_REG.VEL_LIMIT_MAX, None)
        ret, bus_rmsg = self.__pend(UTRC_RW.R, SERVO_REG.VEL_LIMIT_MAX)
        vel = hex_data.bytes_to_int32_big(bus_rmsg.data[0:4])
        vel = int_to_rad(vel)
        return ret, vel

    def _set_vel_limit_max(self, vel):
        vel = rad_to_int(vel)
        txdata = hex_data.int32_to_bytes_big(vel)
        self.__send(UTRC_RW.W, SERVO_REG.VEL_LIMIT_MAX, txdata)
        ret, bus_rmsg = self.__pend(UTRC_RW.W, SERVO_REG.VEL_LIMIT_MAX)
        return ret

    def _get_vel_limit_diff(self):
        self.__send(UTRC_RW.R, SERVO_REG.VEL_LIMIT_DIFF, None)
        ret, bus_rmsg = self.__pend(UTRC_RW.R, SERVO_REG.VEL_LIMIT_DIFF)
        vel = hex_data.bytes_to_int32_big(bus_rmsg.data[0:4])
        vel = int_to_rad(vel)
        return ret, vel

    def _set_vel_limit_diff(self, vel):
        vel = rad_to_int(vel)
        txdata = hex_data.int32_to_bytes_big(vel)
        self.__send(UTRC_RW.W, SERVO_REG.VEL_LIMIT_DIFF, txdata)
        ret, bus_rmsg = self.__pend(UTRC_RW.W, SERVO_REG.VEL_LIMIT_DIFF)
        return ret

    def _get_vel_pidp(self):
        self.__send(UTRC_RW.R, SERVO_REG.VEL_PIDP, None)
        ret, bus_rmsg = self.__pend(UTRC_RW.R, SERVO_REG.VEL_PIDP)
        p = hex_data.bytes_to_int32_big(bus_rmsg.data[0:4])
        return ret, p

    def _set_vel_pidp(self, p):
        p = int(p)
        txdata = hex_data.int32_to_bytes_big(p)
        self.__send(UTRC_RW.W, SERVO_REG.VEL_PIDP, txdata)
        ret, bus_rmsg = self.__pend(UTRC_RW.W, SERVO_REG.VEL_PIDP)
        return ret

    def _get_vel_pidi(self):
        self.__send(UTRC_RW.R, SERVO_REG.VEL_PIDI, None)
        ret, bus_rmsg = self.__pend(UTRC_RW.R, SERVO_REG.VEL_PIDI)
        pid_i = hex_data.bytes_to_int32_big(bus_rmsg.data[0:4])
        return ret, pid_i

    def _set_vel_pidi(self, pid_i):
        pid_i = int(pid_i)
        txdata = hex_data.int32_to_bytes_big(pid_i)
        self.__send(UTRC_RW.W, SERVO_REG.VEL_PIDI, txdata)
        ret, bus_rmsg = self.__pend(UTRC_RW.W, SERVO_REG.VEL_PIDI)
        return ret

    def _get_vel_smooth_cyc(self):
        self.__send(UTRC_RW.R, SERVO_REG.VEL_SMOOTH_CYC, None)
        ret, bus_rmsg = self.__pend(UTRC_RW.R, SERVO_REG.VEL_SMOOTH_CYC)
        return ret, bus_rmsg.data[0]

    def _set_vel_smooth_cyc(self, cyc):
        txdata = [0]
        txdata[0] = int(cyc)
        self.__send(UTRC_RW.W, SERVO_REG.VEL_SMOOTH_CYC, txdata)
        ret, bus_rmsg = self.__pend(UTRC_RW.W, SERVO_REG.VEL_SMOOTH_CYC)
        return ret

############################################################
#                       Current Api
############################################################

    def _get_tau_target(self):
        self.__send(UTRC_RW.R, SERVO_REG.TAU_TARGET, None)
        ret, bus_rmsg = self.__pend(UTRC_RW.R, SERVO_REG.TAU_TARGET)
        tau = hex_data.bytes_to_int32_big(bus_rmsg.data[0:4])
        tau = int_to_rad(tau)
        return ret, tau

    def _set_tau_target(self, tau):
        tau = rad_to_int(tau)
        txdata = hex_data.int32_to_bytes_big(tau)
        self.__send(UTRC_RW.W, SERVO_REG.TAU_TARGET, txdata)
        ret, bus_rmsg = self.__pend(UTRC_RW.W, SERVO_REG.TAU_TARGET)
        return ret

    def _get_tau_current(self):
        self.__send(UTRC_RW.R, SERVO_REG.TAU_CURRENT, None)
        ret, bus_rmsg = self.__pend(UTRC_RW.R, SERVO_REG.TAU_CURRENT)
        tau = hex_data.bytes_to_int32_big(bus_rmsg.data[0:4])
        tau = int_to_rad(tau)
        return ret, tau

    def _get_tau_limit_min(self):
        self.__send(UTRC_RW.R, SERVO_REG.TAU_LIMIT_MIN, None)
        ret, bus_rmsg = self.__pend(UTRC_RW.R, SERVO_REG.TAU_LIMIT_MIN)
        tau = hex_data.bytes_to_int32_big(bus_rmsg.data[0:4])
        tau = int_to_rad(tau)
        return ret, tau

    def _set_tau_limit_min(self, tau):
        tau = rad_to_int(tau)
        txdata = hex_data.int32_to_bytes_big(tau)
        self.__send(UTRC_RW.W, SERVO_REG.TAU_LIMIT_MIN, txdata)
        ret, bus_rmsg = self.__pend(UTRC_RW.W, SERVO_REG.TAU_LIMIT_MIN)
        return ret

    def _get_tau_limit_max(self):
        self.__send(UTRC_RW.R, SERVO_REG.TAU_LIMIT_MAX, None)
        ret, bus_rmsg = self.__pend(UTRC_RW.R, SERVO_REG.TAU_LIMIT_MAX)
        tau = hex_data.bytes_to_int32_big(bus_rmsg.data[0:4])
        tau = int_to_rad(tau)
        return ret, tau

    def _set_tau_limit_max(self, tau):
        tau = rad_to_int(tau)
        txdata = hex_data.int32_to_bytes_big(tau)
        self.__send(UTRC_RW.W, SERVO_REG.TAU_LIMIT_MAX, txdata)
        ret, bus_rmsg = self.__pend(UTRC_RW.W, SERVO_REG.TAU_LIMIT_MAX)
        return ret

    def _get_tau_limit_diff(self):
        self.__send(UTRC_RW.R, SERVO_REG.TAU_LIMIT_DIFF, None)
        ret, bus_rmsg = self.__pend(UTRC_RW.R, SERVO_REG.TAU_LIMIT_DIFF)
        value = hex_data.bytes_to_int32_big(bus_rmsg.data[0:4])
        value = int_to_rad(value)
        return ret, value

    def _set_tau_limit_diff(self, value):
        value = rad_to_int(value)
        txdata = hex_data.int32_to_bytes_big(value)
        self.__send(UTRC_RW.W, SERVO_REG.TAU_LIMIT_DIFF, txdata)
        ret, bus_rmsg = self.__pend(UTRC_RW.W, SERVO_REG.TAU_LIMIT_DIFF)
        return ret

    def _get_tau_pidp(self):
        self.__send(UTRC_RW.R, SERVO_REG.TAU_PIDP, None)
        ret, bus_rmsg = self.__pend(UTRC_RW.R, SERVO_REG.TAU_PIDP)
        pid_p = hex_data.bytes_to_int32_big(bus_rmsg.data[0:4])
        return ret, pid_p

    def _set_tau_pidp(self, pid_p):
        pid_p = int(pid_p)
        txdata = hex_data.int32_to_bytes_big(pid_p)
        self.__send(UTRC_RW.W, SERVO_REG.TAU_PIDP, txdata)
        ret, bus_rmsg = self.__pend(UTRC_RW.W, SERVO_REG.TAU_PIDP)
        return ret

    def _get_tau_pidi(self):
        self.__send(UTRC_RW.R, SERVO_REG.TAU_PIDI, None)
        ret, bus_rmsg = self.__pend(UTRC_RW.R, SERVO_REG.TAU_PIDI)
        pid_i = hex_data.bytes_to_int32_big(bus_rmsg.data[0:4])
        return ret, pid_i

    def _set_tau_pidi(self, pid_i):
        pid_i = int(pid_i)
        txdata = hex_data.int32_to_bytes_big(pid_i)
        self.__send(UTRC_RW.W, SERVO_REG.TAU_PIDI, txdata)
        ret, bus_rmsg = self.__pend(UTRC_RW.W, SERVO_REG.TAU_PIDI)
        return ret

    def _get_tau_smooth_cyc(self):
        self.__send(UTRC_RW.R, SERVO_REG.TAU_SMOOTH_CYC, None)
        ret, bus_rmsg = self.__pend(UTRC_RW.R, SERVO_REG.TAU_SMOOTH_CYC)
        return ret, bus_rmsg.data[0]

    def _set_tau_smooth_cyc(self, value):
        txdata = [0]
        txdata[0] = int(value)
        self.__send(UTRC_RW.W, SERVO_REG.TAU_SMOOTH_CYC, txdata)
        ret, bus_rmsg = self.__pend(UTRC_RW.W, SERVO_REG.TAU_SMOOTH_CYC)
        return ret
