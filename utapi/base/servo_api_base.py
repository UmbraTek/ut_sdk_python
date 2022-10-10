#!/usr/bin/env python3
#
# Copyright (C) 2020 UmbraTek Inc. All Rights Reserved.
#
# Software License Agreement (BSD License)
#
# Author: Jimy Zhang <jimy.zhang@umbratek.com> <jimy92@163.com>
# =============================================================================
from utapi.common.utrc import UTRC_RW, UTRC_RX_ERROR
from utapi.common import hex_data
from utapi.base.servo_reg import SERVO_REG
import threading


class _ServoApiBase:
    def __init__(self, socket_fp, bus_client, tx_data):
        self.DB_FLG = "[AdraApiB] "
        self.mutex = threading.Lock()
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

    def _send(self, rw, cmd, cmd_data, len_tx=0):
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

    def _pend(self, rw, cmd, timeout_s=1):
        if self.__is_err:
            return -999, self.tx_data

        if rw == UTRC_RW.R:
            data_rlen = cmd[2]
        else:
            data_rlen = cmd[4]
        return self.bus_client.pend(self.tx_data, data_rlen, timeout_s)

    def __sendpend(self, rw, reg, tx_data):
        self.mutex.acquire()
        self._send(rw, reg, tx_data)
        ret, bus_rmsg = self._pend(rw, reg)
        self.mutex.release()
        return ret, bus_rmsg

    def is_err(self):
        return self.__is_err

    ############################################################
    #                       Basic Function
    ############################################################

    def __get_reg_int8(self, reg, n=1, txdata=None):
        ret, bus_rmsg = self.__sendpend(UTRC_RW.R, reg, txdata)
        if n == 1:
            value = hex_data.bytes_to_int8(bus_rmsg.data[0], n)
        else:
            value = hex_data.bytes_to_int8(bus_rmsg.data[0:n], n)
        return ret, value

    def __set_reg_int8(self, reg, value, n=1):
        txdata = hex_data.int8_to_bytes_big(value, n)
        ret, bus_rmsg = self.__sendpend(UTRC_RW.W, reg, txdata)
        return ret

    def __set_reg_uint8(self, reg, value, n=1):
        txdata = hex_data.uint8_to_bytes_big(value, n)
        ret, bus_rmsg = self.__sendpend(UTRC_RW.W, reg, txdata)
        return ret

    def __get_reg_int32(self, reg, n=1, txdata=None):
        ret, bus_rmsg = self.__sendpend(UTRC_RW.R, reg, txdata)
        value = hex_data.bytes_to_int32_big(bus_rmsg.data, n)
        return ret, value

    def __set_reg_int32(self, reg, value, n=1):
        txdata = hex_data.int32_to_bytes_big(value, n)
        ret, bus_rmsg = self.__sendpend(UTRC_RW.W, reg, txdata)
        return ret

    def __get_reg_fp32(self, reg, n=1, txdata=None):
        ret, bus_rmsg = self.__sendpend(UTRC_RW.R, reg, txdata)
        value = hex_data.bytes_to_fp32_big(bus_rmsg.data, n)
        return ret, value

    def __set_reg_fp32(self, reg, value, n=1):
        datas = hex_data.fp32_to_bytes_big(value, n)
        ret, bus_rmsg = self.__sendpend(UTRC_RW.W, reg, datas)
        return ret

    ############################################################
    #                       Basic Api
    ############################################################

    def _get_uuid(self):
        ret, uuid = self.__get_reg_int8(SERVO_REG.UUID, 12)
        string = ""
        for i in uuid:
            string += "{0:0>2}".format(str(hex(i))[2:])
        return ret, string

    def _get_sw_version(self):
        ret, version = self.__get_reg_int8(SERVO_REG.SW_VERSION, 12)
        version = "".join(chr(i) for i in version)
        return ret, version

    def _get_hw_version(self):
        ret, version = self.__get_reg_int8(SERVO_REG.HW_VERSION, 12)
        string = ""
        for i in version:
            string += "{0:0>2}".format(str(hex(i))[2:])
        return ret, string

    def _get_multi_version(self):
        ret, version = self.__get_reg_int32(SERVO_REG.MULTI_VERSION)
        version = "0000000000" + str(version)
        return ret, version[len(version) - 12:len(version)]

    def _get_mech_ratio(self):
        return self.__get_reg_fp32(SERVO_REG.MECH_RATIO)

    def _set_mech_ratio(self, ratio):
        return self.__set_reg_fp32(SERVO_REG.MECH_RATIO, ratio)

    def _set_com_id(self, id):
        return self.__set_reg_uint8(SERVO_REG.COM_ID, int(id))

    def _set_com_baud(self, baud):
        return self.__set_reg_int32(SERVO_REG.COM_BAUD, int(baud))

    def _reset_err(self):
        return self.__set_reg_uint8(SERVO_REG.RESET_ERR, SERVO_REG.RESET_ERR[0])

    def _restart_driver(self):
        return self.__set_reg_uint8(SERVO_REG.REBOOT_DRIVER, SERVO_REG.REBOOT_DRIVER[0])

    def _erase_parm(self):
        return self.__set_reg_uint8(SERVO_REG.ERASE_PARM, SERVO_REG.ERASE_PARM[0])

    def _saved_parm(self):
        return self.__set_reg_uint8(SERVO_REG.SAVED_PARM, SERVO_REG.SAVED_PARM[0])

    ############################################################
    #                       Extension Api
    ############################################################

    def _get_elec_ratio(self):
        return self.__get_reg_fp32(SERVO_REG.ELEC_RATIO)

    def _set_elec_ratio(self, ratio):
        return self.__set_reg_fp32(SERVO_REG.ELEC_RATIO, ratio)

    def _get_motion_dir(self):
        return self.__get_reg_int8(SERVO_REG.MOTION_DIR)

    def _set_motion_dir(self, dir):
        return self.__set_reg_int8(SERVO_REG.MOTION_DIR, int(dir))

    def _get_iwdg_cyc(self):
        return self.__get_reg_int32(SERVO_REG.IWDG_CYC)

    def _set_iwdg_cyc(self, cyc):
        return self.__set_reg_int32(SERVO_REG.IWDG_CYC, int(cyc))

    def _get_temp_limit(self):
        ret, value = self.__get_reg_int8(SERVO_REG.TEMP_LIMIT, 2)
        return ret, value[0], value[1]

    def _set_temp_limit(self, min, max):
        txdata = [int(min), int(max)]
        return self.__set_reg_int8(SERVO_REG.TEMP_LIMIT, txdata, 2)

    def _get_volt_limit(self):
        ret, value = self.__get_reg_int8(SERVO_REG.VOLT_LIMIT, 2)
        return ret, value[0], value[1]

    def _set_volt_limit(self, min, max):
        txdata = [int(min), int(max)]
        return self.__set_reg_int8(SERVO_REG.VOLT_LIMIT, txdata, 2)

    def _get_curr_limit(self):
        return self.__get_reg_fp32(SERVO_REG.CURR_LIMIT)

    def _set_curr_limit(self, value):
        return self.__set_reg_fp32(SERVO_REG.CURR_LIMIT, value)

    def _get_brake_delay(self):
        ret, bus_rmsg = self.__sendpend(UTRC_RW.R, SERVO_REG.BRAKE_DELAY, None)
        ontime = hex_data.bytes_to_uint16_big(bus_rmsg.data[0:2])
        offtime = hex_data.bytes_to_uint16_big(bus_rmsg.data[2:4])
        return ret, ontime, offtime

    def _set_brake_delay(self, ontime, offtime):
        txdata = hex_data.uint16_to_bytes_big(int(ontime))
        txdata += hex_data.uint16_to_bytes_big(int(offtime))
        ret, bus_rmsg = self.__sendpend(UTRC_RW.W, SERVO_REG.BRAKE_DELAY, txdata)
        return ret

    def _get_debug_arg(self, i):
        txdata = bytes([int(i)])
        ret, bus_rmsg = self.__sendpend(UTRC_RW.R, SERVO_REG.DEBUG_ARG, txdata)
        p = hex_data.bytes_to_fp32_big(bus_rmsg.data[0:4])
        return ret, p

    def _set_debug_arg(self, i, param):
        txdata = bytes([int(i)])
        txdata += hex_data.fp32_to_bytes_big(float(param))
        ret, bus_rmsg = self.__sendpend(UTRC_RW.W, SERVO_REG.DEBUG_ARG, txdata)
        return ret

    ############################################################
    #                       Control Api
    ############################################################

    def _get_motion_mode(self):
        return self.__get_reg_int8(SERVO_REG.MOTION_MDOE)

    def _set_motion_mode(self, mode):
        return self.__set_reg_uint8(SERVO_REG.MOTION_MDOE, int(mode))

    def _get_motion_enable(self):
        return self.__get_reg_int8(SERVO_REG.MOTION_ENABLE)

    def _set_motion_enable(self, enable):
        return self.__set_reg_uint8(SERVO_REG.MOTION_ENABLE, int(enable))

    def _get_brake_enable(self):
        return self.__get_reg_int8(SERVO_REG.BRAKE_ENABLE)

    def _set_brake_enable(self, able):
        return self.__set_reg_uint8(SERVO_REG.BRAKE_ENABLE, int(able))

    def _get_temp_driver(self):
        return self.__get_reg_fp32(SERVO_REG.TEMP_DRIVER)

    def _get_temp_motor(self):
        return self.__get_reg_fp32(SERVO_REG.TEMP_MOTOR)

    def _get_bus_volt(self):
        return self.__get_reg_fp32(SERVO_REG.BUS_VOLT)

    def _get_bus_curr(self):
        return self.__get_reg_fp32(SERVO_REG.BUS_CURR)

    def _get_multi_volt(self):
        return self.__get_reg_fp32(SERVO_REG.MULTI_VOLT)

    def _get_error_code(self):
        return self.__get_reg_int8(SERVO_REG.ERROR_CODE)

    ############################################################
    #                       Position Api
    ############################################################

    def _get_pos_target(self):
        return self.__get_reg_fp32(SERVO_REG.POS_TARGET)

    def _set_pos_target(self, pos):
        return self.__set_reg_fp32(SERVO_REG.POS_TARGET, pos)

    def _get_pos_current(self):
        return self.__get_reg_fp32(SERVO_REG.POS_CURRENT)

    def _get_pos_limit_min(self):
        return self.__get_reg_fp32(SERVO_REG.POS_LIMIT_MIN)

    def _set_pos_limit_min(self, pos):
        return self.__set_reg_fp32(SERVO_REG.POS_LIMIT_MIN, pos)

    def _get_pos_limit_max(self):
        return self.__get_reg_fp32(SERVO_REG.POS_LIMIT_MAX)

    def _set_pos_limit_max(self, pos):
        return self.__set_reg_fp32(SERVO_REG.POS_LIMIT_MAX, pos)

    def _get_pos_limit_diff(self):
        return self.__get_reg_fp32(SERVO_REG.POS_LIMIT_DIFF)

    def _set_pos_limit_diff(self, pos):
        return self.__set_reg_fp32(SERVO_REG.POS_LIMIT_DIFF, pos)

    def _get_pos_pidp(self):
        return self.__get_reg_fp32(SERVO_REG.POS_PIDP)

    def _set_pos_pidp(self, p):
        return self.__set_reg_fp32(SERVO_REG.POS_PIDP, p)

    def _get_pos_smooth_cyc(self):
        return self.__get_reg_int8(SERVO_REG.POS_SMOOTH_CYC)

    def _set_pos_smooth_cyc(self, cyc):
        return self.__set_reg_uint8(SERVO_REG.POS_SMOOTH_CYC, int(cyc))

    def _get_pos_adrc_param(self, i):
        txdata = bytes([int(i)])
        ret, bus_rmsg = self.__sendpend(UTRC_RW.R, SERVO_REG.POS_ADRC_PARAM, txdata)
        p = hex_data.bytes_to_fp32_big(bus_rmsg.data[0:4])
        return ret, p

    def _set_pos_adrc_param(self, i, param):
        txdata = bytes([int(i)])
        txdata += hex_data.fp32_to_bytes_big(float(param))
        ret, bus_rmsg = self.__sendpend(UTRC_RW.W, SERVO_REG.POS_ADRC_PARAM, txdata)
        return ret

    def _pos_cal_zero(self):
        return self.__set_reg_uint8(SERVO_REG.POS_CAL_ZERO, SERVO_REG.POS_CAL_ZERO[0])

    ############################################################
    #                       Speed Api
    ############################################################

    def _get_vel_target(self):
        return self.__get_reg_fp32(SERVO_REG.VEL_TARGET)

    def _set_vel_target(self, vel):
        return self.__set_reg_fp32(SERVO_REG.VEL_TARGET, vel)

    def _get_vel_current(self):
        return self.__get_reg_fp32(SERVO_REG.VEL_CURRENT)

    def _get_vel_limit_min(self):
        return self.__get_reg_fp32(SERVO_REG.VEL_LIMIT_MIN)

    def _set_vel_limit_min(self, vel):
        return self.__set_reg_fp32(SERVO_REG.VEL_LIMIT_MIN, vel)

    def _get_vel_limit_max(self):
        return self.__get_reg_fp32(SERVO_REG.VEL_LIMIT_MAX)

    def _set_vel_limit_max(self, vel):
        return self.__set_reg_fp32(SERVO_REG.VEL_LIMIT_MAX, vel)

    def _get_vel_limit_diff(self):
        return self.__get_reg_fp32(SERVO_REG.VEL_LIMIT_DIFF)

    def _set_vel_limit_diff(self, vel):
        return self.__set_reg_fp32(SERVO_REG.VEL_LIMIT_DIFF, vel)

    def _get_vel_pidp(self):
        return self.__get_reg_fp32(SERVO_REG.VEL_PIDP)

    def _set_vel_pidp(self, p):
        return self.__set_reg_fp32(SERVO_REG.VEL_PIDP, p)

    def _get_vel_pidi(self):
        return self.__get_reg_fp32(SERVO_REG.VEL_PIDI)

    def _set_vel_pidi(self, i):
        return self.__set_reg_fp32(SERVO_REG.VEL_PIDI, i)

    def _get_vel_smooth_cyc(self):
        return self.__get_reg_int8(SERVO_REG.VEL_SMOOTH_CYC)

    def _set_vel_smooth_cyc(self, cyc):
        return self.__set_reg_uint8(SERVO_REG.VEL_SMOOTH_CYC, int(cyc))

    def _get_vel_adrc_param(self, i):
        txdata = bytes([int(i)])
        ret, bus_rmsg = self.__sendpend(UTRC_RW.R, SERVO_REG.VEL_ADRC_PARAM, txdata)
        p = hex_data.bytes_to_fp32_big(bus_rmsg.data[0:4])
        return ret, p

    def _set_vel_adrc_param(self, i, param):
        txdata = bytes([int(i)])
        txdata += hex_data.fp32_to_bytes_big(float(param))
        ret, bus_rmsg = self.__sendpend(UTRC_RW.W, SERVO_REG.VEL_ADRC_PARAM, txdata)
        return ret

    ############################################################
    #                       Current Api
    ############################################################

    def _get_tau_target(self):
        return self.__get_reg_fp32(SERVO_REG.TAU_TARGET)

    def _set_tau_target(self, tau):
        return self.__set_reg_fp32(SERVO_REG.TAU_TARGET, tau)

    def _get_tau_current(self):
        return self.__get_reg_fp32(SERVO_REG.TAU_CURRENT)

    def _get_tau_limit_min(self):
        return self.__get_reg_fp32(SERVO_REG.TAU_LIMIT_MIN)

    def _set_tau_limit_min(self, tau):
        return self.__set_reg_fp32(SERVO_REG.TAU_LIMIT_MIN, tau)

    def _get_tau_limit_max(self):
        return self.__get_reg_fp32(SERVO_REG.TAU_LIMIT_MAX)

    def _set_tau_limit_max(self, tau):
        return self.__set_reg_fp32(SERVO_REG.TAU_LIMIT_MAX, tau)

    def _get_tau_limit_diff(self):
        return self.__get_reg_fp32(SERVO_REG.TAU_LIMIT_DIFF)

    def _set_tau_limit_diff(self, value):
        return self.__set_reg_fp32(SERVO_REG.TAU_LIMIT_DIFF, value)

    def _get_tau_pidp(self):
        return self.__get_reg_fp32(SERVO_REG.TAU_PIDP)

    def _set_tau_pidp(self, p):
        return self.__set_reg_fp32(SERVO_REG.TAU_PIDP, p)

    def _get_tau_pidi(self):
        return self.__get_reg_fp32(SERVO_REG.TAU_PIDI)

    def _set_tau_pidi(self, i):
        return self.__set_reg_fp32(SERVO_REG.TAU_PIDI, i)

    def _get_tau_smooth_cyc(self):
        return self.__get_reg_int8(SERVO_REG.TAU_SMOOTH_CYC)

    def _set_tau_smooth_cyc(self, cyc):
        return self.__set_reg_uint8(SERVO_REG.TAU_SMOOTH_CYC, int(cyc))

    def _get_tau_adrc_param(self, i):
        txdata = bytes([int(i)])
        ret, bus_rmsg = self.__sendpend(UTRC_RW.R, SERVO_REG.TAU_ADRC_PARAM, txdata)
        p = hex_data.bytes_to_fp32_big(bus_rmsg.data[0:4])
        return ret, p

    def _set_tau_adrc_param(self, i, param):
        txdata = bytes([int(i)])
        txdata += hex_data.fp32_to_bytes_big(float(param))
        ret, bus_rmsg = self.__sendpend(UTRC_RW.W, SERVO_REG.TAU_ADRC_PARAM, txdata)
        return ret

    ############################################################
    #                       Developer Api
    ############################################################

    def _set_cpos_target(self, sid, eid, pos):
        id = self.id
        self.connect_to_id(0x55, 0x55)

        num = eid - sid + 1
        txdata = bytes([sid])
        txdata += bytes([eid])
        txdata += hex_data.fp32_to_bytes_big(pos, num)
        SERVO_REG.CPOS_TARGET[3] = 2 + 4 * num
        self.mutex.acquire()
        self._send(UTRC_RW.W, SERVO_REG.CPOS_TARGET, txdata)
        self.connect_to_id(id, id)
        self.mutex.release()

        return 0

    def _set_ctau_target(self, sid, eid, tau):
        id = self.id
        self.connect_to_id(0x55, 0x55)

        num = eid - sid + 1
        txdata = bytes([sid])
        txdata += bytes([eid])
        txdata += hex_data.fp32_to_bytes_big(tau, num)
        SERVO_REG.CTAU_TARGET[3] = 2 + 4 * num
        self.mutex.acquire()
        self._send(UTRC_RW.W, SERVO_REG.CTAU_TARGET, txdata)
        self.connect_to_id(id, id)
        self.mutex.release()

        return 0

    def _set_cpostau_target(self, sid, eid, pos, tau):
        id = self.id

        num = (eid - sid + 1)
        postau = [0] * num * 2
        for i in range(num):
            postau[i * 2] = pos[i]
            postau[i * 2 + 1] = tau[i]

        txdata = bytes([sid])
        txdata += bytes([eid])
        txdata += hex_data.fp32_to_bytes_big(postau, num * 2)
        SERVO_REG.CPOSTAU_TARGET[3] = 4 * num * 2 + 2

        self.mutex.acquire()
        self.connect_to_id(0x55, 0x55)
        self._send(UTRC_RW.W, SERVO_REG.CPOSTAU_TARGET, txdata)
        self.connect_to_id(id, id)
        self.mutex.release()

        return 0

    def _set_cposvel_target(self, sid, eid, pos, vel):
        id = self.id

        num = (eid - sid + 1)
        posvel = [0] * num * 2
        for i in range(num):
            posvel[i * 2] = pos[i]
            posvel[i * 2 + 1] = vel[i]

        txdata = bytes([sid])
        txdata += bytes([eid])
        txdata += hex_data.fp32_to_bytes_big(posvel, num * 2)
        SERVO_REG.CPOSVEL_TARGET[3] = 4 * num * 2 + 2

        self.mutex.acquire()
        self.connect_to_id(0x55, 0x55)
        self._send(UTRC_RW.W, SERVO_REG.CPOSVEL_TARGET, txdata)
        self.connect_to_id(id, id)
        self.mutex.release()

        return 0

    def _get_spostau_current(self):
        # self.mutex.acquire()
        ret, bus_rmsg = self.__sendpend(UTRC_RW.R, SERVO_REG.SPOSTAU_CURRENT, None)
        # self.mutex.release()

        if ret == UTRC_RX_ERROR.TIMEOUT:
            num = 0
            pos = 0
            tau = 0
        else:
            num = hex_data.bytes_to_int8(bus_rmsg.data[0])
            pos = hex_data.bytes_to_fp32_big(bus_rmsg.data[1:5])
            tau = hex_data.bytes_to_fp32_big(bus_rmsg.data[5:9])
        return ret, num, pos, tau

    def _get_cpostau_current(self, sid, eid):
        id = self.id
        num = (eid - sid + 1)

        ret = [0] * num
        broadcast_num = [0] * num
        pos = [0] * num
        tau = [0] * num

        txdata = bytes([sid])
        txdata += bytes([eid])
        self.mutex.acquire()
        self.connect_to_id(0x55, 0x55)
        self._send(UTRC_RW.R, SERVO_REG.CPOSTAU_CURRENT, txdata)
        for i in range(num):
            ret[i], bus_rmsg = self._pend(UTRC_RW.R, SERVO_REG.CPOSTAU_CURRENT)
            # if (bus_rmsg.master_id != i + 1):
            #    ret[i] = UTRC_RX_ERROR.TIMEOUT

            if ret[i] == UTRC_RX_ERROR.TIMEOUT:
                broadcast_num[i] = 0
                pos[i] = 0
                tau[i] = 0
            else:
                broadcast_num[i] = hex_data.bytes_to_int8(bus_rmsg.data[0])
                pos[i] = hex_data.bytes_to_fp32_big(bus_rmsg.data[1:5])
                tau[i] = hex_data.bytes_to_fp32_big(bus_rmsg.data[5:9])

        self.connect_to_id(id, id)
        self.mutex.release()

        return ret, broadcast_num, pos, tau

