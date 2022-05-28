#!/usr/bin/env python3
#
# Copyright (C) 2022 UmbraTek Inc. All Rights Reserved.
#
# Software License Agreement (BSD License)
#
# Author: Jimy Zhang <jimy.zhang@umbratek.com> <jimy92@163.com>
# =============================================================================
from utapi.base.gpio_api_base import _GpioApiBase


class CgpioApiBase(_GpioApiBase):
    def __init__(self, socket_fp, bus_client, tx_data):
        _GpioApiBase.__init__(self, socket_fp, bus_client, tx_data)
        self.connect_to_id(1)

    def close(self):
        u"""
        Close socket
        """
        self._close()

    def connect_to_id(self, id, virtual_id=0):
        u"""Sets the connection Controller Gpio ID.

        Args:
            id (int): ID of the Controller Gpio.
            virtual_id (int, optional): Only used for debugging. Defaults to 0.
        """
        return self._connect_to_id(id, virtual_id)

    ############################################################
    #                       Basic Api
    ############################################################

    def get_uuid(self):
        u"""Get the uuid

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning.
            uuid (string): The unique code of umbratek products is also one of the bases of maintenance and warranty.
            12-bit string.
        """
        return self._get_uuid()

    def get_sw_version(self):
        u"""Get the software version.

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning.
            version (string): Software version, 12-bit string.
        """
        return self._get_sw_version()

    def get_hw_version(self):
        u"""Get the hardware version.

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning.
            version (string): Hardware version, 12-bit string.
        """
        return self._get_hw_version()

    ############################################################
    #                       Developer Api
    ############################################################

    def get_frame_in(self):
        u"""Gets controller GPIO input information

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning.
            fun (uint32): Controller GPIO module input instruction.
                If bit16==1, bit0 indicates shutdown request (1: Shutdown, 0: No operation)
                If bit17==1, bit1 indicates ESTOP switch status (1: Pressed. 0: Not pressed)
            digit_gpio (uint32): Digital input GPIO status
                If bit31==1, bit14 indicates Wireless Button 1 status (1: Pressed, 0: Not pressed)
                If bit30==1, bit15 indicates Wireless Button 2 status (1: Pressed, 0: Not pressed)
                If bit16==1, bit0 indicates GPIO DIN1 status (1: High level, 0: Low level)
                If bit17==1, bit1 indicates GPIO DIN2 status (1: High level, 0: Low level)
                If bit18==1, bit2 indicates GPIO DIN3 status (1: High level, 0: Low level)
                If bit19==1, bit3 indicates GPIO DIN4 status (1: High level, 0: Low level)
                And so on
            adc_value (list): The first is the bus voltage, The others are GPIO analog input voltage values [V]
            adc_num (int): The number of GPIO analog inputs
        """
        return self._get_frame_in()

    def get_frame_ou(self):
        u"""Gets controller GPIO output information

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning.
            fun (uint32): Controller GPIO module output instruction.
                If bit16==1, bit0 indicates shutdown request (1: Open the DC48V, 0: Shutdown)
                If bit17==1, bit1 == 1: Output error status(Button LED flashes at a frequency of 3Hz)
                If bit18==1, bit2 == 1: Output enable status(Button LED is on)
                If bit19==1, bit3 indicates automatic startup(
                    1: Automatic startup when power is on,
                    0: Not automatic startup when power is on)
            digit_gpio (uint32): Digital output GPIO status
                If bit16==1, bit0 indicates GPIO DO1 status (1: High level, 0: Low level)
                If bit17==1, bit1 indicates GPIO DO2 status (1: High level, 0: Low level)
                And so on
            dac_value (list): GPIO analog output voltage values [V]
            dac_num (int): The number of GPIO analog outputs
        """
        return self._get_frame_ou()

    def set_out_digit(self, do1=-1, do2=-1):
        u"""Set digital output GPIO status

        Args:
            do1 (int, optional): Digital output IO1 (0: low level, 1: high level, others: not operate)
            do2 (int, optional): Digital output IO2 (0: low level, 1: high level, others: not operate)

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning.
        """
        digit = 0x0
        if do1 == 0:
            digit = digit | (0x00010000 << 0)
        elif do1 == 1:
            digit = digit | (0x00010001 << 0)

        if do2 == 0:
            digit = digit | (0x00010000 << 1)
        elif do2 == 1:
            digit = digit | (0x00010001 << 1)

        return self._set_out_digit(digit)

    def set_out_fun(self, dc48=-1, led=-1, autostart=-1):
        u"""Set controller GPIO module output instruction.

        Args:
            dc48 (int, optional): (1: Open the DC48V, 0: Shutdown, others: not operate)
            led (int, optional): (0: Button led blink, 1: Button led on, 2: Button led breathing, others: not operate)
            autostart (int, optional): (
                1: Automatic startup when power is on,
                0: Not automatic startup when power is on,
                others: not operate)

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning.
        """
        fun = 0x0

        if dc48 == 0:
            fun = fun | (0x00010000 << 0)
        elif dc48 == 1:
            fun = fun | (0x00010001 << 0)

        if led == 0:
            fun = fun | (0x00010001 << 1)
        elif led == 1:
            fun = fun | (0x00010001 << 2)
        elif led == 2:
            fun = fun | ((0x00010000 << 2) | (0x00010000 << 1))

        if autostart == 0:
            fun = fun | (0x00010000 << 3)
        elif autostart == 1:
            fun = fun | (0x00010001 << 3)

        return self._set_out_fun(fun)

    def open_dc48(self):
        return self.set_out_fun(1, -1, -1)

    def sys_shutdown(self):
        return self.set_out_fun(0, -1, -1)

    def button_led_blink(self):
        return self.set_out_fun(-1, 0, -1)

    def button_led_on(self):
        u"""Button led on
        This setting takes effect only when the current status is breathing
        """
        return self.set_out_fun(-1, 1, -1)

    def button_led_breathing(self):
        return self.set_out_fun(-1, 2, -1)

    def set_auto_startup(self):
        u"""Automatic startup when power is on
        """
        return self.set_out_fun(-1, -1, 1)

    def set_not_auto_startup(self):
        u"""Not automatic startup when power is on
        """
        return self.set_out_fun(-1, -1, 0)
