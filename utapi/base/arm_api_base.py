#!/usr/bin/env python3
#
# Copyright (C) 2020 UmbraTek Inc. All Rights Reserved.
#
# Software License Agreement (BSD License)
#
# Author: Jimy Zhang <jimy.zhang@umbratek.com> <jimy92@163.com>
# =============================================================================
from utapi.common import hex_data
from utapi.base.arm_reg import ARM_REG, RS485_LINE
from utapi.base.gpio_reg import GPIO_REG
from utapi.common.utrc import UtrcClient, UtrcType, UTRC_RW, UTRC_RX_ERROR
import logging
import threading


class _ArmApiBase:
    def __init__(self, socket_fp):
        self.DB_FLG = "[UbotApi ] "
        self.__is_err = 0

        self.socket_fp = socket_fp
        self.socket_fp.flush()
        self.utrc_client = UtrcClient(self.socket_fp)
        self.mutex = threading.Lock()

        self.tx_data = UtrcType()
        self.tx_data.state = 0x00
        self.tx_data.master_id = 0xAA
        self.tx_data.slave_id = 0x55

        self.tgpio_id = 1
        self.cgpio_id = 1
        self.__AXIS = 6
        self.reg = ARM_REG(self.__AXIS)

        ret, axis = self.get_axis()

        if ret == UTRC_RX_ERROR.STATE or ret == 0:
            self.__AXIS = axis
            self.reg = ARM_REG(self.__AXIS)
        else:
            logging.error("[UbotApi ] Error: __init__ get_axis, ret: %d" % ret)
            self.__is_err = 1

    def close(self):
        """Disconnect from the arm"""
        if self.socket_fp:
            self.socket_fp.close()
            logging.info("[UbotApi ] ubot api close")

    def __send(self, rw, cmd, cmd_data):
        if self.__is_err:
            return 0

        if rw == UTRC_RW.R:
            data_wlen = cmd[1]
        else:
            data_wlen = cmd[3]

        self.tx_data.rw = rw
        self.tx_data.cmd = cmd[0]
        self.tx_data.len = data_wlen + 1

        for i in range(data_wlen):
            self.tx_data.data[i] = cmd_data[i]

        self.utrc_client.send(self.tx_data)

    def __pend(self, rw, cmd, timeout_s=1):
        if self.__is_err:
            return -999, self.tx_data

        if rw == UTRC_RW.R:
            data_rlen = cmd[2]
        else:
            data_rlen = cmd[4]
        return self.utrc_client.pend(self.tx_data, data_rlen, timeout_s)

    def __sendpend(self, rw, reg, tx_data):
        self.mutex.acquire()
        self.__send(rw, reg, tx_data)
        ret, utrc_rmsg = self.__pend(rw, reg)
        self.mutex.release()
        return ret, utrc_rmsg

    def is_err(self):
        return self.__is_err

    ############################################################
    #                       Basic Function
    ############################################################

    def __get_reg_int8(self, reg, n):
        ret, utrc_rmsg = self.__sendpend(UTRC_RW.R, reg, None)
        if n == 1:
            value = hex_data.bytes_to_int8(utrc_rmsg.data[0], n)
        else:
            value = hex_data.bytes_to_int8(utrc_rmsg.data[0:n], n)
        return ret, value

    def __set_reg_int8(self, reg, value, n):
        txdata = hex_data.int8_to_bytes_big(value, n)
        ret, utrc_rmsg = self.__sendpend(UTRC_RW.W, reg, txdata)
        return ret

    def __get_reg_int32(self, reg, n):
        ret, utrc_rmsg = self.__sendpend(UTRC_RW.R, reg, None)
        value = hex_data.bytes_to_int32_big(utrc_rmsg.data, n)
        return ret, value

    def __set_reg_int32(self, reg, value, n):
        txdata = hex_data.int32_to_bytes_big(value, n)
        ret, utrc_rmsg = self.__sendpend(UTRC_RW.W, reg, txdata)
        return ret

    def __get_reg_fp32(self, reg, n):
        ret, utrc_rmsg = self.__sendpend(UTRC_RW.R, reg, None)
        value = hex_data.bytes_to_fp32_big(utrc_rmsg.data, n)
        return ret, value

    def __set_reg_fp32(self, reg, value, n):
        datas = hex_data.fp32_to_bytes_big(value, n)
        ret, utrc_rmsg = self.__sendpend(UTRC_RW.W, reg, datas)
        return ret

    def __get_reg_fp32_fp32(self, reg, rx_n, txdata, tx_n):
        datas = hex_data.fp32_to_bytes_big(txdata, tx_n)
        ret, utrc_rmsg = self.__sendpend(UTRC_RW.R, reg, datas)
        value = hex_data.bytes_to_fp32_big(utrc_rmsg.data, rx_n)
        return ret, value

    def __get_reg_int8_fp32(self, reg, rx_n, txdata, tx_n):
        datas = hex_data.fp32_to_bytes_big(txdata, tx_n)
        ret, utrc_rmsg = self.__sendpend(UTRC_RW.R, reg, datas)
        if rx_n == 1:
            value = hex_data.bytes_to_int8(utrc_rmsg.data[0], rx_n)
        else:
            value = hex_data.bytes_to_int8(utrc_rmsg.data[0:rx_n], rx_n)
        return ret, value

    ############################################################
    #                       Basic Api
    ############################################################

    def get_uuid(self):
        """Get the uuid of the arm

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
            uuid (string): The unique code of umbratek products is also a certificate of repair and warranty
                           17-bit string
        """
        ret, uuid = self.__get_reg_int8(self.reg.UUID, 17)
        uuid = "".join([chr(x) for x in uuid])
        return ret, uuid

    def get_sw_version(self):
        """Get the software version

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
            version (string): Software version, 20-bit string
        """
        ret, version = self.__get_reg_int8(self.reg.SW_VERSION, 20)
        ver_srt = "".join([chr(x) for x in version])
        return ret, ver_srt

    def get_hw_version(self):
        """Get the hardware version

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
            version (string): Hardware version, 20-bit string
        """
        ret, version = self.__get_reg_int8(self.reg.HW_VERSION, 20)
        ver_srt = "".join([chr(x) for x in version])
        return ret, ver_srt

    def get_axis(self):
        """Get the number of arm axes

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
            axis (int): The number of arm axes
        """
        ret, axis = self.__get_reg_int8(self.reg.UBOT_AXIS, 1)
        self.__AXIS = axis
        return ret, axis

    def get_sys_autorun(self):
        """Get the arm automatically starts symbol when it is powered on.

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
            autorun (int): 0: The arm does not start automatically when it is powered on.
                           1: The arm automatically starts when it is powered on.

        """
        return self.__get_reg_int8(self.reg.SYS_AUTORUN, 1)

    def set_sys_autorun(self, autorun):
        """Set the arm to start automatically when it is powered on.

        Args:
            autorun (int): 0: The arm does not start automatically when it is powered on.
                           1: The arm automatically starts when it is powered on.

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
        """
        return self.__set_reg_int8(self.reg.SYS_AUTORUN, int(autorun), 1)

    def shutdown_system(self):
        """Power off the controller

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
        """
        return self.__set_reg_int8(self.reg.SYS_SHUTDOWN, self.reg.SYS_SHUTDOWN[0], 1)

    def reset_err(self):
        """Reset the error state of the device

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
        """
        return self.__set_reg_int8(self.reg.RESET_ERR, self.reg.RESET_ERR[0], 1)

    def reboot_system(self):
        """Restart the system

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
        """
        return self.__set_reg_int8(self.reg.SYS_REBOOT, self.reg.SYS_REBOOT[0], 1)

    def erase_parm(self):
        """Restore the parameters to factory settings

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
        """
        return self.__set_reg_int8(self.reg.ERASE_PARM, self.reg.ERASE_PARM[0], 1)

    def saved_parm(self):
        """Save the current parameter settings

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
        """
        return self.__set_reg_int8(self.reg.SAVED_PARM, self.reg.SAVED_PARM[0], 1)

    ############################################################
    #                       Control Api
    ############################################################

    def get_motion_mode(self):
        """Get the operating mode of the arm

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
            mode (int): operating mode of the arm
                0: position control mode
                1: servo motion mode, users must set to this mode first before using the moveto_servoj interface.
                2: joint teaching mode
                3: cartesian teaching mode (NOT used in current version)

        """
        return self.__get_reg_int8(self.reg.MOTION_MDOE, 1)

    def set_motion_mode(self, mode):
        """Set the operating mode of the arm

        Args:
            mode (int): operating mode of the arm
                See the get_motion_mode

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
        """
        return self.__set_reg_int8(self.reg.MOTION_MDOE, int(mode), 1)

    def get_motion_enable(self):
        """Get the enable state of the arm

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
            value (int): There are a total of 32 bits, the 1th bit represents the enable state of the first joint brake,
                the 1th bit represents the enable state of the second joint brake, and so on.
                0xFFFF means all enable
                0x0000 means all disable
                0x0001 means only the first joint is enabled
        """
        return self.__get_reg_int32(self.reg.MOTION_ENABLE, 1)

    def set_motion_enable(self, axis, en):
        """Set the enable state of the arm

        Args:
            axis (int): Joint axis, if it is greater than the maximum number of joints, set all joints
            en (bool): 1-enable, 0-disable

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
        """
        txdata = [int(axis), int(en)]
        return self.__set_reg_int8(self.reg.MOTION_ENABLE, txdata, 2)

    def get_brake_enable(self):
        """Get the enable state of the joint brake

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
            value (int): There are a total of 32 bits, the 1th bit represents the enable state of the first joint brake,
                the 2th bit represents the enable state of the second joint brake, and so on.
                0xFFFF means all enable
                0x0000 means all disable
                0x0001 means only the first joint is enabled

        """
        return self.__get_reg_int32(self.reg.BRAKE_ENABLE, 1)

    def set_brake_enable(self, axis, en):
        """Only set the enable state of the joint brake

        Args:
            axis (int): Joint axis, if it is greater than the maximum number of joints, set all joints
            en (bool): 1-enable, 0-disable

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
        """
        txdata = [int(axis), int(en)]
        return self.__set_reg_int8(self.reg.BRAKE_ENABLE, txdata, 2)

    def get_error_code(self):
        """Get error code

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
            code (list): code[0] is error code, code[1] is warning code
        """
        return self.__get_reg_int8(self.reg.ERROR_CODE, 2)

    def get_servo_msg(self):
        """Get servo status information

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
            msg (list): Servo motor communication status and operation error code
                msg[0:Axis] Servo communication status
                msg[Axis:2*Axis] Servo error code
        """
        ret, msg = self.__get_reg_int8(self.reg.SERVO_MSG, self.__AXIS * 2)
        msg_srt = " ".join([str(x) for x in msg])
        return ret, msg_srt

    def get_motion_status(self):
        """Get the running status of the arm

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
            state (int): Current running status
                1: Moving
                2: Sleeping, ready to motion
                3: Paused
                4: Stopping

        """
        return self.__get_reg_int8(self.reg.MOTION_STATUS, 1)

    def set_motion_status(self, state):
        """Set the running status of the arm

        Args:
            state (int): running status
                0: Set to ready
                3: Set to pause
                4: Set to stop

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
        """
        return self.__set_reg_int8(self.reg.MOTION_STATUS, int(state), 1)

    def get_cmd_num(self):
        """Get the current number of instruction cache

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
        """
        return self.__get_reg_int32(self.reg.CMD_NUM, 1)

    def set_cmd_num(self, value):
        """Clear the current instruction cache

        Args:
            value (int): NOT used in current version

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
        """
        return self.__set_reg_int32(self.reg.CMD_NUM, int(value), 1)

    ############################################################
    #                     Trajectory Api
    ############################################################

    def moveto_cartesian_line(self, mvpose, mvvelo, mvacc, mvtime):
        """Move to position (linear in tool-space) When using this command, the robot must be at a standstill
        Take a look at application example Demo04

        Args:
            mvpose (list): cartesian position [mm mm mm rad rad rad]
            mvvelo (float): tool speed [mm/s]
            mvacc (float): tool acceleration [mm/s^2]
            mvtime (float): NOT used in current version

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
        """
        txdata = [0] * 9
        for i in range(6):
            txdata[i] = mvpose[i]
        txdata[6] = mvvelo
        txdata[7] = mvacc
        txdata[8] = mvtime
        return self.__set_reg_fp32(self.reg.MOVET_LINE, txdata, 9)

    def moveto_cartesian_lineb(self, mvpose, mvvelo, mvacc, mvtime, mvradii):
        """Blend circular (in tool-space) and move linear (in tool-space) to position.
        Accelerates to and moves with constant tool speed v.
        The velocity is continuous between multiple position points.
        Take a look at application example Demo05

        Args:
            mvpose (list): cartesian position [mm mm mm rad rad rad]
            mvvelo (float): tool speed [mm/s]
            mvacc (float): tool acceleration [mm/s^2]
            mvtime (float): NOT used in current version
            mvradii (float): blend radius [mm]

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
        """
        txdata = [0] * 10
        for i in range(6):
            txdata[i] = mvpose[i]
        txdata[6] = mvvelo
        txdata[7] = mvacc
        txdata[8] = mvtime
        txdata[9] = mvradii
        return self.__set_reg_fp32(self.reg.MOVET_LINEB, txdata, 10)

    def moveto_cartesian_circle(self, pose1, pose2, mvvelo, mvacc, mvtime, percent):
        """Move to position (circular in tool-space).
        TCP moves on the circular arc segment from current pose, through pose1 to pose2.
        Accelerates to and moves with constant tool speed mvvelo.
        Take a look at application example Demo06

        Args:
            pose1 (list): path cartesian position 1 [mm mm mm rad rad rad]
            pose2 (list): path cartesian position 2 [mm mm mm rad rad rad]
            mvvelo (float): tool speed [m/s]
            mvacc (float): tool acceleration [mm/s^2]
            mvtime (float): NOT used in current version
            percent (float): The length of the trajectory, the unit is a percentage of the circumference,
                              which can be tens of percent or hundreds of percent

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
        """
        txdata = [0] * 16
        for i in range(6):
            txdata[i] = pose1[i]
        for i in range(6):
            txdata[6 + i] = pose2[i]
        txdata[12] = mvvelo
        txdata[13] = mvacc
        txdata[14] = mvtime
        txdata[15] = percent
        return self.__set_reg_fp32(self.reg.MOVET_CIRCLE, txdata, 16)

    def moveto_cartesian_p2p(self, mvpose, mvvelo, mvacc, mvtime):
        """"Move to position (linear in joint-space), When using this command, the robot must be at a standstill
        Take a look at application example

        Args:
            mvpose (list): cartesian position [mm mm mm rad rad rad]
            mvvelo (float): joint speed [rad/s]
            mvacc (float): joint acceleration [rad/s^2]
            mvtime (float): NOT used in current version

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
        """
        txdata = [0] * 9
        for i in range(6):
            txdata[i] = mvpose[i]
        txdata[6] = mvvelo
        txdata[7] = mvacc
        txdata[8] = mvtime
        return self.__set_reg_fp32(self.reg.MOVET_P2P, txdata, 9)

    def moveto_cartesian_p2pb(self):
        """NOT public in current version

        Returns:
            [type]: [description]
        """
        return 0

    def moveto_joint_line(self, mvjoint, mvvelo, mvacc, mvtime):
        """Move to position (linear in tool-space) When using this command, the robot must be at a standstill
            Take a look at application example

        Args:
            mvjoint (list): target joint positions [rad]
            mvvelo (float): tool speed of leading axis [mm/s]
            mvacc (float): tool acceleration of leading axis [mm/s^2]
            mvtime (float): NOT used in current version

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
        """
        txdata = [0] * (self.__AXIS + 3)
        for i in range(self.__AXIS):
            txdata[i] = mvjoint[i]
        txdata[self.__AXIS] = mvvelo
        txdata[self.__AXIS + 1] = mvacc
        txdata[self.__AXIS + 2] = mvtime
        return self.__set_reg_fp32(self.reg.MOVEJ_LINE, txdata, self.__AXIS + 3)

    def moveto_joint_lineb(self, mvjoint, mvvelo, mvacc, mvtime, mvradii):
        """Blend circular (in tool-space) and move linear (in tool-space) to position.
        Accelerates to and moves with constant tool speed v.
        The velocity is continuous between multiple position points.
        Take a look at application example

        Args:
            mvjoint(list): joint position[rad]
            mvvelo(float): tool speed[mm/s]
            mvacc(float): tool acceleration[mm/s^2]
            mvtime(float): NOT used in current version
            mvradii(float): blend radius[mm]

        Returns:
            ret(int): Function execution result code, refer to appendix for code meaning
        """
        txdata = [0] * (self.__AXIS + 4)
        for i in range(self.__AXIS):
            txdata[i] = mvjoint[i]
        txdata[self.__AXIS] = mvvelo
        txdata[self.__AXIS + 1] = mvacc
        txdata[self.__AXIS + 2] = mvtime
        txdata[self.__AXIS + 3] = mvradii
        return self.__set_reg_fp32(self.reg.MOVEJ_LINEB, txdata, self.__AXIS + 4)

    def moveto_joint_circle(self, mvjoint1, mvjoint2, mvvelo, mvacc, mvtime, percent):
        """"Move to position (circular in tool-space).
        TCP moves on the circular arc segment from current pose, through mvjoint1 to mvjoint2.
        Accelerates to and moves with constant tool speed mvvelo.
        Take a look at application example

        Args:
            mvjoint1 (list): path cartesian position 1 [rad]
            mvjoint2 (list): path cartesian position 2 [rad]
            mvvelo (float): tool speed [m/s]
            mvacc (float): tool acceleration [mm/s^2]
            mvtime (float): NOT used in current version
            percent (float): The length of the trajectory, the unit is a percentage of the circumference,
                              which can be tens of percent or hundreds of percent...

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
        """
        txdata = [0] * (self.__AXIS * 2 + 4)
        for i in range(self.__AXIS):
            txdata[i] = mvjoint1[i]
        for i in range(self.__AXIS):
            txdata[self.__AXIS + i] = mvjoint2[i]
        txdata[self.__AXIS * 2] = mvvelo
        txdata[self.__AXIS * 2 + 1] = mvacc
        txdata[self.__AXIS * 2 + 2] = mvtime
        txdata[self.__AXIS * 2 + 3] = percent
        return self.__set_reg_fp32(self.reg.MOVEJ_CIRCLE, txdata, self.__AXIS * 2 + 4)

    def moveto_joint_p2p(self, mvjoint, mvvelo, mvacc, mvtime):
        """Move to position(linear in joint - space) When using this command, the robot must be at a standstill
            Take a look at application example Demo03

        Args:
            mvjoint(list): target joint positions[rad]
            mvvelo(float): joint speed of leading axis[rad / s]
            mvacc(float): joint acceleration of leading axis[rad / sˆ2]
            mvtime(float): NOT used in current version

        Returns:
            ret(int): Function execution result code, refer to appendix for code meaning
        """
        txdata = [0] * (self.__AXIS + 3)
        for i in range(self.__AXIS):
            txdata[i] = mvjoint[i]
        txdata[self.__AXIS] = mvvelo
        txdata[self.__AXIS + 1] = mvacc
        txdata[self.__AXIS + 2] = mvtime
        return self.__set_reg_fp32(self.reg.MOVEJ_P2P, txdata, self.__AXIS + 3)

    def moveto_joint_p2pb(self):
        """NOT public in current version

        Returns:
            [type]: [description]
        """
        return 0

    def moveto_home_p2p(self, mvvelo, mvacc, mvtime):
        """Move to position of home(linear in joint - space) When using this command, the robot must be at a standstill

        Args:
            mvvelo(float): joint speed of leading axis[rad / s]
            mvacc(float): joint acceleration of leading axis[rad / sˆ2]
            mvtime(float): NOT used in current version

        Returns:
            ret(int): Function execution result code, refer to appendix for code meaning
        """
        txdata = [0] * 3
        txdata[0] = mvvelo
        txdata[1] = mvacc
        txdata[2] = mvtime
        return self.__set_reg_fp32(self.reg.MOVEJ_HOME, txdata, 3)

    def moveto_servoj(self, mvjoint, mvvelo, mvacc, mvtime):
        """NOT public in current version

        Args:
            mvjoint(list): joint positions[rad]
            mvvelo(float): NOT used in current version
            mvacc(float): NOT used in current version
            mvtime(float): NOT used in current version

        Returns:
            ret(int): Function execution result code, refer to appendix for code meaning
        """
        txdata = [0] * (self.__AXIS + 3)
        for i in range(self.__AXIS):
            txdata[i] = mvjoint[i]
        txdata[self.__AXIS] = mvvelo
        txdata[self.__AXIS + 1] = mvacc
        txdata[self.__AXIS + 2] = mvtime
        return self.__set_reg_fp32(self.reg.MOVE_SERVOJ, txdata, self.__AXIS + 3)

    def moveto_servo_joint(self, frames_num, mvjoint, mvtime):
        """Move to position(linear in joint - space) When using this command,
            And specify the time to execute to the target position
            Take a look at application example Demo08

        Args:
            frames_num(int32_t): Number of locations, up to three
            mvjoint(list): joint positions[rad], That's equal to the number of joints times the number of frames
            mvtime(list): The time to move to the target is specified in as many frames as possible[seconds]

        Returns:
            ret(int): Function execution result code, refer to appendix for code meaning
        """
        data_len = frames_num * (self.__AXIS + 1)
        txdata = [0] * data_len

        for i in range(frames_num):
            for j in range(self.__AXIS):
                txdata[i * (self.__AXIS + 1) + j] = mvjoint[i][j]
            txdata[i * (self.__AXIS + 1) + self.__AXIS] = mvtime[i]

        datas = hex_data.uint32_to_bytes_big(frames_num)
        datas += hex_data.fp32_to_bytes_big(txdata, data_len)

        self.reg.MOVES_JOINT[3] = (data_len + 1) * 4
        ret, utrc_rmsg = self.__sendpend(UTRC_RW.W, self.reg.MOVES_JOINT, datas)
        return ret

    def move_sleep(self, time):
        """Sleep for an amount of motion time

        Args:
            time(float): sleep time[s]

        Returns:
            ret(int): Function execution result code, refer to appendix for code meaning
        """
        return self.__set_reg_fp32(self.reg.MOVE_SLEEP, time, 1)

    def plan_sleep(self, time):
        """Sleep for an amount of plan time

        Args:
            time(float): sleep time[s]

        Returns:
            ret(int): Function execution result code, refer to appendix for code meaning
        """
        return self.__set_reg_fp32(self.reg.PLAN_SLEEP, time, 1)

    ############################################################
    #                    Parameter Api
    ############################################################

    def get_tcp_jerk(self):
        """Get the jerk of the tool - space

        Returns:
            ret(int): Function execution result code, refer to appendix for code meaning
            jerk(float): jerk[mm / s ^ 3]

        """
        return self.__get_reg_fp32(self.reg.TCP_JERK, 1)

    def set_tcp_jerk(self, jerk):
        """Set the jerk of the tool - space

        Args:
            jerk(float): jerk[mm / s ^ 3]

        Returns:
            ret(int): Function execution result code, refer to appendix for code meaning
        """
        return self.__set_reg_fp32(self.reg.TCP_JERK, jerk, 1)

    def get_tcp_maxacc(self):
        """Set the maximum acceleration of the tool - space

        Returns:
            ret(int): Function execution result code, refer to appendix for code meaning
            maxacc(float): maximum acceleration[mm / s ^ 2]
        """
        return self.__get_reg_fp32(self.reg.TCP_MAXACC, 1)

    def set_tcp_maxacc(self, maxacc):
        """Set the maximum acceleration of the tool - space

        Args:
            maxacc(float): maximum acceleration[mm / s ^ 2]

        Returns:
            ret(int): Function execution result code, refer to appendix for code meaning
        """
        return self.__set_reg_fp32(self.reg.TCP_MAXACC, maxacc, 1)

    def get_joint_jerk(self):
        """Get the jerk of the joint - space

        Returns:
            ret(int): Function execution result code, refer to appendix for code meaning
            jerk(float): jerk[rad / s ^ 3]
        """
        return self.__get_reg_fp32(self.reg.JOINT_JERK, 1)

    def set_joint_jerk(self, jerk):
        """Set the jerk of the joint - space

        Args:
            jerk(float): jerk[rad / s ^ 3]

        Returns:
            ret(int): Function execution result code, refer to appendix for code meaning
        """
        return self.__set_reg_fp32(self.reg.JOINT_JERK, jerk, 1)

    def get_joint_maxacc(self):
        """Get the maximum acceleration of the joint - space

        Returns:
            ret(int): Function execution result code, refer to appendix for code meaning
            maxacc(float): Maximum acceleration[rad / s ^ 2]
        """
        return self.__get_reg_fp32(self.reg.JOINT_MAXACC, 1)

    def set_joint_maxacc(self, maxacc):
        """Set the maximum acceleration of the joint - space

        Args:
            maxacc(float): maximum acceleration[rad / s ^ 2]

        Returns:
            ret(int): Function execution result code, refer to appendix for code meaning
        """
        return self.__set_reg_fp32(self.reg.JOINT_MAXACC, maxacc, 1)

    def get_tcp_offset(self):
        """Get the coordinate offset of the end tcp tool

        Returns:
            ret(int): Function execution result code, refer to appendix for code meaning
            offset(list): Offset cartesian position[mm mm mm rad rad rad]
        """
        return self.__get_reg_fp32(self.reg.TCP_OFFSET, 6)

    def set_tcp_offset(self, offset):
        """Set the coordinate offset of the end tcp tool

        Args:
            offset(list): Offset cartesian position[mm mm mm rad rad rad]

        Returns:
            ret(int): Function execution result code, refer to appendix for code meaning
        """
        return self.__set_reg_fp32(self.reg.TCP_OFFSET, offset, 6)

    def get_tcp_load(self):
        """Get payload mass and center of gravity

        Returns:
            ret(int): Function execution result code, refer to appendix for code meaning
            value(list): [Mass, CoGx, CoGy, CoGz], mass in kilograms, Center of Gravity in millimeter
        """
        return self.__get_reg_fp32(self.reg.LOAD_PARAM, 4)

    def set_tcp_load(self, mass, dir):
        """Set payload mass and center of gravity
        This function must be called, when the payload weight or weight distribution changes
        when the robot picks up or puts down a heavy workpiece.
        The dir is specified as a vector, [CoGx, CoGy, CoGz], displacement, from the toolmount.

        Args:
            mass(float): mass in kilograms
            dir(list): Center of Gravity: [CoGx, CoGy, CoGz] in millimeter

        Returns:
            ret(int): Function execution result code, refer to appendix for code meaning
        """
        txdata = [mass, dir[0], dir[1], dir[2]]
        return self.__set_reg_fp32(self.reg.LOAD_PARAM, txdata, 4)

    def get_gravity_dir(self):
        """Get the direction of the acceleration experienced by the robot

        Returns:
            ret(int): Function execution result code, refer to appendix for code meaning
            value(list): 3D vector, describing the direction of the gravity, relative to the base of the robot.
        """
        return self.__get_reg_fp32(self.reg.GRAVITY_DIR, 3)

    def set_gravity_dir(self, value):
        """Set the direction of the acceleration experienced by the robot. When the robot mounting is fixed,
        this corresponds to an accleration of gaway from the earth's centre.
        It is recommended to use this feature with Studio, which provides graphical interface Settings.

        Args:
            value(list): 3D vector, describing the direction of the gravity, relative to the base of the robot.

        Returns:
            ret(int): Function execution result code, refer to appendix for code meaning
        """
        return self.__set_reg_fp32(self.reg.GRAVITY_DIR, value, 3)

    def get_collis_sens(self):
        """NOT public in current version
        Get the sensitivity of collision detection

        Returns:
            ret(int): Function execution result code, refer to appendix for code meaning
            num(int): 0 - 5
        """
        return self.__get_reg_int8(self.reg.COLLIS_SENS, 1)

    def set_collis_sens(self, num):
        """NOT public in current version
        Set the sensitivity of collision detection

        Args:
            num(int): 0 - 5, 0 means close collision detection, sensitivity increases from 1 to 5,
            and 5 is the highest sensitivity

        Returns:
            ret(int): Function execution result code, refer to appendix for code meaning
        """
        return self.__set_reg_int8(self.reg.COLLIS_SENS, int(num), 1)

    def get_teach_sens(self):
        """Get the sensitivity of freedrive

        Returns:
            ret(int): Function execution result code, refer to appendix for code meaning
            num(int): 90 - 110
        """
        return self.__get_reg_int8(self.reg.TEACH_SENS, 1)

    def set_teach_sens(self, num):
        """Set the sensitivity of freedrive

        Args:
            num (int): 90 - 110, sensitivity increases from 90 % to 110 %, and 110 is the highest sensitivity

        Returns:
            ret(int): Function execution result code, refer to appendix for code meaning
        """
        return self.__set_reg_int8(self.reg.TEACH_SENS, int(num), 1)

    ############################################################
    #                       State Api
    ############################################################

    def get_tcp_target_pos(self):
        """Get the current target tool pose
        Get the 6d pose representing the tool position and orientation specified in the base frame.
        The calculation of this pose is based on the current target joint positions.

        Returns:
            ret(int): Function execution result code, refer to appendix for code meaning
            pos(list): The current target TCP vector; ([X, Y, Z, Rx, Ry, Rz])[mm mm mm rad rad rad]

        """
        return self.__get_reg_fp32(self.reg.TCP_POS_CURR, 6)

    def get_tcp_actual_pos(self):
        """NOT public in current version
        Get the current measured tool pose
        Get the 6d pose representing the tool position and orientation specified in the base frame.
        The calculation of this pose is based on the actual robot encoder readings.

        Returns:
            ret(int): Function execution result code, refer to appendix for code meaning
            pos(list): The current actual TCP vector: ([X, Y, Z, Rx, Ry, Rz])[mm mm mm rad rad rad]
        """
        return 0, 0

    def get_joint_target_pos(self):
        """Get the desired angular position of all joints
        The angular target positions are expressed in radians and returned as a vector of length N.
        Note that the output might differ from the output of get_joint_actual_pose(),
        especially during cceleration and heavy loads.

        Returns:
            ret(int): Function execution result code, refer to appendix for code meaning
            joints(list): The current target joint angular position vector in rad

        """
        return self.__get_reg_fp32(self.reg.JOINT_POS_CURR, self.__AXIS)

    def get_joint_actual_pos(self):
        """NOT public in current version
        Get the actual angular positions of all joints
        The angular actual positions are expressed in radians and returned as a vector of length N.
        Note that the output might differ from the output of get target joint positions(),
        especially during cceleration and heavy loads.

        Returns:
            ret(int): Function execution result code, refer to appendix for code meaning
            joints(list): The actual target joint angular position vector in rad
        """
        return 0, 0

    def get_ik(self, pose, qnear):
        """Inverse kinematic transformation(tool space -> joint space).
        qnear, the solution closest to qnear is returned.
        Otherwise, the solution closest to the current joint positions is returned.

        Args:
            pose(list): tool pose: ([X, Y, Z, Rx, Ry, Rz])[mm mm mm rad rad rad]
            qnear(list): joint positions [rad]

        Returns:
            ret(int): Function execution result code, refer to appendix for code meaning
            joints(list): joint positions[rad]
        """
        txdata = [0] * (6 + self.__AXIS)
        for i in range(6):
            txdata[i] = pose[i]
        for i in range(self.__AXIS):
            txdata[6 + i] = qnear[i]

        return self.__get_reg_fp32_fp32(self.reg.CAL_IK, self.__AXIS, txdata, 6 + self.__AXIS)

    def get_fk(self, joints):
        """Forward kinematic transformation(joint space -> tool space).

        Args:
            joints(list): joint positions[rad]

        Returns:
            ret(int): Function execution result code, refer to appendix for code meaning
            pos(list): tool pose: ([X, Y, Z, Rx, Ry, Rz])[mm mm mm rad rad rad]
        """
        txdata = [0] * self.__AXIS
        for i in range(self.__AXIS):
            txdata[i] = joints[i]
        return self.__get_reg_fp32_fp32(self.reg.CAL_FK, 6, txdata, self.__AXIS)

    def is_joint_limit(self, joints):
        """Checks if the given joints is reachable and within the current safety limits of the robot.

        Args:
            joints(list): joint positions[rad]

        Returns:
            ret(int): Function execution result code, refer to appendix for code meaning
            value[bool]: True if within limits, false otherwise
        """
        txdata = [0] * self.__AXIS
        for i in range(self.__AXIS):
            txdata[i] = joints[i]
        return self.__get_reg_int8_fp32(self.reg.IS_JOINT_LIMIT, 1, txdata, self.__AXIS)

    def is_tcp_limit(self, pose):
        """Checks if the given pose is reachable and within the current safety limits of the robot.
        This check considers joint limits(if the target pose is specified as joint positions), safety planes limits,
        If a solution is found when applying the inverse kinematics to the given target TCP pose,
        this pose is considered reachable.

        Args:
            pose(list): Target pose: ([X, Y, Z, Rx, Ry, Rz])[mm mm mm rad rad rad]

        Returns:
            ret(int): Function execution result code, refer to appendix for code meaning
            value[bool]: True if within limits, false otherwise
        """
        txdata = [0] * 6
        for i in range(6):
            txdata[i] = pose[i]
        return self.__get_reg_int8_fp32(self.reg.IS_TCP_LIMIT, 1, txdata, 6)

    ############################################################
    #                       Rs485 Api
    ############################################################

    def get_utrc_int8_now(self, line, id, reg):
        """Read the 8 - bit register of the device through the utrc protocol
        Communicate immediately, do not wait for the execution of other instructions in the queue
        Protocol details refer to[utrc_communication_protocol]

        Args:
            line(int): RS485 line
                2: RS485 at the end of the robotic arm
                3: RS485 for control box
            id(int): ID number of the device[1 - 125]
            reg(int): Device register address[0x01 - 0x7F]

        Returns:
            value[0](int): Function execution result code, refer to appendix for code meaning
            value[1](int): Data

        """
        txdata = bytes([line])
        txdata += bytes([id])
        txdata += bytes([reg])

        ret, utrc_rmsg = self.__sendpend(UTRC_RW.R, self.reg.UTRC_INT8_NOW, txdata)
        value = utrc_rmsg.data[0:2]
        value = hex_data.bytes_to_int8(value, 2)
        if ret == 0 or ret == UTRC_RX_ERROR.STATE:
            return value[0], value[1]
        else:
            return ret, ret

    def set_utrc_int8_now(self, line, id, reg, value):
        """Write the 8 - bit register of the device through the utrc protocol
        Communicate immediately, do not wait for the execution of other instructions in the queue
        Protocol details refer to[utrc_communication_protocol]

        Args:
            line(int): RS485 line
                2: RS485 at the end of the robotic arm
                3: RS485 for control box
            id(int): ID number of the device[1 - 125]
            reg(int): Device register address[0x01 - 0x7F]
            value(int): Data

        Returns:
            ret(int): Function execution result code, refer to appendix for code meaning
        """
        txdata = bytes([line])
        txdata += bytes([id])
        txdata += bytes([reg])
        txdata += bytes([int(value)])

        ret, utrc_rmsg = self.__sendpend(UTRC_RW.W, self.reg.UTRC_INT8_NOW, txdata)
        value = hex_data.bytes_to_int8(utrc_rmsg.data[0])
        if ret == 0 or ret == UTRC_RX_ERROR.STATE:
            return value
        else:
            return ret

    def get_utrc_int32_now(self, line, id, reg):
        """Read the int32 register of the device through the utrc protocol
        Communicate immediately, do not wait for the execution of other instructions in the queue
        Protocol details refer to[utrc_communication_protocol]

        Args:
            line(int): RS485 line
                2: RS485 at the end of the robotic arm
                3: RS485 for control box
            id(int): ID number of the device[1 - 125]
            reg(int): Device register address[0x01 - 0x7F]

        Returns:
            value[0](int): Function execution result code, refer to appendix for code meaning
            value[1](int): Data
        """
        txdata = bytes([line])
        txdata += bytes([id])
        txdata += bytes([reg])

        ret, utrc_rmsg = self.__sendpend(UTRC_RW.R, self.reg.UTRC_INT32_NOW, txdata)
        value = [0] * 2
        value[0] = hex_data.bytes_to_int32_big(utrc_rmsg.data[0:4])
        value[1] = hex_data.bytes_to_int32_big(utrc_rmsg.data[4:8])
        if ret == 0 or ret == UTRC_RX_ERROR.STATE:
            return value[0], value[1]
        else:
            return ret, ret

    def set_utrc_int32_now(self, line, id, reg, value):
        """Write the int32 register of the device through the utrc protocol
        Communicate immediately, do not wait for the execution of other instructions in the queue
        Protocol details refer to[utrc_communication_protocol]

        Args:
            line(int): RS485 line
                2: RS485 at the end of the robotic arm
                3: RS485 for control box
            id(int): ID number of the device[1 - 125]
            reg(int): Device register address[0x01 - 0x7F]
            value(int): Data

        Returns:
            ret(int): Function execution result code, refer to appendix for code meaning
        """
        txdata = bytes([line])
        txdata += bytes([id])
        txdata += bytes([reg])
        txdata += hex_data.int32_to_bytes_big(int(value))

        ret, utrc_rmsg = self.__sendpend(UTRC_RW.W, self.reg.UTRC_INT32_NOW, txdata)
        value = hex_data.bytes_to_int8(utrc_rmsg.data[0])
        if ret == 0 or ret == UTRC_RX_ERROR.STATE:
            return value
        else:
            return ret

    def get_utrc_float_now(self, line, id, reg):
        """Read the float register of the device through the utrc protocol
        Communicate immediately, do not wait for the execution of other instructions in the queue
        Protocol details refer to[utrc_communication_protocol]

        Args:
            line(int): RS485 line
                2: RS485 at the end of the robotic arm
                3: RS485 for control box
            id(int): ID number of the device[1 - 125]
            reg(int): Device register address[0x01 - 0x7F]

        Returns:
            value[0](int): Function execution result code, refer to appendix for code meaning
            value[1](float): Data
        """
        txdata = bytes([line])
        txdata += bytes([id])
        txdata += bytes([reg])

        ret, utrc_rmsg = self.__sendpend(UTRC_RW.R, self.reg.UTRC_FP32_NOW, txdata)
        value = [0] * 2
        value[0] = hex_data.bytes_to_fp32_big(utrc_rmsg.data[0:4])
        value[1] = hex_data.bytes_to_fp32_big(utrc_rmsg.data[4:8])
        if ret == 0 or ret == UTRC_RX_ERROR.STATE:
            return value[0], value[1]
        else:
            return ret, ret

    def set_utrc_float_now(self, line, id, reg, value):
        """Write the float register of the device through the utrc protocol
        Communicate immediately, do not wait for the execution of other instructions in the queue
        Protocol details refer to[utrc_communication_protocol]

        Args:
            line(int): RS485 line
                2: RS485 at the end of the robotic arm
                3: RS485 for control box
            id(int): ID number of the device[1 - 125]
            reg(int): Device register address[0x01 - 0x7F]
            value(float): Data

        Returns:
            ret(int): Function execution result code, refer to appendix for code meaning
        """
        txdata = bytes([line])
        txdata += bytes([id])
        txdata += bytes([reg])
        txdata += hex_data.fp32_to_bytes_big(value)

        ret, utrc_rmsg = self.__sendpend(UTRC_RW.W, self.reg.UTRC_FP32_NOW, txdata)
        value = hex_data.bytes_to_int8(utrc_rmsg.data[0])
        if ret == 0 or ret == UTRC_RX_ERROR.STATE:
            return value
        else:
            return ret

    def get_utrc_int8n_now(self, line, id, reg, len):
        """Read the int8s register of the device through the utrc protocol
        Communicate immediately, do not wait for the execution of other instructions in the queue
        Protocol details refer to[utrc_communication_protocol]

        Args:
            line(int): RS485 line
                2: RS485 at the end of the robotic arm
                3: RS485 for control box
            id(int): ID number of the device[1 - 125]
            reg(int): Device register address[0x01 - 0x7F]

        Returns:
            value[0](int): Function execution result code, refer to appendix for code meaning
            value[1](list): Data
        """
        txdata = bytes([line])
        txdata += bytes([id])
        txdata += bytes([reg])
        txdata += bytes([len])
        self.reg.UTRC_INT8N_NOW[2] = len + 1

        ret, utrc_rmsg = self.__sendpend(UTRC_RW.R, self.reg.UTRC_INT8N_NOW, txdata)
        value = utrc_rmsg.data[0:len + 1]
        value[0] = hex_data.bytes_to_int8(value[0])
        if ret == 0 or ret == UTRC_RX_ERROR.STATE:
            return value[0], value[1:len + 1]
        else:
            return ret, ret

    def set_utrc_int8n_now(self, line, id, reg, len, value):
        """Write the int8s register of the device through the utrc protocol
        Communicate immediately, do not wait for the execution of other instructions in the queue
        Protocol details refer to[utrc_communication_protocol]

        Args:
            line(int): RS485 line
                2: RS485 at the end of the robotic arm
                3: RS485 for control box
            id(int): ID number of the device[1 - 125]
            reg(int): Device register address[0x01 - 0x7F]
            value(list): Data

        Returns:
            ret(int): Function execution result code, refer to appendix for code meaning
        """
        txdata = bytes([line])
        txdata += bytes([id])
        txdata += bytes([reg])
        txdata += bytes([len])
        for i in range(len):
            txdata += bytes([value[i]])
        self.reg.UTRC_INT8N_NOW[3] = len + 4

        ret, utrc_rmsg = self.__sendpend(UTRC_RW.W, self.reg.UTRC_INT8N_NOW, txdata)
        value = hex_data.bytes_to_int8(utrc_rmsg.data[0])
        if ret == 0 or ret == UTRC_RX_ERROR.STATE:
            return value
        else:
            return ret

    def set_utrc_int8_que(self, line, id, reg, value):
        """Write the 8 - bit register of the device through the utrc protocol
        Queue communication, waiting for the completion of the execution of the instructions in the previous queue
        Protocol details refer to[utrc_communication_protocol]

        Args:
            line(int): RS485 line
                2: RS485 at the end of the robotic arm
                3: RS485 for control box
            id(int): ID number of the device[1 - 125]
            reg(int): Device register address[0x01 - 0x7F]
            value(int): Data

        Returns:
            ret(int): Function execution result code, refer to appendix for code meaning
        """
        txdata = bytes([line])
        txdata += bytes([id])
        txdata += bytes([reg])
        txdata += bytes([int(value)])

        ret, utrc_rmsg = self.__sendpend(UTRC_RW.W, self.reg.UTRC_INT8_QUE, txdata)
        if ret == UTRC_RX_ERROR.STATE:
            return 0
        else:
            return ret

    def set_utrc_int32_que(self, line, id, reg, value):
        """Write the int32 register of the device through the utrc protocol
        Queue communication, waiting for the completion of the execution of the instructions in the previous queue
        Protocol details refer to[utrc_communication_protocol]

        Args:
            line(int): RS485 line
                2: RS485 at the end of the robotic arm
                3: RS485 for control box
            id(int): ID number of the device[1 - 125]
            reg(int): Device register address[0x01 - 0x7F]
            value(int): Data

        Returns:
            ret(int): Function execution result code, refer to appendix for code meaning
        """
        txdata = bytes([line])
        txdata += bytes([id])
        txdata += bytes([reg])
        txdata += hex_data.int32_to_bytes_big(int(value))

        ret, utrc_rmsg = self.__sendpend(UTRC_RW.W, self.reg.UTRC_INT32_QUE, txdata)
        if ret == UTRC_RX_ERROR.STATE:
            return 0
        else:
            return ret

    def set_utrc_float_que(self, line, id, reg, value):
        """Write the float register of the device through the utrc protocol
        Queue communication, waiting for the completion of the execution of the instructions in the previous queue
        Protocol details refer to[utrc_communication_protocol]

        Args:
            line(int): RS485 line
                2: RS485 at the end of the robotic arm
                3: RS485 for control box
            id(int): ID number of the device[1 - 125]
            reg(int): Device register address[0x01 - 0x7F]
            value(float): Data

        Returns:
            ret(int): Function execution result code, refer to appendix for code meaning
        """

        txdata = bytes([line])
        txdata += bytes([id])
        txdata += bytes([reg])
        txdata += hex_data.fp32_to_bytes_big(value)

        ret, utrc_rmsg = self.__sendpend(UTRC_RW.W, self.reg.UTRC_FP32_QUE, txdata)
        if ret == UTRC_RX_ERROR.STATE:
            return 0
        else:
            return ret

    def set_utrc_int8n_que(self, line, id, reg, len, value):
        """Write the 8 - bit register of the device through the utrc protocol
        Queue communication, waiting for the completion of the execution of the instructions in the previous queue
        Protocol details refer to[utrc_communication_protocol]

        Args:
            line(int): RS485 line
                2: RS485 at the end of the robotic arm
                3: RS485 for control box
            id(int): ID number of the device[1 - 125]
            reg(int): Device register address[0x01 - 0x7F]
            value(list): Data

        Returns:
            ret(int): Function execution result code, refer to appendix for code meaning
        """
        txdata = bytes([line])
        txdata += bytes([id])
        txdata += bytes([reg])
        txdata += bytes([len])
        for i in range(len):
            txdata += bytes([value[i]])
        self.reg.UTRC_INT8N_QUE[3] = len + 4

        ret, utrc_rmsg = self.__sendpend(UTRC_RW.W, self.reg.UTRC_INT8N_QUE, txdata)
        if ret == UTRC_RX_ERROR.STATE:
            return 0
        else:
            return ret

    def set_pass_rs485_now(self, line, timeout_ms, tx_len, rx_len, tx_data):
        """Send data to rs485 bus and receive data
        Communicate immediately, do not wait for the execution of other instructions in the queue

        Args:
            line(int): RS485 line
                2: RS485 at the end of the robotic arm
                3: RS485 for control box
            timeout_ms(int): Receive data timeout[ms]
            tx_len(int): The length of the data sent
            rx_len(int): The length of the received data
            tx_data(list): Data sent

        Returns:
            ret(int): Function execution result code, refer to appendix for code meaning
            data(list): Data received
        """
        if tx_len > 125 or rx_len > 125:
            return -991, 0, 0, 0

        txdata = bytes([line])
        txdata += bytes([timeout_ms])
        txdata += bytes([tx_len])
        txdata += bytes([rx_len])
        for i in range(tx_len):
            txdata += bytes([tx_data[i]])
        self.reg.PASS_RS485_NOW[3] = tx_len + 4
        self.reg.PASS_RS485_NOW[4] = rx_len + 2

        ret, utrc_rmsg = self.__sendpend(UTRC_RW.W, self.reg.PASS_RS485_NOW, txdata)
        value = utrc_rmsg.data[0:rx_len + 2]
        value[0] = hex_data.bytes_to_int8(value[0])
        if ret == 0 or ret == UTRC_RX_ERROR.STATE:
            return value[0], value[1:rx_len + 2]
        else:
            return ret, ret

    def set_pass_rs485_que(self, line, tx_len, tx_data):
        """Send data to rs485 bus
        Queue communication, waiting for the completion of the execution of the instructions in the previous queue

        Args:
            line(int): RS485 line
                2: RS485 at the end of the robotic arm
                3: RS485 for control box
            tx_len(int): The length of the data sent
            tx_data(list): Data sent

        Returns:
            ret(int): Function execution result code, refer to appendix for code meaning
        """
        if tx_len > 125:
            return -99

        txdata = bytes([line])
        txdata += bytes([tx_len])
        for i in range(tx_len):
            txdata += bytes([tx_data[i]])
        self.reg.PASS_RS485_QUE[3] = tx_len + 2

        ret, utrc_rmsg = self.__sendpend(UTRC_RW.W, self.reg.PASS_RS485_QUE, txdata)
        if ret == UTRC_RX_ERROR.STATE:
            return 0
        else:
            return ret

    def get_utrc_u8float_now(self, line, id, reg, num):
        """Read the float list register of the device through the utrc protocol
        Communicate immediately, do not wait for the execution of other instructions in the queue
        Protocol details refer to[utrc_communication_protocol]

        Args:
            line(int): RS485 line
                2: RS485 at the end of the robotic arm
                3: RS485 for control box
            id(int): ID number of the device[1 - 125]
            reg(int): Device register address[0x01 - 0x7F]
            num([uint8_t]): The number of values in a register

        Returns:
            ret(int): Function execution result code, refer to appendix for code meaning
            value([float]): Data
        """

        txdata = bytes([line])
        txdata += bytes([id])
        txdata += bytes([reg])
        txdata += bytes([num])

        ret, utrc_rmsg = self.__sendpend(UTRC_RW.R, self.reg.UTRC_U8FP32_NOW, txdata)
        value = [0] * 2
        value[0] = hex_data.bytes_to_fp32_big(utrc_rmsg.data[0:4])
        value[1] = hex_data.bytes_to_fp32_big(utrc_rmsg.data[4:8])
        if ret == 0 or ret == UTRC_RX_ERROR.STATE:
            return value[0], value[1]
        else:
            return ret, ret

    def set_utrc_u8float_now(self, line, id, reg, num, value):
        """Write the float list register of the device through the utrc protocol
        Communicate immediately, do not wait for the execution of other instructions in the queue
        Protocol details refer to[utrc_communication_protocol]

        Args:
            line(int): RS485 line
                2: RS485 at the end of the robotic arm
                3: RS485 for control box
            id(int): ID number of the device[1 - 125]
            reg(int): Device register address[0x01 - 0x7F]
            num([uint8_t]): The number of values in a register
            value([type]): Data

        Returns:
            ret(int): Function execution result code, refer to appendix for code meaning
        """

        txdata = bytes([line])
        txdata += bytes([id])
        txdata += bytes([reg])
        txdata += bytes([num])
        txdata += hex_data.fp32_to_bytes_big(value)

        ret, utrc_rmsg = self.__sendpend(UTRC_RW.W, self.reg.UTRC_U8FP32_NOW, txdata)
        value = hex_data.bytes_to_int8(utrc_rmsg.data[0])
        if ret == 0 or ret == UTRC_RX_ERROR.STATE:
            return value
        else:
            return ret

    def get_utrc_nfloat_now(self, line, id, reg, len):
        """Read the floats register of the device through the utrc protocol
        Communicate immediately, do not wait for the execution of other instructions in the queue
        Protocol details refer to[utrc_communication_protocol]

        Args:
            line(int): RS485 line
                2: RS485 at the end of the robotic arm
                3: RS485 for control box
            id(int): ID number of the device[1 - 125]
            reg(int): Device register address[0x01 - 0x7F]

        Returns:
            value[0](int): Function execution result code, refer to appendix for code meaning
            value[1](list): Data
        """
        txdata = bytes([line])
        txdata += bytes([id])
        txdata += bytes([reg])
        txdata += bytes([len])
        self.reg.UTRC_FP32N_NOW[2] = len * 4 + 4

        ret, utrc_rmsg = self.__sendpend(UTRC_RW.R, self.reg.UTRC_FP32N_NOW, txdata)
        rx_data = hex_data.bytes_to_fp32_big(utrc_rmsg.data, len + 1)
        if ret == 0 or ret == UTRC_RX_ERROR.STATE:
            return rx_data[0], rx_data[1:len + 1]
        else:
            return ret, ret

    ############################################################
    #                       GPIO Api
    ############################################################
    def __get_gpio_in(self, line, id):
        """Gets the input value for the GPIO module

        Args:
            line(int): RS485 line
                2: RS485 at the end of the robotic arm
                3: RS485 for control box
            id(int): ID number of the device[1 - 125]

        Returns:
            ret(int): Function execution result code, refer to appendix for code meaning
            data(list): Data received
                data[0]: Functional status
                data[1]: digit I / O input
                data[2]: dac num
                data[2 - N]: dac value
        """

        txdata = bytes([line])
        txdata += bytes([id])

        ret, utrc_rmsg = self.__sendpend(UTRC_RW.R, self.reg.GPIO_IN, txdata)
        value = [0] * 20
        value[0] = hex_data.bytes_to_int8(utrc_rmsg.data[0])
        value[1] = hex_data.bytes_to_uint32_big(utrc_rmsg.data[1:5])  # fun
        value[2] = hex_data.bytes_to_uint32_big(utrc_rmsg.data[5:9])  # digit
        value[3] = utrc_rmsg.data[9]
        for i in range(value[3]):
            value[4 + i] = hex_data.bytes_to_fp32_big(utrc_rmsg.data[(10 + i * 4):(14 + i * 4)])  # digit
        if ret == 0 or ret == UTRC_RX_ERROR.STATE:
            return value[0], value[1:]
        else:
            return ret, ret

    def __get_gpio_ou(self, line, id):
        """Gets the output value of the GPIO module

        Args:
            line(int): RS485 line
                2: RS485 at the end of the robotic arm
                3: RS485 for control box
            id(int): ID number of the device[1 - 125]

        Returns:
            ret(int): Function execution result code, refer to appendix for code meaning
            data(list): Data received
                data[0]: Functional status
                data[1]: digit I / O output
                data[2]: adc num
                data[2 - N]: adc value
        """

        txdata = bytes([line])
        txdata += bytes([id])

        ret, utrc_rmsg = self.__sendpend(UTRC_RW.R, self.reg.GPIO_OU, txdata)
        value = [0] * 20
        value[0] = hex_data.bytes_to_int8(utrc_rmsg.data[0])
        value[1] = hex_data.bytes_to_uint32_big(utrc_rmsg.data[1:5])  # fun
        value[2] = hex_data.bytes_to_uint32_big(utrc_rmsg.data[5:9])  # digit
        value[3] = utrc_rmsg.data[9]
        for i in range(value[3]):
            value[4 + i] = hex_data.bytes_to_fp32_big(utrc_rmsg.data[(10 + i * 4):(14 + i * 4)])  # digit
        if ret == 0 or ret == UTRC_RX_ERROR.STATE:
            return value[0], value[1:]
        else:
            return ret, ret

    ############################################################
    #                    End-Tool GPIO Api
    ############################################################
    def get_tgpio_in(self):
        """Gets the input value of the end - tool GPIO module

        Returns:
            ret(int): Function execution result code, refer to appendix for code meaning
            data(list): Data received
                data[0]: controller function
                data[1]: digit I / O input
                data[2]: dac num
                data[2 - N]: dac value
        """
        return self.__get_gpio_in(RS485_LINE.TGPIO, self.tgpio_id)

    def get_tgpio_out(self):
        """Gets the output value of the end - tool GPIO module

        Returns:
            ret(int): Function execution result code, refer to appendix for code meaning
            data(list): Data received
                data[0]: gpio function
                data[1]: digit I / O output
                data[2]: adc num
                data[2 - N]: adc value
        """
        return self.__get_gpio_ou(RS485_LINE.TGPIO, self.tgpio_id)

    def set_tgpio_digit_out(self, value):
        """Set the end - tool GPIO module to output digital I / O
        The higher 16 bits are the I / O to be set, and the lower 16 bits are the value to be set

        Args:
            value(uint32_t): Digital I / O output value
                For example: 0x00010001 = > Set GPIO 1 to high
                For example: 0x00030003 = > Set GPIO 1 and 2 to high

        Returns:
            ret(int): Function execution result code, refer to appendix for code meaning
        """
        return self.set_utrc_int32_now(RS485_LINE.TGPIO, self.tgpio_id, 0x13, int(value))

    def get_tgpio_uuid(self):
        """Get the UUID of the end - tool GPIO module

        Returns:
            ret(int): Function execution result code, refer to appendix for code meaning
            uuid(string): The unique code of umbratek products is also a certificate of repair and warranty
                           12 - bit string
        """
        ret, data = self.get_utrc_int8n_now(RS485_LINE.TGPIO, self.tgpio_id, GPIO_REG.UUID[0], GPIO_REG.UUID[2])
        print(ret)
        print(data)
        uuid = data[0:12]
        string = ""
        for i in uuid:
            string += "{0:0>2}".format(str(hex(i))[2:])
        return ret, string

    def get_tgpio_sw_version(self):
        """Get the software version of the end - tool GPIO module

        Returns:
            ret(int): Function execution result code, refer to appendix for code meaning
            version(string): Software version, 12 - bit string
        """
        ret, data = self.get_utrc_int8n_now(RS485_LINE.TGPIO, self.tgpio_id, GPIO_REG.SW_VERSION[0],
                                            GPIO_REG.SW_VERSION[2])
        version = data[0:12]
        print("get_tgpio_sw_version: ")
        print(version)
        version = "".join([chr(x) for x in version])
        print(version)
        return ret, version

    def get_tgpio_hw_version(self):
        """Get the hardware version of the end - tool GPIO module

        Returns:
            ret(int): Function execution result code, refer to appendix for code meaning
            version(string): Hardware version, 12 - bit string
        """
        ret, data = self.get_utrc_int8n_now(RS485_LINE.TGPIO, self.tgpio_id, GPIO_REG.HW_VERSION[0],
                                            GPIO_REG.HW_VERSION[2])
        version = data[0:12]
        print("get_tgpio_hw_version: ")
        print(version)
        string = ""
        for i in version:
            string += "{0:0>2}".format(str(hex(i))[2:])
        print(string)
        return ret, string

    ############################################################
    #                    Controller GPIO Api
    ############################################################
    def get_cgpio_in(self):
        """Gets the input value of the controller GPIO module

        Returns:
            ret(int): Function execution result code, refer to appendix for code meaning
            data(list): Data received
                data[0]: controller function
                data[1]: digit I / O input
                data[2]: dac num
                data[2 - N]: dac value
        """
        return self.__get_gpio_in(RS485_LINE.CGPIO, self.cgpio_id)

    def get_cgpio_out(self):
        """Gets the output value of the controller GPIO module

        Returns:
            ret(int): Function execution result code, refer to appendix for code meaning
            data(list): Data received
                data[0]: gpio function
                data[1]: digit I / O output
                data[2]: adc num
                data[2 - N]: adc value
        """
        return self.__get_gpio_ou(RS485_LINE.CGPIO, self.cgpio_id)

    def set_cgpio_digit_out(self, value):
        """Set the controller GPIO module to output digital I / O
        The higher 16 bits are the I / O to be set, and the lower 16 bits are the value to be set

        Args:
            value(uint32_t): Digital I / O output value
                For example: 0x00010001 = > Set GPIO 1 to high
                For example: 0x00030003 = > Set GPIO 1 and 2 to high

        Returns:
            ret(int): Function execution result code, refer to appendix for code meaning
        """
        return self.set_utrc_int32_now(RS485_LINE.CGPIO, self.cgpio_id, GPIO_REG.DIGITOU[0], int(value))

    def get_cgpio_uuid(self):
        """Get the UUID of the NTRO Controller

        Returns:
            ret(int): Function execution result code, refer to appendix for code meaning
            uuid(string): The unique code of umbratek products is also a certificate of repair and warranty
                           12 - bit string
        """
        ret, data = self.get_utrc_int8n_now(RS485_LINE.CGPIO, self.cgpio_id, GPIO_REG.UUID[0], GPIO_REG.UUID[2])
        print(ret)
        print(data)
        uuid = data[0:12]
        string = ""
        for i in uuid:
            string += "{0:0>2}".format(str(hex(i))[2:])
        return ret, string

    def get_cgpio_sw_version(self):
        """Get the software version of the NTRO Controller

        Returns:
            ret(int): Function execution result code, refer to appendix for code meaning
            version(string): Software version, 12 - bit string
        """
        ret, data = self.get_utrc_int8n_now(RS485_LINE.CGPIO, self.cgpio_id, GPIO_REG.SW_VERSION[0],
                                            GPIO_REG.SW_VERSION[2])
        version = data[0:12]
        print("get_cgpio_sw_version: ")
        print(version)
        version = "".join([chr(x) for x in version])
        print(version)
        return ret, version

    def get_cgpio_hw_version(self):
        """Get the hardware version of the NTRO Controller

        Returns:
            ret(int): Function execution result code, refer to appendix for code meaning
            version(string): Hardware version, 12 - bit string
        """
        ret, data = self.get_utrc_int8n_now(RS485_LINE.CGPIO, self.cgpio_id, GPIO_REG.HW_VERSION[0],
                                            GPIO_REG.HW_VERSION[2])
        version = data[0:12]
        print("get_cgpio_hw_version: ")
        print(version)
        string = ""
        for i in version:
            string += "{0:0>2}".format(str(hex(i))[2:])
        print(string)
        return ret, string
