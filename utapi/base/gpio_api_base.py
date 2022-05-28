#!/usr/bin/env python3
#
# Copyright (C) 2022 UmbraTek Inc. All Rights Reserved.
#
# Software License Agreement (BSD License)
#
# Author: Jimy Zhang <jimy.zhang@umbratek.com> <jimy92@163.com>
# =============================================================================
from utapi.common.utrc import UTRC_RW
from utapi.common import hex_data
from utapi.base.gpio_reg import GPIO_REG
import threading


class _GpioApiBase:
    def __init__(self, socket_fp, bus_client, tx_data):
        self.DB_FLG = "[GpioApiB] "
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
        ret, uuid = self.__get_reg_int8(GPIO_REG.UUID, 12)
        string = ""
        for i in uuid:
            string += "{0:0>2}".format(str(hex(i))[2:])
        return ret, string

    def _get_sw_version(self):
        ret, version = self.__get_reg_int8(GPIO_REG.SW_VERSION, 12)
        version = "".join(chr(i) for i in version)
        return ret, version

    def _get_hw_version(self):
        ret, version = self.__get_reg_int8(GPIO_REG.HW_VERSION, 12)
        string = ""
        for i in version:
            string += "{0:0>2}".format(str(hex(i))[2:])
        return ret, string

    def _set_com_id(self, id):
        return self.__set_reg_uint8(GPIO_REG.COM_ID, int(id))

    def _set_com_baud(self, baud):
        return self.__set_reg_int32(GPIO_REG.COM_BAUD, int(baud))

    def _reset_err(self):
        return self.__set_reg_uint8(GPIO_REG.RESET_ERR, GPIO_REG.RESET_ERR[0])

    def _restart_driver(self):
        return self.__set_reg_uint8(GPIO_REG.REBOOT_DRIVER, GPIO_REG.REBOOT_DRIVER[0])

    def _erase_parm(self):
        return self.__set_reg_uint8(GPIO_REG.ERASE_PARM, GPIO_REG.ERASE_PARM[0])

    def _saved_parm(self):
        return self.__set_reg_uint8(GPIO_REG.SAVED_PARM, GPIO_REG.SAVED_PARM[0])

    ############################################################
    #                       Extension Api
    ############################################################

    def _get_temp_limit(self):
        ret, value = self.__get_reg_int8(GPIO_REG.TEMP_LIMIT, 2)
        return ret, value[0], value[1]

    def _set_temp_limit(self, min, max):
        txdata = [int(min), int(max)]
        return self.__set_reg_int8(GPIO_REG.TEMP_LIMIT, txdata, 2)

    def _get_volt_limit(self):
        ret, value = self.__get_reg_int8(GPIO_REG.VOLT_LIMIT, 2)
        return ret, value[0], value[1]

    def _set_volt_limit(self, min, max):
        txdata = [int(min), int(max)]
        return self.__set_reg_int8(GPIO_REG.VOLT_LIMIT, txdata, 2)

    def _get_curr_limit(self):
        return self.__get_reg_fp32(GPIO_REG.CURR_LIMIT)

    def _set_curr_limit(self, value):
        return self.__set_reg_fp32(GPIO_REG.CURR_LIMIT, value)

    ############################################################
    #                       Control Api
    ############################################################

    def _get_temp_driver(self):
        return self.__get_reg_fp32(GPIO_REG.TEMP_DRIVER)

    def _get_bus_volt(self):
        return self.__get_reg_fp32(GPIO_REG.BUS_VOLT)

    def _get_bus_curr(self):
        return self.__get_reg_fp32(GPIO_REG.BUS_CURR)

    def _get_error_code(self):
        return self.__get_reg_int8(GPIO_REG.ERROR_CODE)

    ############################################################
    #                       Developer Api
    ############################################################

    def _get_frame_in(self):
        ret, bus_rmsg = self.__sendpend(UTRC_RW.R, GPIO_REG.FRAME_IN, None)
        fun = hex_data.bytes_to_uint32_big(bus_rmsg.data[0:4], 1)
        digitin = hex_data.bytes_to_uint32_big(bus_rmsg.data[4:8], 1)
        adc_n = bus_rmsg.data[8]
        adc_v = hex_data.bytes_to_fp32_big(bus_rmsg.data[9:9 + 4 * adc_n], adc_n)
        return ret, fun, digitin, adc_v, adc_n

    def _get_frame_ou(self):
        ret, bus_rmsg = self.__sendpend(UTRC_RW.R, GPIO_REG.FRAME_OU, None)
        fun = hex_data.bytes_to_uint32_big(bus_rmsg.data[0:4], 1)
        digitou = hex_data.bytes_to_uint32_big(bus_rmsg.data[4:8], 1)
        dac_n = bus_rmsg.data[8]
        dac_v = hex_data.bytes_to_fp32_big(bus_rmsg.data[9:9 + 4 * dac_n], dac_n)
        return ret, fun, digitou, dac_v, dac_n

    def _set_out_digit(self, digit):
        return self.__set_reg_int32(GPIO_REG.DIGITOU, digit)

    def _set_out_fun(self, fun):
        return self.__set_reg_int32(GPIO_REG.FUNGPIO, fun)
