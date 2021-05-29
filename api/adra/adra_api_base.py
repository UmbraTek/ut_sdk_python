# Copyright 2020 The UmbraTek Inc. All Rights Reserved.
#
# Software License Agreement (BSD License)
#
# Author: Jimy Zhang <jimy.zhang@umbratek.com> <jimy92@163.com>
# =============================================================================
from common.utrc import UTRC_RW
from common import hex_data
from adra.adra_reg import ADRA_REG, rad_to_int, int_to_rad


class _AdraApiBase():
    def __init__(self, socket_fp, bus_client, tx_data):
        self.DB_FLG = '[AdraApiB] '
        self.socket_fp = socket_fp
        self.bus_client = bus_client
        self.tx_data = tx_data
        self.__is_err = 0

        id = 1
        self.id = id
        self.virid = id

    def close(self):
        """Close socket
        """
        if self.socket_fp:
            self.socket_fp.close()

    def connect_to_id(self, id, virtual_id=0):
        """Connect actuator ID

        Args:
            id (int): The ID number of the actuator
            virtual_id (int, optional): Only used for debugging. Defaults to 0.
        """
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

    def get_uuid(self):
        """Get the uuid

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
            uuid (string): The unique code of umbratek products is also a certificate of repair and warranty
                           12-bit string
        """
        self.__send(UTRC_RW.R, ADRA_REG.UUID, None)
        ret, bus_rmsg = self.__pend(UTRC_RW.R, ADRA_REG.UUID)
        uuid = bus_rmsg.data[0:12]
        return ret, uuid

    def get_sw_version(self):
        """Get the software version

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
            version (string): Software version, 12-bit string
        """
        self.__send(UTRC_RW.R, ADRA_REG.SW_VERSION, None)
        ret, bus_rmsg = self.__pend(UTRC_RW.R, ADRA_REG.SW_VERSION)
        version = bus_rmsg.data[0:12]
        return ret, version

    def get_hw_version(self):
        """Get the hardware version

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
            version (string): Hardware version, 12-bit string
        """
        self.__send(UTRC_RW.R, ADRA_REG.HW_VERSION, None)
        ret, bus_rmsg = self.__pend(UTRC_RW.R, ADRA_REG.HW_VERSION)
        version = bus_rmsg.data[0:12]
        return ret, version

    def get_multi_version(self):
        """Get the Multi-turn version

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
            version (int): Multi-turn version
        """
        self.__send(UTRC_RW.R, ADRA_REG.MULTI_VERSION, None)
        ret, bus_rmsg = self.__pend(UTRC_RW.R, ADRA_REG.MULTI_VERSION)
        version = hex_data.bytes_to_int32_big(bus_rmsg.data[0:4])
        return ret, version

    def get_mech_ratio(self):
        """Get the reduction ratio of the mechanical reducer

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
            ratio (float): reduction ratio
        """
        self.__send(UTRC_RW.R, ADRA_REG.MECH_RATIO, None)
        ret, bus_rmsg = self.__pend(UTRC_RW.R, ADRA_REG.MECH_RATIO)
        ratio = hex_data.bytes_to_int32_big(bus_rmsg.data[0:4])
        ratio = int_to_rad(ratio)
        return ret, ratio

    def set_mech_ratio(self, ratio):
        """Set the reduction ratio of the mechanical reducer

        Args:
            ratio (float): reduction ratio

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
        """
        ratio = rad_to_int(ratio)
        txdata = hex_data.int32_to_bytes_big(ratio)
        self.__send(UTRC_RW.W, ADRA_REG.MECH_RATIO, txdata)
        ret, bus_rmsg = self.__pend(UTRC_RW.W, ADRA_REG.MECH_RATIO)
        return ret

    def set_com_id(self, id):
        """Set the id number of the device

        Args:
            id (int): id number [1-125]

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
        """
        txdata = [0]
        txdata[0] = int(id)
        self.__send(UTRC_RW.W, ADRA_REG.COM_ID, txdata)
        ret, bus_rmsg = self.__pend(UTRC_RW.W, ADRA_REG.COM_ID)
        return ret

    def set_com_baud(self, baud):
        """Set communication baud rate, which can only be set to the following baud rates:
        9600, 14400, 19200, 38400, 56000,
        115200,128000,230400,256000,460800,500,000,512000,600000,750000,
        921600,1000000,1500000,2000000,2500000,3000000,3500000,4000000,4500000,
        5000000,5500000,6000000,8000000,11250000

        Args:
            baud (int): communication baud rate

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
        """
        txdata = hex_data.int32_to_bytes_big(int(baud))
        self.__send(UTRC_RW.W, ADRA_REG.COM_BAUD, txdata)
        ret, bus_rmsg = self.__pend(UTRC_RW.W, ADRA_REG.COM_BAUD)
        return ret

    def reset_err(self):
        """Reset fault

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
        """
        txdata = [0]
        txdata[0] = ADRA_REG.RESET_ERR[0]
        self.__send(UTRC_RW.W, ADRA_REG.RESET_ERR, txdata)
        ret, bus_rmsg = self.__pend(UTRC_RW.W, ADRA_REG.RESET_ERR)
        return ret

    def restart_driver(self):
        """Restart the device

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
        """
        txdata = [0]
        txdata[0] = ADRA_REG.REBOOT_DRIVER[0]
        self.__send(UTRC_RW.W, ADRA_REG.REBOOT_DRIVER, txdata)
        ret, bus_rmsg = self.__pend(UTRC_RW.W, ADRA_REG.REBOOT_DRIVER)
        return ret

    def erase_parm(self):
        """Restore the parameters to factory settings

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
        """
        txdata = [0]
        txdata[0] = ADRA_REG.ERASE_PARM[0]
        self.__send(UTRC_RW.W, ADRA_REG.ERASE_PARM, txdata)
        ret, bus_rmsg = self.__pend(UTRC_RW.W, ADRA_REG.ERASE_PARM, 3)
        return ret

    def saved_parm(self):
        """Save the current parameter settings

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
        """
        txdata = [0]
        txdata[0] = ADRA_REG.SAVED_PARM[0]
        self.__send(UTRC_RW.W, ADRA_REG.SAVED_PARM, txdata)
        ret, bus_rmsg = self.__pend(UTRC_RW.W, ADRA_REG.SAVED_PARM, 3)
        return ret

############################################################
#                       Ectension Api
############################################################

    def get_elec_ratio(self):
        """Get electronic gear ratio

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
            ratio (float): reduction ratio
        """
        self.__send(UTRC_RW.R, ADRA_REG.ELEC_RATIO, None)
        ret, bus_rmsg = self.__pend(UTRC_RW.R, ADRA_REG.ELEC_RATIO)
        ratio = hex_data.bytes_to_int32_big(bus_rmsg.data[0:4])
        ratio = int_to_rad(ratio)
        return ret, ratio

    def set_elec_ratio(self, ratio):
        """Set electronic gear ratio

        Args:
            ratio (float): reduction ratio

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
        """
        ratio = rad_to_int(ratio)
        txdata = hex_data.int32_to_bytes_big(ratio)
        self.__send(UTRC_RW.W, ADRA_REG.ELEC_RATIO, txdata)
        ret, bus_rmsg = self.__pend(UTRC_RW.W, ADRA_REG.ELEC_RATIO)
        return ret

    def get_motion_dir(self):
        """Get the direction of motion, 0: positive direction, 1: negative direction

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
            dir (bool): 1 or 0
        """
        self.__send(UTRC_RW.R, ADRA_REG.MOTION_DIR, None)
        ret, bus_rmsg = self.__pend(UTRC_RW.R, ADRA_REG.MOTION_DIR)
        dir = hex_data.bytes_to_int8(bus_rmsg.data[0])
        return ret, dir

    def set_motion_dir(self, dir):
        """Set the direction of motion, 0: positive direction, 1: negative direction

        Args:
            dir (bool): 1 or 0

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
        """
        txdata = [0]
        txdata[0] = int(dir)
        self.__send(UTRC_RW.W, ADRA_REG.MOTION_DIR, txdata)
        ret, bus_rmsg = self.__pend(UTRC_RW.W, ADRA_REG.MOTION_DIR)
        return ret

    def get_temp_limit(self):
        """Get the temperature limit threshold

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
            min (int): Minimum temperature alarm threshold
            max (int): Maximum temperature alarm threshold
        """
        self.__send(UTRC_RW.R, ADRA_REG.TEMP_LIMIT, None)
        ret, bus_rmsg = self.__pend(UTRC_RW.R, ADRA_REG.TEMP_LIMIT)
        min = hex_data.bytes_to_int8(bus_rmsg.data[0])
        max = hex_data.bytes_to_int8(bus_rmsg.data[1])
        return ret, min, max

    def set_temp_limit(self, min, max):
        """Set the temperature limit threshold, 
        the minimum alarm threshold range [-20, 90], 
        the maximum alarm threshold range [-20, 90], in degrees Celsius

        Args:
            min (int): Minimum temperature alarm threshold
            max (int): Maximum temperature alarm threshold

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
        """
        txdata = hex_data.int8_to_bytes_big(int(min))
        txdata += hex_data.int8_to_bytes_big(int(max))
        self.__send(UTRC_RW.W, ADRA_REG.TEMP_LIMIT, txdata)
        ret, bus_rmsg = self.__pend(UTRC_RW.W, ADRA_REG.TEMP_LIMIT)
        return ret

    def get_volt_limit(self):
        """Get the voltage limit threshold

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
            min (int): Minimum voltage alarm threshold
            max (int): Maximum voltage alarm threshold
        """
        self.__send(UTRC_RW.R, ADRA_REG.VOLT_LIMIT, None)
        ret, bus_rmsg = self.__pend(UTRC_RW.R, ADRA_REG.VOLT_LIMIT)
        min = hex_data.bytes_to_int8(bus_rmsg.data[0])
        max = hex_data.bytes_to_int8(bus_rmsg.data[1])
        return ret, min, max

    def set_volt_limit(self, min, max):
        """Set the voltage limit threshold, 
        the minimum alarm threshold range [18, 55], 
        the maximum alarm threshold range [18, 55], unit volt

        Args:
            min (int): Minimum voltage alarm threshold
            max (int): Maximum voltage alarm threshold

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
        """
        txdata = hex_data.int8_to_bytes_big(int(min))
        txdata += hex_data.int8_to_bytes_big(int(max))
        self.__send(UTRC_RW.W, ADRA_REG.VOLT_LIMIT, txdata)
        ret, bus_rmsg = self.__pend(UTRC_RW.W, ADRA_REG.VOLT_LIMIT)
        return ret

    def get_curr_limit(self):
        """Get current limit threshold

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
            value (float): Maximum current alarm threshold
        """
        self.__send(UTRC_RW.R, ADRA_REG.CURR_LIMIT, None)
        ret, bus_rmsg = self.__pend(UTRC_RW.R, ADRA_REG.CURR_LIMIT)
        value = hex_data.bytes_to_int32_big(bus_rmsg.data[0:4])
        value = int_to_rad(value)
        return ret, value

    def set_curr_limit(self, value):
        """Set current limit threshold

        Args:
            value (float): Maximum current alarm threshold

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
        """
        value = rad_to_int(value)
        txdata = hex_data.int32_to_bytes_big(value)
        self.__send(UTRC_RW.W, ADRA_REG.CURR_LIMIT, txdata)
        ret, bus_rmsg = self.__pend(UTRC_RW.W, ADRA_REG.CURR_LIMIT)
        return ret

    def get_brake_pwm(self):
        """Ready to be eliminated

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
        """
        self.__send(UTRC_RW.R, ADRA_REG.BRAKE_PWM, None)
        ret, bus_rmsg = self.__pend(UTRC_RW.R, ADRA_REG.BRAKE_PWM)
        brake_pwm = hex_data.bytes_to_int8(bus_rmsg.data[0])
        return ret, brake_pwm

    def set_brake_pwm(self, brake_pwm):
        """Ready to be eliminated

        Args:
            brake_pwm ([type]): [description]

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
        """
        txdata = [0]
        txdata[0] = int(brake_pwm)
        self.__send(UTRC_RW.W, ADRA_REG.BRAKE_PWM, txdata)
        ret, bus_rmsg = self.__pend(UTRC_RW.W, ADRA_REG.BRAKE_PWM)
        return ret

############################################################
#                       Control Api
############################################################

    def get_motion_mode(self):
        """Get the operating mode

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
            mode (int): operating mode of the arm
                1: Position mode
                2: Speed ​​mode
                3: Current mode
                4: Mixed mode
        """
        self.__send(UTRC_RW.R, ADRA_REG.MOTION_MDOE, None)
        ret, bus_rmsg = self.__pend(UTRC_RW.R, ADRA_REG.MOTION_MDOE)
        return ret, bus_rmsg.data[0]

    def set_motion_mode(self, mode):
        """Set the operating mode
        When the motion mode is set, the device will deactivate the motion enable and need to re-enable the motion

        Args:
            mode (int): operating mode of the arm
                1: Position mode
                2: Speed ​​mode
                3: Current mode
                4: Mixed mode

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
        """
        txdata = [0]
        txdata[0] = int(mode)
        self.__send(UTRC_RW.W, ADRA_REG.MOTION_MDOE, txdata)
        ret, bus_rmsg = self.__pend(UTRC_RW.W, ADRA_REG.MOTION_MDOE)
        return ret

    def get_motion_enable(self):
        """Get motion enable status

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
            enable (bool): 0 Disable servo, 1 Enable servo
        """
        self.__send(UTRC_RW.R, ADRA_REG.MOTION_ENABLE, None)
        ret, bus_rmsg = self.__pend(UTRC_RW.R, ADRA_REG.MOTION_ENABLE)
        return ret, bus_rmsg.data[0]

    def set_motion_enable(self, enable):
        """Set motion enable status

        Args:
            enable (bool): 0 Disable servo, 1 Enable servo

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
        """
        txdata = [0]
        txdata[0] = int(enable)
        self.__send(UTRC_RW.W, ADRA_REG.MOTION_ENABLE, txdata)
        ret, bus_rmsg = self.__pend(UTRC_RW.W, ADRA_REG.MOTION_ENABLE)
        return ret

    def get_brake_enable(self):
        """Get brake enable status

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
            enable (bool): 0 Disable brake, 1 Enable brake
        """
        self.__send(UTRC_RW.R, ADRA_REG.BRAKE_ENABLE, None)
        ret, bus_rmsg = self.__pend(UTRC_RW.R, ADRA_REG.BRAKE_ENABLE)
        return ret, bus_rmsg.data[0]

    def set_brake_enable(self, able):
        """Set the brake enable state, enable the brake separately, and operate this register only when the motion is disabled, 
        because the brake is automatically opened in the motion enable state.

        Args:
            enable (bool): 0 Disable brake, 1 Enable brake

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
        """
        txdata = [0]
        txdata[0] = int(able)
        self.__send(UTRC_RW.W, ADRA_REG.BRAKE_ENABLE, txdata)
        ret, bus_rmsg = self.__pend(UTRC_RW.W, ADRA_REG.BRAKE_ENABLE)
        return ret

    def get_temp_driver(self):
        """Get drive temperature

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
            temp (float): temperature [degrees Celsius]
        """
        self.__send(UTRC_RW.R, ADRA_REG.TEMP_DRIVER, None)
        ret, bus_rmsg = self.__pend(UTRC_RW.R, ADRA_REG.TEMP_DRIVER)
        temp = hex_data.bytes_to_int32_big(bus_rmsg.data[0:4])
        return ret, int_to_rad(temp)

    def get_temp_motor(self):
        """Get drive motor

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
            temp (float): temperature [degrees Celsius]
        """
        self.__send(UTRC_RW.R, ADRA_REG.TEMP_MOTOR, None)
        ret, bus_rmsg = self.__pend(UTRC_RW.R, ADRA_REG.TEMP_MOTOR)
        temp = hex_data.bytes_to_int32_big(bus_rmsg.data[0:4])
        return ret, int_to_rad(temp)

    def get_bus_volt(self):
        """Get bus voltage

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
            volt (float): volt [V]
        """
        self.__send(UTRC_RW.R, ADRA_REG.BUS_VOLT, None)
        ret, bus_rmsg = self.__pend(UTRC_RW.R, ADRA_REG.BUS_VOLT)
        volt = hex_data.bytes_to_int32_big(bus_rmsg.data[0:4])
        return ret, int_to_rad(volt)

    def get_bus_curr(self):
        """Get bus current

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
            current (float): current [A]
        """
        self.__send(UTRC_RW.R, ADRA_REG.BUS_CURR, None)
        ret, bus_rmsg = self.__pend(UTRC_RW.R, ADRA_REG.BUS_CURR)
        current = hex_data.bytes_to_int32_big(bus_rmsg.data[0:4])
        return ret, int_to_rad(current)

    def get_multi_volt(self):
        """Get battery voltage of multi-turn encoder

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
            volt (float): volt [V]
        """
        self.__send(UTRC_RW.R, ADRA_REG.MULTI_VOLT, None)
        ret, bus_rmsg = self.__pend(UTRC_RW.R, ADRA_REG.MULTI_VOLT)
        volt = hex_data.bytes_to_int32_big(bus_rmsg.data[0:4])
        volt = int_to_rad(volt)
        return ret, volt

    def get_error_code(self):
        """Get error code, the meaning of the fault code is referred to the appendix <fault code>

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
            code (int): error code
        """
        self.__send(UTRC_RW.R, ADRA_REG.ERROR_CODE, None)
        ret, bus_rmsg = self.__pend(UTRC_RW.R, ADRA_REG.ERROR_CODE)
        return ret, hex_data.bytes_to_int8(bus_rmsg.data[0])

############################################################
#                       Position Api
############################################################

    def get_pos_target(self):
        """Get target position

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
            pos (float): target position [rad]
        """
        self.__send(UTRC_RW.R, ADRA_REG.POS_TARGET, None)
        ret, bus_rmsg = self.__pend(UTRC_RW.R, ADRA_REG.POS_TARGET)
        pos = hex_data.bytes_to_int32_big(bus_rmsg.data[0:4])
        pos = int_to_rad(pos)
        return ret, pos

    def set_pos_target(self, pos):
        """Set target position

        Args:
            pos (float): target position [rad]

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
        """
        pos = rad_to_int(pos)
        txdata = hex_data.int32_to_bytes_big(pos)
        self.__send(UTRC_RW.W, ADRA_REG.POS_TARGET, txdata)
        ret, bus_rmsg = self.__pend(UTRC_RW.W, ADRA_REG.POS_TARGET)
        return ret

    def get_pos_current(self):
        """Get current position

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
            pos (float): current position [rad]
        """
        self.__send(UTRC_RW.R, ADRA_REG.POS_CURRENT, None)
        ret, bus_rmsg = self.__pend(UTRC_RW.R, ADRA_REG.POS_CURRENT)
        pos = hex_data.bytes_to_int32_big(bus_rmsg.data[0:4])
        pos = int_to_rad(pos)
        return ret, pos

    def get_pos_limit_min(self):
        """Get the minimum limit threshold of the position in position mode

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
            pos (float): position [rad]
        """
        self.__send(UTRC_RW.R, ADRA_REG.POS_LIMIT_MIN, None)
        ret, bus_rmsg = self.__pend(UTRC_RW.R, ADRA_REG.POS_LIMIT_MIN)
        pos = hex_data.bytes_to_int32_big(bus_rmsg.data[0:4])
        pos = int_to_rad(pos)
        return ret, pos

    def set_pos_limit_min(self, pos):
        """Set the minimum limit threshold of the position in position mode, 
        other modes such as speed mode and current mode do not work

        Args:
            pos (float): position [rad]

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
        """
        pos = rad_to_int(pos)
        txdata = hex_data.int32_to_bytes_big(pos)
        self.__send(UTRC_RW.W, ADRA_REG.POS_LIMIT_MIN, txdata)
        ret, bus_rmsg = self.__pend(UTRC_RW.W, ADRA_REG.POS_LIMIT_MIN)
        return ret

    def get_pos_limit_max(self):
        """Get the maximum limit threshold of the position in position mode

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
            pos (float): position [rad]
        """
        self.__send(UTRC_RW.R, ADRA_REG.POS_LIMIT_MAX, None)
        ret, bus_rmsg = self.__pend(UTRC_RW.R, ADRA_REG.POS_LIMIT_MAX)
        pos = hex_data.bytes_to_int32_big(bus_rmsg.data[0:4])
        pos = int_to_rad(pos)
        return ret, pos

    def set_pos_limit_max(self, pos):
        """Set the maximum limit threshold of the position in position mode, 
        other modes such as speed mode and current mode do not work

        Args:
            pos (float): position [rad]

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
        """
        pos = rad_to_int(pos)
        txdata = hex_data.int32_to_bytes_big(pos)
        self.__send(UTRC_RW.W, ADRA_REG.POS_LIMIT_MAX, txdata)
        ret, bus_rmsg = self.__pend(UTRC_RW.W, ADRA_REG.POS_LIMIT_MAX)
        return ret

    def get_pos_limit_diff(self):
        """Get the maximum position following error threshold in position mode

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
            pos (float): position [rad]
        """
        self.__send(UTRC_RW.R, ADRA_REG.POS_LIMIT_DIFF, None)
        ret, bus_rmsg = self.__pend(UTRC_RW.R, ADRA_REG.POS_LIMIT_DIFF)
        pos = hex_data.bytes_to_int32_big(bus_rmsg.data[0:4])
        pos = int_to_rad(pos)
        return ret, pos

    def set_pos_limit_diff(self, pos):
        """Set the maximum position following error threshold in position mode, 
        the tracking error alarm threshold of the current position and the target position, 
        other modes such as speed mode and current mode do not work

        Args:
            pos (float): position [rad]

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
        """
        pos = rad_to_int(pos)
        txdata = hex_data.int32_to_bytes_big(pos)
        self.__send(UTRC_RW.W, ADRA_REG.POS_LIMIT_DIFF, txdata)
        ret, bus_rmsg = self.__pend(UTRC_RW.W, ADRA_REG.POS_LIMIT_DIFF)
        return ret

    def get_pos_pidp(self):
        """Get position loop control parameter P

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
            p (int): parameter P
        """
        self.__send(UTRC_RW.R, ADRA_REG.POS_PIDP, None)
        ret, bus_rmsg = self.__pend(UTRC_RW.R, ADRA_REG.POS_PIDP)
        p = hex_data.bytes_to_int32_big(bus_rmsg.data[0:4])
        return ret, p

    def set_pos_pidp(self, p):
        """Get position loop control parameter P

        Args:
            p (int): parameter P

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
        """
        p = int(p)
        txdata = hex_data.int32_to_bytes_big(p)
        self.__send(UTRC_RW.W, ADRA_REG.POS_PIDP, txdata)
        ret, bus_rmsg = self.__pend(UTRC_RW.W, ADRA_REG.POS_PIDP)
        return ret

    def get_pos_smooth_cyc(self):
        """Get smoothing filter period of the position loop

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
            cyc (int): smoothing period [1-125]
        """
        self.__send(UTRC_RW.R, ADRA_REG.POS_SMOOTH_CYC, None)
        ret, bus_rmsg = self.__pend(UTRC_RW.R, ADRA_REG.POS_SMOOTH_CYC)
        return ret, bus_rmsg.data[0]

    def set_pos_smooth_cyc(self, cyc):
        """Set smoothing filter period of the position loop. The larger the smoothing period, 
        the smoother the movement and the slower the response. The range is 1 to 125

        Args:
            cyc (int): smoothing period [1-125]

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
        """
        txdata = [0]
        txdata[0] = int(cyc)
        self.__send(UTRC_RW.W, ADRA_REG.POS_SMOOTH_CYC, txdata)
        ret, bus_rmsg = self.__pend(UTRC_RW.W, ADRA_REG.POS_SMOOTH_CYC)
        return ret

    def pos_cal_zero(self):
        """Set current position as mechanical zero, after the operation, the user needs to restart the device

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
        """
        txdata = [0]
        txdata[0] = ADRA_REG.POS_CAL_ZERO[0]
        self.__send(UTRC_RW.W, ADRA_REG.POS_CAL_ZERO, txdata)
        ret, bus_rmsg = self.__pend(UTRC_RW.W, ADRA_REG.POS_CAL_ZERO)
        return ret

############################################################
#                       Speed Api
############################################################

    def get_vel_target(self):
        """Get target speed

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
            vel (float): speed [rad/s]
        """
        self.__send(UTRC_RW.R, ADRA_REG.VEL_TARGET, None)
        ret, bus_rmsg = self.__pend(UTRC_RW.R, ADRA_REG.VEL_TARGET)
        vel = hex_data.bytes_to_int32_big(bus_rmsg.data[0:4])
        vel = int_to_rad(vel)
        return ret, vel

    def set_vel_target(self, vel):
        """Set target speed

        Args:
            vel (float): speed [rad/s]

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
        """
        vel = rad_to_int(vel)
        txdata = hex_data.int32_to_bytes_big(vel)
        self.__send(UTRC_RW.W, ADRA_REG.VEL_TARGET, txdata)
        ret, bus_rmsg = self.__pend(UTRC_RW.W, ADRA_REG.VEL_TARGET)
        return ret

    def get_vel_current(self):
        """Get current speed

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
            vel (float): speed [rad/s]
        """
        self.__send(UTRC_RW.R, ADRA_REG.VEL_CURRENT, None)
        ret, bus_rmsg = self.__pend(UTRC_RW.R, ADRA_REG.VEL_CURRENT)
        vel = hex_data.bytes_to_int32_big(bus_rmsg.data[0:4])
        vel = int_to_rad(vel)
        return ret, vel

    def get_vel_limit_min(self):
        """Get the minimum limit of the speed in speed mode and position mode

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
            vel (float): speed [rad/s]
        """
        self.__send(UTRC_RW.R, ADRA_REG.VEL_LIMIT_MIN, None)
        ret, bus_rmsg = self.__pend(UTRC_RW.R, ADRA_REG.VEL_LIMIT_MIN)
        vel = hex_data.bytes_to_int32_big(bus_rmsg.data[0:4])
        vel = int_to_rad(vel)
        return ret, vel

    def set_vel_limit_min(self, vel):
        """Set the minimum limit of the speed in speed mode and position mode, 
        other modes such as current mode do not work

        Args:
            vel (float): speed [rad/s]

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
        """
        vel = rad_to_int(vel)
        txdata = hex_data.int32_to_bytes_big(vel)
        self.__send(UTRC_RW.W, ADRA_REG.VEL_LIMIT_MIN, txdata)
        ret, bus_rmsg = self.__pend(UTRC_RW.W, ADRA_REG.VEL_LIMIT_MIN)
        return ret

    def get_vel_limit_max(self):
        """Get maximum limit of the speed in speed mode and position mode

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
            vel (float): speed [rad/s]
        """
        self.__send(UTRC_RW.R, ADRA_REG.VEL_LIMIT_MAX, None)
        ret, bus_rmsg = self.__pend(UTRC_RW.R, ADRA_REG.VEL_LIMIT_MAX)
        vel = hex_data.bytes_to_int32_big(bus_rmsg.data[0:4])
        vel = int_to_rad(vel)
        return ret, vel

    def set_vel_limit_max(self, vel):
        """Set maximum limit of the speed in speed mode and position mode, 
        other modes such as current mode do not work

        Args:
            vel (float): speed [rad/s]

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
        """
        vel = rad_to_int(vel)
        txdata = hex_data.int32_to_bytes_big(vel)
        self.__send(UTRC_RW.W, ADRA_REG.VEL_LIMIT_MAX, txdata)
        ret, bus_rmsg = self.__pend(UTRC_RW.W, ADRA_REG.VEL_LIMIT_MAX)
        return ret

    def get_vel_limit_diff(self):
        """Get the maximum speed following error threshold in the speed mode

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
            vel (float): speed [rad/s]
        """
        self.__send(UTRC_RW.R, ADRA_REG.VEL_LIMIT_DIFF, None)
        ret, bus_rmsg = self.__pend(UTRC_RW.R, ADRA_REG.VEL_LIMIT_DIFF)
        vel = hex_data.bytes_to_int32_big(bus_rmsg.data[0:4])
        vel = int_to_rad(vel)
        return ret, vel

    def set_vel_limit_diff(self, vel):
        """Set the maximum speed following error threshold in the speed mode,
        the tracking error alarm threshold of the current spped and the target speed, 
        other modes such as position mode and current mode do not work

        Args:
            vel (float): speed [rad/s]

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
        """
        vel = rad_to_int(vel)
        txdata = hex_data.int32_to_bytes_big(vel)
        self.__send(UTRC_RW.W, ADRA_REG.VEL_LIMIT_DIFF, txdata)
        ret, bus_rmsg = self.__pend(UTRC_RW.W, ADRA_REG.VEL_LIMIT_DIFF)
        return ret

    def get_vel_pidp(self):
        """Get speed loop control parameter P

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
            p (int): parameter P
        """
        self.__send(UTRC_RW.R, ADRA_REG.VEL_PIDP, None)
        ret, bus_rmsg = self.__pend(UTRC_RW.R, ADRA_REG.VEL_PIDP)
        p = hex_data.bytes_to_int32_big(bus_rmsg.data[0:4])
        return ret, p

    def set_vel_pidp(self, p):
        """Set speed loop control parameter P

        Args:
            p (int): parameter P

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
        """
        p = int(p)
        txdata = hex_data.int32_to_bytes_big(p)
        self.__send(UTRC_RW.W, ADRA_REG.VEL_PIDP, txdata)
        ret, bus_rmsg = self.__pend(UTRC_RW.W, ADRA_REG.VEL_PIDP)
        return ret

    def get_vel_pidi(self):
        """Get speed loop control parameter I

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
            pid_i (int): parameter pid_i
        """
        self.__send(UTRC_RW.R, ADRA_REG.VEL_PIDI, None)
        ret, bus_rmsg = self.__pend(UTRC_RW.R, ADRA_REG.VEL_PIDI)
        pid_i = hex_data.bytes_to_int32_big(bus_rmsg.data[0:4])
        return ret, pid_i

    def set_vel_pidi(self, pid_i):
        """Set speed loop control parameter I

        Args:
            pid_i (int): parameter pid_i

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
        """
        pid_i = int(pid_i)
        txdata = hex_data.int32_to_bytes_big(pid_i)
        self.__send(UTRC_RW.W, ADRA_REG.VEL_PIDI, txdata)
        ret, bus_rmsg = self.__pend(UTRC_RW.W, ADRA_REG.VEL_PIDI)
        return ret

    def get_vel_smooth_cyc(self):
        """Get smoothing filter period of the speed loop

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
            cyc (int): smoothing period [1-125]
        """
        self.__send(UTRC_RW.R, ADRA_REG.VEL_SMOOTH_CYC, None)
        ret, bus_rmsg = self.__pend(UTRC_RW.R, ADRA_REG.VEL_SMOOTH_CYC)
        return ret, bus_rmsg.data[0]

    def set_vel_smooth_cyc(self, cyc):
        """Set smoothing filter period of the speed loop. The larger the smoothing period, 
        the smoother the movement and the slower the response. The range is 1 to 125

        Args:
            cyc (int): smoothing period [1-125]

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
        """
        txdata = [0]
        txdata[0] = int(cyc)
        self.__send(UTRC_RW.W, ADRA_REG.VEL_SMOOTH_CYC, txdata)
        ret, bus_rmsg = self.__pend(UTRC_RW.W, ADRA_REG.VEL_SMOOTH_CYC)
        return ret


############################################################
#                       Current Api
############################################################

    def get_tau_target(self):
        """Get target current

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
            tau (float): target current [A]
        """
        self.__send(UTRC_RW.R, ADRA_REG.TAU_TARGET, None)
        ret, bus_rmsg = self.__pend(UTRC_RW.R, ADRA_REG.TAU_TARGET)
        tau = hex_data.bytes_to_int32_big(bus_rmsg.data[0:4])
        tau = int_to_rad(tau)
        return ret, tau

    def set_tau_target(self, tau):
        """Set target current

        Args:
            tau (float): target current [A]

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
        """
        tau = rad_to_int(tau)
        txdata = hex_data.int32_to_bytes_big(tau)
        self.__send(UTRC_RW.W, ADRA_REG.TAU_TARGET, txdata)
        ret, bus_rmsg = self.__pend(UTRC_RW.W, ADRA_REG.TAU_TARGET)
        return ret

    def get_tau_current(self):
        """Get current current

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
            tau (float): current current [A]
        """
        self.__send(UTRC_RW.R, ADRA_REG.TAU_CURRENT, None)
        ret, bus_rmsg = self.__pend(UTRC_RW.R, ADRA_REG.TAU_CURRENT)
        tau = hex_data.bytes_to_int32_big(bus_rmsg.data[0:4])
        tau = int_to_rad(tau)
        return ret, tau

    def get_tau_limit_min(self):
        """Get the minimum limit threshold of the current

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
            tau (float): current [A]
        """
        self.__send(UTRC_RW.R, ADRA_REG.TAU_LIMIT_MIN, None)
        ret, bus_rmsg = self.__pend(UTRC_RW.R, ADRA_REG.TAU_LIMIT_MIN)
        tau = hex_data.bytes_to_int32_big(bus_rmsg.data[0:4])
        tau = int_to_rad(tau)
        return ret, tau

    def set_tau_limit_min(self, tau):
        """Set the minimum limit threshold of the current, all modes are effective

        Args:
            tau (float): current [A]

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
        """
        tau = rad_to_int(tau)
        txdata = hex_data.int32_to_bytes_big(tau)
        self.__send(UTRC_RW.W, ADRA_REG.TAU_LIMIT_MIN, txdata)
        ret, bus_rmsg = self.__pend(UTRC_RW.W, ADRA_REG.TAU_LIMIT_MIN)
        return ret

    def get_tau_limit_max(self):
        """Get the maximum limit threshold of the current

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
            tau (float): current [A]
        """
        self.__send(UTRC_RW.R, ADRA_REG.TAU_LIMIT_MAX, None)
        ret, bus_rmsg = self.__pend(UTRC_RW.R, ADRA_REG.TAU_LIMIT_MAX)
        tau = hex_data.bytes_to_int32_big(bus_rmsg.data[0:4])
        tau = int_to_rad(tau)
        return ret, tau

    def set_tau_limit_max(self, tau):
        """Set the maximum limit threshold of the current, all modes are effective

        Args:
            tau (float): current [A]

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
        """
        tau = rad_to_int(tau)
        txdata = hex_data.int32_to_bytes_big(tau)
        self.__send(UTRC_RW.W, ADRA_REG.TAU_LIMIT_MAX, txdata)
        ret, bus_rmsg = self.__pend(UTRC_RW.W, ADRA_REG.TAU_LIMIT_MAX)
        return ret

    def get_tau_limit_diff(self):
        """Get the maximum current following error threshold in the current mode

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
            tau (float): current [A]
        """
        self.__send(UTRC_RW.R, ADRA_REG.TAU_LIMIT_DIFF, None)
        ret, bus_rmsg = self.__pend(UTRC_RW.R, ADRA_REG.TAU_LIMIT_DIFF)
        value = hex_data.bytes_to_int32_big(bus_rmsg.data[0:4])
        value = int_to_rad(value)
        return ret, value

    def set_tau_limit_diff(self, value):
        """Set the maximum current following error threshold in the current mode, 
        the tracking error alarm threshold of the current current and the target current, 
        other modes such as position mode and speed mode do not work

        Args:
            tau (float): current [A]

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
        """
        value = rad_to_int(value)
        txdata = hex_data.int32_to_bytes_big(value)
        self.__send(UTRC_RW.W, ADRA_REG.TAU_LIMIT_DIFF, txdata)
        ret, bus_rmsg = self.__pend(UTRC_RW.W, ADRA_REG.TAU_LIMIT_DIFF)
        return ret

    def get_tau_pidp(self):
        """Get current loop control parameter P

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
            pid_p (int): parameter P
        """
        self.__send(UTRC_RW.R, ADRA_REG.TAU_PIDP, None)
        ret, bus_rmsg = self.__pend(UTRC_RW.R, ADRA_REG.TAU_PIDP)
        pid_p = hex_data.bytes_to_int32_big(bus_rmsg.data[0:4])
        return ret, pid_p

    def set_tau_pidp(self, pid_p):
        """Set current loop control parameter P

        Args:
            pid_p (int): parameter P

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
        """
        pid_p = int(pid_p)
        txdata = hex_data.int32_to_bytes_big(pid_p)
        self.__send(UTRC_RW.W, ADRA_REG.TAU_PIDP, txdata)
        ret, bus_rmsg = self.__pend(UTRC_RW.W, ADRA_REG.TAU_PIDP)
        return ret

    def get_tau_pidi(self):
        """Get current loop control parameter I

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
            pid_i (int): parameter I
        """
        self.__send(UTRC_RW.R, ADRA_REG.TAU_PIDI, None)
        ret, bus_rmsg = self.__pend(UTRC_RW.R, ADRA_REG.TAU_PIDI)
        pid_i = hex_data.bytes_to_int32_big(bus_rmsg.data[0:4])
        return ret, pid_i

    def set_tau_pidi(self, pid_i):
        """Set current loop control parameter I

        Args:
            pid_i (int): parameter I

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
        """
        pid_i = int(pid_i)
        txdata = hex_data.int32_to_bytes_big(pid_i)
        self.__send(UTRC_RW.W, ADRA_REG.TAU_PIDI, txdata)
        ret, bus_rmsg = self.__pend(UTRC_RW.W, ADRA_REG.TAU_PIDI)
        return ret

    def get_tau_smooth_cyc(self):
        """Get smoothing filter period of the current loop

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
            cyc (int): smoothing period [1-125]
        """
        self.__send(UTRC_RW.R, ADRA_REG.TAU_SMOOTH_CYC, None)
        ret, bus_rmsg = self.__pend(UTRC_RW.R, ADRA_REG.TAU_SMOOTH_CYC)
        return ret, bus_rmsg.data[0]

    def set_tau_smooth_cyc(self, value):
        """Set smoothing filter period of the current loop. The larger the smoothing period, 
        the smoother the movement and the slower the response. The range is 1 to 125

        Args:
            cyc (int): smoothing period [1-125]

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
        """
        txdata = [0]
        txdata[0] = int(value)
        self.__send(UTRC_RW.W, ADRA_REG.TAU_SMOOTH_CYC, txdata)
        ret, bus_rmsg = self.__pend(UTRC_RW.W, ADRA_REG.TAU_SMOOTH_CYC)
        return ret
