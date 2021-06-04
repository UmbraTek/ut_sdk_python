# Copyright 2020 The UmbraTek Inc. All Rights Reserved.
#
# Software License Agreement (BSD License)
#
# Author: Jimy Zhang <jimy.zhang@umbratek.com> <jimy92@163.com>
# =============================================================================
from common import hex_data
from base.arm_reg import ARM_REG
from common.utrc import UtrcClient, UtrcType, UTRC_RW, UTRC_RX_ERROR
import logging


class _ArmApiBase():
    def __init__(self, socket_fp):
        self.DB_FLG = '[UbotApi ] '
        self.__is_err = 0

        self.socket_fp = socket_fp
        self.socket_fp.flush()
        self.utrc_client = UtrcClient(self.socket_fp)

        self.tx_data = UtrcType()
        self.tx_data.state = 0x00
        self.tx_data.master_id = 0xAA
        self.tx_data.slave_id = 0x55

        self.__AXIS = 6
        self.reg = ARM_REG(self.__AXIS)

        ret, axis = self.get_axis()

        if (ret == UTRC_RX_ERROR.STATE or ret == 0):
            self.__AXIS = axis
            self.reg = ARM_REG(self.__AXIS)
        else:
            logging.error("[UbotApi ] Error: __init__ get_axis, ret: %d" % ret)
            self.__is_err = 1

    def close(self):
        """Disconnect from the arm
        """
        if self.socket_fp:
            self.socket_fp.close()
            logging.info('[UbotApi ] ubot api close')

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

    def is_err(self):
        return self.__is_err

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
        self.__send(UTRC_RW.R, self.reg.UUID, None)
        ret, utrc_rmsg = self.__pend(UTRC_RW.R, self.reg.UUID)
        uuid = utrc_rmsg.data[0:17]
        uuid = "".join([chr(x) for x in uuid])
        return ret, uuid

    def get_sw_version(self):
        """Get the software version

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
            version (string): Software version, 20-bit string
        """
        self.__send(UTRC_RW.R, self.reg.SW_VERSION, None)
        ret, utrc_rmsg = self.__pend(UTRC_RW.R, self.reg.SW_VERSION)
        version = utrc_rmsg.data[0:20]
        ver_srt = "".join([chr(x) for x in version])
        return ret, ver_srt

    def get_hw_version(self):
        """Get the hardware version

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
            version (string): Hardware version, 20-bit string
        """
        self.__send(UTRC_RW.R, self.reg.HW_VERSION, None)
        ret, utrc_rmsg = self.__pend(UTRC_RW.R, self.reg.HW_VERSION)
        version = utrc_rmsg.data[0:20]
        ver_srt = "".join([chr(x) for x in version])
        return ret, ver_srt

    def get_axis(self):
        """Get the number of arm axes

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
            axis (int): The number of arm axes
        """
        self.__send(UTRC_RW.R, self.reg.UBOT_AXIS, None)
        ret, utrc_rmsg = self.__pend(UTRC_RW.R, self.reg.UBOT_AXIS)
        axis = utrc_rmsg.data[0]
        self.__AXIS = axis
        return ret, axis

    def shutdown_system(self):
        """Power off the controller

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
        """
        txdata = [0]
        txdata[0] = int(self.reg.SYS_SHUTDOWN[0])
        self.__send(UTRC_RW.W, self.reg.SYS_SHUTDOWN, txdata)
        ret, utrc_rmsg = self.__pend(UTRC_RW.W, self.reg.SYS_SHUTDOWN)
        return ret

    def reset_err(self):
        """Reset the error state of the device

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
        """
        txdata = [0]
        txdata[0] = int(self.reg.RESET_ERR[0])
        self.__send(UTRC_RW.W, self.reg.RESET_ERR, txdata)
        ret, utrc_rmsg = self.__pend(UTRC_RW.W, self.reg.RESET_ERR)
        return ret

    def reboot_system(self):
        """Restart the system

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
        """
        txdata = [0]
        txdata[0] = int(self.reg.SYS_REBOOT[0])
        self.__send(UTRC_RW.W, self.reg.SYS_REBOOT, txdata)
        ret, utrc_rmsg = self.__pend(UTRC_RW.W, self.reg.SYS_REBOOT)
        return ret

    def erase_parm(self):
        """Restore the parameters to factory settings

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
        """
        txdata = [0]
        txdata[0] = int(self.reg.ERASE_PARM[0])
        self.__send(UTRC_RW.W, self.reg.ERASE_PARM, txdata)
        ret, utrc_rmsg = self.__pend(UTRC_RW.W, self.reg.ERASE_PARM)
        return ret

    def saved_parm(self):
        """Save the current parameter settings

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
        """
        txdata = [0]
        txdata[0] = int(self.reg.SAVED_PARM[0])
        self.__send(UTRC_RW.W, self.reg.SAVED_PARM, txdata)
        ret, utrc_rmsg = self.__pend(UTRC_RW.W, self.reg.SAVED_PARM)
        return ret

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
        self.__send(UTRC_RW.R, self.reg.MOTION_MDOE, None)
        ret, utrc_rmsg = self.__pend(UTRC_RW.R, self.reg.MOTION_MDOE)
        mode = utrc_rmsg.data[0]
        return ret, mode

    def set_motion_mode(self, mode):
        """Set the operating mode of the arm

        Args:
            mode (int): operating mode of the arm
                See the get_motion_mode

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
        """
        txdata = [0]
        txdata[0] = int(mode)
        self.__send(UTRC_RW.W, self.reg.MOTION_MDOE, txdata)
        ret, utrc_rmsg = self.__pend(UTRC_RW.W, self.reg.MOTION_MDOE)
        return ret

    def get_motion_enable(self):
        """Get the enable state of the arm

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
            value (int): There are a total of 32 bits, the 0th bit represents the enable state of the first joint brake, and so on. 
                0xFFFF means all enable 
                0x0000 means all disable 
                0x0001 means only the first joint is enabled
        """
        self.__send(UTRC_RW.R, self.reg.MOTION_ENABLE, None)
        ret, utrc_rmsg = self.__pend(UTRC_RW.R, self.reg.MOTION_ENABLE)
        value = hex_data.bytes_to_uint32_big(utrc_rmsg.data)
        return ret, value

    def set_motion_enable(self, axis, en):
        """Set the enable state of the arm

        Args:
            axis (int): Joint axis, if it is greater than the maximum number of joints, set all joints
            en (bool): 1-enable, 0-disable

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
        """
        txdata = [0] * 2
        txdata[0] = axis
        txdata[1] = en
        self.__send(UTRC_RW.W, self.reg.MOTION_ENABLE, txdata)
        ret, utrc_rmsg = self.__pend(UTRC_RW.W, self.reg.MOTION_ENABLE)
        return ret

    def get_brake_enable(self):
        """Get the enable state of the joint brake

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
            value (int): There are a total of 32 bits, the 0th bit represents the enable state of the first joint brake, and so on. 
                0xFFFF means all enable 
                0x0000 means all disable 
                0x0001 means only the first joint is enabled

        """
        self.__send(UTRC_RW.R, self.reg.BRAKE_ENABLE, None)
        ret, utrc_rmsg = self.__pend(UTRC_RW.R, self.reg.BRAKE_ENABLE)
        value = hex_data.bytes_to_uint32_big(utrc_rmsg.data)
        return ret, value

    def set_brake_enable(self, axis, en):
        """Only set the enable state of the joint brake

        Args:
            axis (int): Joint axis, if it is greater than the maximum number of joints, set all joints
            en (bool): 1-enable, 0-disable

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
        """
        txdata = [0] * 2
        txdata[0] = axis
        txdata[1] = en
        self.__send(UTRC_RW.W, self.reg.BRAKE_ENABLE, txdata)
        ret, utrc_rmsg = self.__pend(UTRC_RW.W, self.reg.BRAKE_ENABLE)
        return ret

    def get_error_code(self):
        """Get error code

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
            code (list): code[0] is error code, code[1] is warning code
        """
        self.__send(UTRC_RW.R, self.reg.ERROR_CODE, None)
        ret, utrc_rmsg = self.__pend(UTRC_RW.R, self.reg.ERROR_CODE)
        code = [0] * 2
        code[0] = hex_data.bytes_to_int8(utrc_rmsg.data[0])
        code[1] = hex_data.bytes_to_int8(utrc_rmsg.data[1])
        return ret, code

    def get_servo_msg(self):
        """Get servo status information

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
            msg (list): Servo motor communication status and operation error code
                msg[0:Axis] Servo communication status
                msg[Axis:2*Axis] Servo error code
        """
        self.__send(UTRC_RW.R, self.reg.SERVO_MSG, None)
        ret, utrc_rmsg = self.__pend(UTRC_RW.R, self.reg.SERVO_MSG)
        msg = hex_data.bytes_to_int8(utrc_rmsg.data, self.__AXIS * 2)
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
        self.__send(UTRC_RW.R, self.reg.MOTION_STATUS, None)
        ret, utrc_rmsg = self.__pend(UTRC_RW.R, self.reg.MOTION_STATUS)
        state = utrc_rmsg.data[0]
        return ret, state

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
        txdata = [0]
        txdata[0] = int(state)
        self.__send(UTRC_RW.W, self.reg.MOTION_STATUS, txdata)
        ret, utrc_rmsg = self.__pend(UTRC_RW.W, self.reg.MOTION_STATUS)
        return ret

    def get_cmd_num(self):
        """Get the current number of instruction cache

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
        """
        self.__send(UTRC_RW.R, self.reg.CMD_NUM, None)
        ret, utrc_rmsg = self.__pend(UTRC_RW.R, self.reg.CMD_NUM)
        value = hex_data.bytes_to_uint32_big(utrc_rmsg.data)
        return ret, value

    def set_cmd_num(self, value):
        """Clear the current instruction cache

        Args:
            value (int): NOT used in current version

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
        """
        txdata = hex_data.uint32_to_bytes_big(value)
        self.__send(UTRC_RW.W, self.reg.CMD_NUM, txdata)
        ret, utrc_rmsg = self.__pend(UTRC_RW.W, self.reg.CMD_NUM)
        return ret

############################################################
#                     Trajectory Api
############################################################

    def moveto_cartesian_line(self, mvpose, mvvelo, mvacc, mvtime):
        """Move to position (linear in tool-space)

        Args:
            mvpose (list): cartesian position [mm mm mm rad rad rad]
            mvvelo (float): tool speed [mm/s]
            mvacc (float): tool acceleration [mm/sˆ2]
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
        datas = hex_data.fp32_to_bytes_big(txdata, 9)
        self.__send(UTRC_RW.W, self.reg.MOVET_LINE, datas)
        ret, utrc_rmsg = self.__pend(UTRC_RW.W, self.reg.MOVET_LINE)
        return ret

    def moveto_cartesian_lineb(self, mvpose, mvvelo, mvacc, mvtime, mvradii):
        """Blend circular (in tool-space) and move linear (in tool-space) to position. 
        Accelerates to and moves with constant tool speed v.

        Args:
            mvpose (list): cartesian position [mm mm mm rad rad rad]
            mvvelo (float): tool speed [mm/s]
            mvacc (float): tool acceleration [mm/sˆ2]
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
        datas = hex_data.fp32_to_bytes_big(txdata, 10)
        self.__send(UTRC_RW.W, self.reg.MOVET_LINEB, datas)
        ret, utrc_rmsg = self.__pend(UTRC_RW.W, self.reg.MOVET_LINEB)
        return ret

    def moveto_cartesian_p2p(self):
        """NOT public in current version

        Returns:
            [type]: [description]
        """
        return 0

    def moveto_cartesian_p2pb(self):
        """NOT public in current version

        Returns:
            [type]: [description]
        """
        return 0

    def moveto_cartesian_circle(self, pose1, pose2, mvvelo, mvacc, mvtime, percent):
        """Move to position (circular in tool-space).
        TCP moves on the circular arc segment from current pose, through pose1 to pose2. 
        Accelerates to and moves with constant tool speed mvvelo.

        Args:
            pose1 (list): path cartesian position 1 [mm mm mm rad rad rad]
            pose2 (list): path cartesian position 2 [mm mm mm rad rad rad]
            mvvelo (float): tool speed [m/s]
            mvacc (float): tool acceleration [mm/sˆ2]
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
        datas = hex_data.fp32_to_bytes_big(txdata, 16)
        self.__send(UTRC_RW.W, self.reg.MOVET_CIRCLE, datas)
        ret, utrc_rmsg = self.__pend(UTRC_RW.W, self.reg.MOVET_CIRCLE)
        return ret

    def moveto_joint_line(self):
        """NOT public in current version

        Returns:
            [type]: [description]
        """
        return 0

    def moveto_joint_lineb(self):
        """NOT public in current version

        Returns:
            [type]: [description]
        """
        return 0

    def moveto_joint_p2p(self, mvjoint, mvvelo, mvacc, mvtime):
        """Move to position (linear in joint-space) When using this command, the robot must be at a standstill

        Args:
            mvjoint (list): target joint positions [rad]
            mvvelo (float): joint speed of leading axis [rad/s]
            mvacc (float): joint acceleration of leading axis [rad/sˆ2]
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
        datas = hex_data.fp32_to_bytes_big(txdata, self.__AXIS + 3)
        self.__send(UTRC_RW.W, self.reg.MOVEJ_P2P, datas)
        ret, utrc_rmsg = self.__pend(UTRC_RW.W, self.reg.MOVEJ_P2P)
        return ret

    def moveto_joint_circle(self, pose1, pose2, mvvelo, mvacc, mvtime, percent):
        """NOT public in current version

        Args:
            pose1 ([type]): [description]
            pose2 ([type]): [description]
            mvvelo ([type]): [description]
            mvacc ([type]): [description]
            mvtime ([type]): [description]
            percent ([type]): [description]

        Returns:
            [type]: [description]
        """
        return 0

    def moveto_home_p2p(self, mvvelo, mvacc, mvtime):
        """Move to position of home (linear in joint-space) When using this command, the robot must be at a standstill

        Args:
            mvvelo (float): joint speed of leading axis [rad/s]
            mvacc (float): joint acceleration of leading axis [rad/sˆ2]
            mvtime (float): NOT used in current version

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
        """
        txdata = [0] * 3
        txdata[0] = mvvelo
        txdata[1] = mvacc
        txdata[2] = mvtime
        datas = hex_data.fp32_to_bytes_big(txdata, 3)
        self.__send(UTRC_RW.W, self.reg.MOVEJ_HOME, datas)
        ret, utrc_rmsg = self.__pend(UTRC_RW.W, self.reg.MOVEJ_HOME)
        return ret

    def moveto_servoj(self, mvjoint, mvvelo, mvacc, mvtime):
        """Servo to position (linear in joint-space)
        Servo function used for online control of the robot

        Args:
            mvjoint (list): joint positions [rad]
            mvvelo (float): NOT used in current version
            mvacc (float): NOT used in current version
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
        datas = hex_data.fp32_to_bytes_big(txdata, self.__AXIS + 3)
        self.__send(UTRC_RW.W, self.reg.MOVE_SERVOJ, datas)
        ret, utrc_rmsg = self.__pend(UTRC_RW.W, self.reg.MOVE_SERVOJ)
        return ret

    def move_sleep(self, time):
        """Sleep for an amount of motion time

        Args:
            time (float): sleep time [s]

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
        """
        datas = hex_data.fp32_to_bytes_big(time)
        self.__send(UTRC_RW.W, self.reg.MOVE_SLEEP, datas)
        ret, utrc_rmsg = self.__pend(UTRC_RW.W, self.reg.MOVE_SLEEP)
        return ret

    def plan_sleep(self, time):
        """Sleep for an amount of plan time

        Args:
            time (float): sleep time [s]

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
        """
        datas = hex_data.fp32_to_bytes_big(time)
        self.__send(UTRC_RW.W, self.reg.PLAN_SLEEP, datas)
        ret, utrc_rmsg = self.__pend(UTRC_RW.W, self.reg.PLAN_SLEEP)
        return ret

############################################################
#                    Parameter Api
############################################################

    def get_tcp_jerk(self):
        """Get the jerk of the tool-space

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
            jerk (float): jerk [mm/s^3]

        """
        self.__send(UTRC_RW.R, self.reg.TCP_JERK, None)
        ret, utrc_rmsg = self.__pend(UTRC_RW.R, self.reg.TCP_JERK)
        jerk = hex_data.bytes_to_fp32_big(utrc_rmsg.data)
        return ret, jerk

    def set_tcp_jerk(self, jerk):
        """Set the jerk of the tool-space

        Args:
            jerk (float): jerk [mm/s^3]

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
        """
        txdata = hex_data.fp32_to_bytes_big(jerk)
        self.__send(UTRC_RW.W, self.reg.TCP_JERK, txdata)
        ret, utrc_rmsg = self.__pend(UTRC_RW.W, self.reg.TCP_JERK)
        return ret

    def get_tcp_maxacc(self):
        """Set the maximum acceleration of the tool-space

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
            maxacc (float): maximum acceleration [mm/s^2]
        """
        self.__send(UTRC_RW.R, self.reg.TCP_MAXACC, None)
        ret, utrc_rmsg = self.__pend(UTRC_RW.R, self.reg.TCP_MAXACC)
        maxacc = hex_data.bytes_to_fp32_big(utrc_rmsg.data)
        return ret, maxacc

    def set_tcp_maxacc(self, maxacc):
        """Set the maximum acceleration of the tool-space

        Args:
            maxacc (float): maximum acceleration [mm/s^2]

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
        """
        txdata = hex_data.fp32_to_bytes_big(maxacc)
        self.__send(UTRC_RW.W, self.reg.TCP_MAXACC, txdata)
        ret, utrc_rmsg = self.__pend(UTRC_RW.W, self.reg.TCP_MAXACC)
        return ret

    def get_joint_jerk(self):
        """Get the jerk of the joint-space

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
            jerk (float): jerk [rad/s^3]
        """
        self.__send(UTRC_RW.R, self.reg.JOINT_JERK, None)
        ret, utrc_rmsg = self.__pend(UTRC_RW.R, self.reg.JOINT_JERK)
        value = hex_data.bytes_to_fp32_big(utrc_rmsg.data)
        return ret, value

    def set_joint_jerk(self, jerk):
        """Set the jerk of the joint-space

        Args:
            jerk (float): jerk [rad/s^3]

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
        """
        txdata = hex_data.fp32_to_bytes_big(jerk)
        self.__send(UTRC_RW.W, self.reg.JOINT_JERK, txdata)
        ret, utrc_rmsg = self.__pend(UTRC_RW.W, self.reg.JOINT_JERK)
        return ret

    def get_joint_maxacc(self):
        """Get the maximum acceleration of the joint-space

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
            maxacc (float): Maximum acceleration [rad/s^2]
        """
        self.__send(UTRC_RW.R, self.reg.JOINT_MAXACC, None)
        ret, utrc_rmsg = self.__pend(UTRC_RW.R, self.reg.JOINT_MAXACC)
        maxacc = hex_data.bytes_to_fp32_big(utrc_rmsg.data)
        return ret, maxacc

    def set_joint_maxacc(self, maxacc):
        """Set the maximum acceleration of the joint-space

        Args:
            maxacc (float): maximum acceleration [rad/s^2]

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
        """
        txdata = hex_data.fp32_to_bytes_big(maxacc)
        self.__send(UTRC_RW.W, self.reg.JOINT_MAXACC, txdata)
        ret, utrc_rmsg = self.__pend(UTRC_RW.W, self.reg.JOINT_MAXACC)
        return ret

    def get_tcp_offset(self):
        """Get the coordinate offset of the end tcp tool

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
            offset (list): Offset cartesian position [mm mm mm rad rad rad]
        """
        self.__send(UTRC_RW.R, self.reg.TCP_OFFSET, None)
        ret, utrc_rmsg = self.__pend(UTRC_RW.R, self.reg.TCP_OFFSET)
        offset = hex_data.bytes_to_fp32_big(utrc_rmsg.data, 6)
        return ret, offset

    def set_tcp_offset(self, offset):
        """Set the coordinate offset of the end tcp tool

        Args:
            offset (list): Offset cartesian position [mm mm mm rad rad rad]

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
        """
        txdata = hex_data.fp32_to_bytes_big(offset, 6)
        self.__send(UTRC_RW.W, self.reg.TCP_OFFSET, txdata)
        ret, utrc_rmsg = self.__pend(UTRC_RW.W, self.reg.TCP_OFFSET)
        return ret

    def get_tcp_load(self):
        """Get payload mass and center of gravity

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
            value (list): [Mass, CoGx, CoGy, CoGz], mass in kilograms, Center of Gravity in millimeter
        """
        self.__send(UTRC_RW.R, self.reg.LOAD_PARAM, None)
        ret, utrc_rmsg = self.__pend(UTRC_RW.R, self.reg.LOAD_PARAM)
        value = hex_data.bytes_to_fp32_big(utrc_rmsg.data, 4)
        return ret, value

    def set_tcp_load(self, mass, dir):
        """Set payload mass and center of gravity
        This function must be called, when the payload weight or weight distribution changes
        when the robot picks up or puts down a heavy workpiece.
        The dir is specified as a vector, [CoGx, CoGy, CoGz], displacement,from the toolmount.

        Args:
            mass (float): mass in kilograms
            dir (list): Center of Gravity: [CoGx, CoGy, CoGz] in millimeter

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
        """
        txdata = hex_data.fp32_to_bytes_big(mass, 1)
        txdata += hex_data.fp32_to_bytes_big(dir, 3)
        self.__send(UTRC_RW.W, self.reg.LOAD_PARAM, txdata)
        ret, utrc_rmsg = self.__pend(UTRC_RW.W, self.reg.LOAD_PARAM)
        return ret

    def get_gravity_dir(self):
        """Get the direction of the acceleration experienced by the robot

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
            value (list): 3D vector, describing the direction of the gravity, relative to the base of the robot.
        """
        self.__send(UTRC_RW.R, self.reg.GRAVITY_DIR, None)
        ret, utrc_rmsg = self.__pend(UTRC_RW.R, self.reg.GRAVITY_DIR)
        value = hex_data.bytes_to_fp32_big(utrc_rmsg.data, 3)
        return ret, value

    def set_gravity_dir(self, value):
        """Set the direction of the acceleration experienced by the robot. When the robot mounting is fixed, 
        this corresponds to an accleration of gaway from the earth’s centre
        $ set_gravity_dir([0, 9.82*sin(theta), 9.82*cos(theta)]) // will set the acceleration for a robot 
        that is rotated ”theta” radians around the x-axis of the robot base coordinate system

        Args:
            value (list): 3D vector, describing the direction of the gravity, relative to the base of the robot.

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
        """
        txdata = hex_data.fp32_to_bytes_big(value, 3)
        self.__send(UTRC_RW.W, self.reg.GRAVITY_DIR, txdata)
        ret, utrc_rmsg = self.__pend(UTRC_RW.W, self.reg.GRAVITY_DIR)
        return ret

    def get_collis_sens(self):
        """Get the sensitivity of collision detection

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
            num (int): 0-5
        """
        self.__send(UTRC_RW.R, self.reg.COLLIS_SENS, None)
        ret, utrc_rmsg = self.__pend(UTRC_RW.R, self.reg.COLLIS_SENS)
        num = utrc_rmsg.data[0]
        return ret, num

    def set_collis_sens(self, num):
        """Set the sensitivity of collision detection

        Args:
            num (int): 0-5, 0 means close collision detection, sensitivity increases from 1 to 5, 
            and 5 is the highest sensitivity

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
        """
        txdata = [0]
        txdata[0] = int(num)
        self.__send(UTRC_RW.W, self.reg.COLLIS_SENS, txdata)
        ret, utrc_rmsg = self.__pend(UTRC_RW.W, self.reg.COLLIS_SENS)
        return ret

    def get_teach_sens(self):
        """Get the sensitivity of freedrive

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
            num (int): 1-5
        """
        self.__send(UTRC_RW.R, self.reg.TEACH_SENS, None)
        ret, utrc_rmsg = self.__pend(UTRC_RW.R, self.reg.TEACH_SENS)
        num = utrc_rmsg.data[0]
        return ret, num

    def set_teach_sens(self, num):
        """Set the sensitivity of freedrive

        Args:
            num (int): 1-5, sensitivity increases from 1 to 5, and 5 is the highest sensitivity

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
        """
        txdata = [0]
        txdata[0] = int(num)
        self.__send(UTRC_RW.W, self.reg.TEACH_SENS, txdata)
        ret, utrc_rmsg = self.__pend(UTRC_RW.W, self.reg.TEACH_SENS)
        return ret

############################################################
#                       State Api
############################################################

    def get_tcp_target_pos(self):
        """Get the current target tool pose
        Get the 6d pose representing the tool position and orientation specified in the base frame. 
        The calculation of this pose is based on the current target joint positions.

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
            pos (list): The current target TCP vector; ([X, Y, Z, Rx, Ry, Rz]) [mm mm mm rad rad rad]

        """
        self.__send(UTRC_RW.R, self.reg.TCP_POS_CURR, None)
        ret, utrc_rmsg = self.__pend(UTRC_RW.R, self.reg.TCP_POS_CURR)
        pose = hex_data.bytes_to_fp32_big(utrc_rmsg.data, 6)
        return ret, pose

    def get_tcp_actual_pos(self):
        """Get the current measured tool pose
        Get the 6d pose representing the tool position and orientation specified in the base frame. 
        The calculation of this pose is based on the actual robot encoder readings.

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
            pos (list): The current actual TCP vector : ([X, Y, Z, Rx, Ry, Rz]) [mm mm mm rad rad rad]
        """
        return 0, 0

    def get_joint_target_pos(self):
        """Get the desired angular position of all joints
        The angular target positions are expressed in radians and returned as a vector of length N. 
        Note that the output might differ from the output of get_joint_actual_pose(), 
        especially during cceleration and heavy loads.

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
            joints (list): The current target joint angular position vector in rad

        """
        self.__send(UTRC_RW.R, self.reg.JOINT_POS_CURR, None)
        ret, utrc_rmsg = self.__pend(UTRC_RW.R, self.reg.JOINT_POS_CURR)
        joints = hex_data.bytes_to_fp32_big(utrc_rmsg.data, self.__AXIS)
        return ret, joints

    def get_joint_actual_pos(self):
        """Get the actual angular positions of all joints
        The angular actual positions are expressed in radians and returned as a vector of length N. 
        Note that the output might differ from the output of get target joint positions(), 
        especially during cceleration and heavy loads.

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
            joints (list): The actual target joint angular position vector in rad
        """
        return 0, 0

    def get_ik(self, pose, qnear=None):
        """Inverse kinematic transformation (tool space -> joint space). 
        If qnear is defined, the solution closest to qnear is returned. 
        Otherwise, the solution closest to the current joint positions is returned.

        Args:
            pose (list): tool pose: ([X, Y, Z, Rx, Ry, Rz]) [mm mm mm rad rad rad]
            qnear (list): joint positions (Optional) [rad]

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
            joints (list): joint positions [rad]
        """
        return 0, 0

    def get_fk(self, joints):
        """Forward kinematic transformation (joint space -> tool space). 

        Args:
            joints (list): joint positions [rad]

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
            pos (list): tool pose: ([X, Y, Z, Rx, Ry, Rz]) [mm mm mm rad rad rad]
        """
        return 0, 0

    def is_joint_limit(self, joint):
        """Checks if the given joints is reachable and within the current safety limits of the robot.

        Args:
            joints (list): joint positions [rad]

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
            value [bool]: True if within limits, false otherwise
        """
        return 0, 1

    def is_tcp_limit(self, pose):
        """Checks if the given pose is reachable and within the current safety limits of the robot.
        This check considers joint limits (if the target pose is specified as joint positions), safety planes limits, 
        If a solution is found when applying the inverse kinematics to the given target TCP pose, this pose is considered reachable.

        Args:
            pose (list): Target pose: ([X, Y, Z, Rx, Ry, Rz]) [mm mm mm rad rad rad]

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
            value [bool]: True if within limits, false otherwise
        """
        return 0, 1


############################################################
#                       Rs485 Api
############################################################

    def get_utrc_int8_now(self, line, id, reg):
        """Read the 8-bit register of the device through the utrc protocol
        Communicate immediately, do not wait for the execution of other instructions in the queue
        Protocol details refer to [utrc_communication_protocol]

        Args:
            line (int): RS485 line
                2: RS485 at the end of the robotic arm
                3: RS485 for control box
            id (int): ID number of the device [1-125]
            reg (int): Device register address [0x01-0x7F]

        Returns:
            value[0] (int): Function execution result code, refer to appendix for code meaning
            value[1] (int): Data

        """
        txdata = bytes([line])
        txdata += bytes([id])
        txdata += bytes([reg])

        self.__send(UTRC_RW.R, self.reg.UTRC_INT8_NOW, txdata)
        ret, utrc_rmsg = self.__pend(UTRC_RW.R, self.reg.UTRC_INT8_NOW)
        value = utrc_rmsg.data[0:2]
        value = hex_data.bytes_to_int8(value, 2)
        if ret == 0 or ret == UTRC_RX_ERROR.STATE:
            return value[0], value[1]
        else:
            return ret, ret

    def set_utrc_int8_now(self, line, id, reg, value):
        """Write the 8-bit register of the device through the utrc protocol
        Communicate immediately, do not wait for the execution of other instructions in the queue
        Protocol details refer to [utrc_communication_protocol]

        Args:
            line (int): RS485 line
                2: RS485 at the end of the robotic arm
                3: RS485 for control box
            id (int): ID number of the device [1-125]
            reg (int): Device register address [0x01-0x7F]
            value (int): Data

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
        """
        txdata = bytes([line])
        txdata += bytes([id])
        txdata += bytes([reg])
        txdata += bytes([int(value)])

        self.__send(UTRC_RW.W, self.reg.UTRC_INT8_NOW, txdata)
        ret, utrc_rmsg = self.__pend(UTRC_RW.W, self.reg.UTRC_INT8_NOW)
        value = hex_data.bytes_to_int8(utrc_rmsg.data[0])
        if ret == 0 or ret == UTRC_RX_ERROR.STATE:
            return value
        else:
            return ret

    def get_utrc_int32_now(self, line, id, reg):
        """Read the int32 register of the device through the utrc protocol
        Communicate immediately, do not wait for the execution of other instructions in the queue
        Protocol details refer to [utrc_communication_protocol]

        Args:
            line (int): RS485 line
                2: RS485 at the end of the robotic arm
                3: RS485 for control box
            id (int): ID number of the device [1-125]
            reg (int): Device register address [0x01-0x7F]

        Returns:
            value[0] (int): Function execution result code, refer to appendix for code meaning
            value[1] (int): Data
        """
        txdata = bytes([line])
        txdata += bytes([id])
        txdata += bytes([reg])

        self.__send(UTRC_RW.R, self.reg.UTRC_INT32_NOW, txdata)
        ret, utrc_rmsg = self.__pend(UTRC_RW.R, self.reg.UTRC_INT32_NOW)
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
        Protocol details refer to [utrc_communication_protocol]

        Args:
            line (int): RS485 line
                2: RS485 at the end of the robotic arm
                3: RS485 for control box
            id (int): ID number of the device [1-125]
            reg (int): Device register address [0x01-0x7F]
            value (int): Data

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
        """
        txdata = bytes([line])
        txdata += bytes([id])
        txdata += bytes([reg])
        txdata += hex_data.int32_to_bytes_big(int(value))

        self.__send(UTRC_RW.W, self.reg.UTRC_INT32_NOW, txdata)
        ret, utrc_rmsg = self.__pend(UTRC_RW.W, self.reg.UTRC_INT32_NOW)
        value = hex_data.bytes_to_int8(utrc_rmsg.data[0])
        if ret == 0 or ret == UTRC_RX_ERROR.STATE:
            return value
        else:
            return ret

    def get_utrc_float_now(self, line, id, reg):
        """Read the float register of the device through the utrc protocol
        Communicate immediately, do not wait for the execution of other instructions in the queue
        Protocol details refer to [utrc_communication_protocol]

        Args:
            line (int): RS485 line
                2: RS485 at the end of the robotic arm
                3: RS485 for control box
            id (int): ID number of the device [1-125]
            reg (int): Device register address [0x01-0x7F]

        Returns:
            value[0] (int): Function execution result code, refer to appendix for code meaning
            value[1] (float): Data
        """
        txdata = bytes([line])
        txdata += bytes([id])
        txdata += bytes([reg])

        self.__send(UTRC_RW.R, self.reg.UTRC_FP32_NOW, txdata)
        ret, utrc_rmsg = self.__pend(UTRC_RW.R, self.reg.UTRC_FP32_NOW)
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
        Protocol details refer to [utrc_communication_protocol]

        Args:
            line (int): RS485 line
                2: RS485 at the end of the robotic arm
                3: RS485 for control box
            id (int): ID number of the device [1-125]
            reg (int): Device register address [0x01-0x7F]
            value (float): Data

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
        """
        txdata = bytes([line])
        txdata += bytes([id])
        txdata += bytes([reg])
        txdata += hex_data.fp32_to_bytes_big(value)

        self.__send(UTRC_RW.W, self.reg.UTRC_FP32_NOW, txdata)
        ret, utrc_rmsg = self.__pend(UTRC_RW.W, self.reg.UTRC_FP32_NOW)
        value = hex_data.bytes_to_int8(utrc_rmsg.data[0])
        if ret == 0 or ret == UTRC_RX_ERROR.STATE:
            return value
        else:
            return ret

    def get_utrc_int8n_now(self, line, id, reg, len):
        """Read the int8s register of the device through the utrc protocol
        Communicate immediately, do not wait for the execution of other instructions in the queue
        Protocol details refer to [utrc_communication_protocol]

        Args:
            line (int): RS485 line
                2: RS485 at the end of the robotic arm
                3: RS485 for control box
            id (int): ID number of the device [1-125]
            reg (int): Device register address [0x01-0x7F]

        Returns:
            value[0] (int): Function execution result code, refer to appendix for code meaning
            value[1] (list): Data
        """
        txdata = bytes([line])
        txdata += bytes([id])
        txdata += bytes([reg])
        txdata += bytes([len])
        self.reg.UTRC_INT8N_NOW[2] = len

        self.__send(UTRC_RW.R, self.reg.UTRC_INT8N_NOW, txdata)
        ret, utrc_rmsg = self.__pend(UTRC_RW.R, self.reg.UTRC_INT8N_NOW)
        value = utrc_rmsg.data[0:len + 1]
        value[0] = hex_data.bytes_to_int8(value[0])
        if ret == 0 or ret == UTRC_RX_ERROR.STATE:
            return value[0], value[1:len + 1]
        else:
            return ret, ret

    def set_utrc_int8n_now(self, line, id, reg, len, value):
        """Write the int8s register of the device through the utrc protocol
        Communicate immediately, do not wait for the execution of other instructions in the queue
        Protocol details refer to [utrc_communication_protocol]

        Args:
            line (int): RS485 line
                2: RS485 at the end of the robotic arm
                3: RS485 for control box
            id (int): ID number of the device [1-125]
            reg (int): Device register address [0x01-0x7F]
            value (list): Data

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
        """
        txdata = bytes([line])
        txdata += bytes([id])
        txdata += bytes([reg])
        txdata += bytes([len])
        for i in range(len):
            txdata += bytes([value[i]])
        self.reg.UTRC_INT8N_NOW[3] = len + 4

        self.__send(UTRC_RW.W, self.reg.UTRC_INT8N_NOW, txdata)
        ret, utrc_rmsg = self.__pend(UTRC_RW.W, self.reg.UTRC_INT8N_NOW)
        value = hex_data.bytes_to_int8(utrc_rmsg.data[0])
        if ret == 0 or ret == UTRC_RX_ERROR.STATE:
            return value
        else:
            return ret

    def set_utrc_int8_que(self, line, id, reg, value):
        """Write the 8-bit register of the device through the utrc protocol
        Queue communication, waiting for the completion of the execution of the instructions in the previous queue
        Protocol details refer to [utrc_communication_protocol]

        Args:
            line (int): RS485 line
                2: RS485 at the end of the robotic arm
                3: RS485 for control box
            id (int): ID number of the device [1-125]
            reg (int): Device register address [0x01-0x7F]
            value (int): Data

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
        """
        txdata = bytes([line])
        txdata += bytes([id])
        txdata += bytes([reg])
        txdata += bytes([int(value)])

        self.__send(UTRC_RW.W, self.reg.UTRC_INT8_QUE, txdata)
        ret, utrc_rmsg = self.__pend(UTRC_RW.W, self.reg.UTRC_INT8_QUE)
        if ret == UTRC_RX_ERROR.STATE:
            return 0
        else:
            return ret

    def set_utrc_int32_que(self, line, id, reg, value):
        """Write the int32 register of the device through the utrc protocol
        Queue communication, waiting for the completion of the execution of the instructions in the previous queue
        Protocol details refer to [utrc_communication_protocol]

        Args:
            line (int): RS485 line
                2: RS485 at the end of the robotic arm
                3: RS485 for control box
            id (int): ID number of the device [1-125]
            reg (int): Device register address [0x01-0x7F]
            value (int): Data

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
        """
        txdata = bytes([line])
        txdata += bytes([id])
        txdata += bytes([reg])
        txdata += hex_data.int32_to_bytes_big(int(value))

        self.__send(UTRC_RW.W, self.reg.UTRC_INT32_QUE, txdata)
        ret, utrc_rmsg = self.__pend(UTRC_RW.W, self.reg.UTRC_INT32_QUE)
        if ret == UTRC_RX_ERROR.STATE:
            return 0
        else:
            return ret

    def set_utrc_float_que(self, line, id, reg, value):
        """Write the float register of the device through the utrc protocol
        Queue communication, waiting for the completion of the execution of the instructions in the previous queue
        Protocol details refer to [utrc_communication_protocol]

        Args:
            line (int): RS485 line
                2: RS485 at the end of the robotic arm
                3: RS485 for control box
            id (int): ID number of the device [1-125]
            reg (int): Device register address [0x01-0x7F]
            value (float): Data

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
        """

        txdata = bytes([line])
        txdata += bytes([id])
        txdata += bytes([reg])
        txdata += hex_data.fp32_to_bytes_big(value)

        self.__send(UTRC_RW.W, self.reg.UTRC_FP32_QUE, txdata)
        ret, utrc_rmsg = self.__pend(UTRC_RW.W, self.reg.UTRC_FP32_QUE)
        if ret == UTRC_RX_ERROR.STATE:
            return 0
        else:
            return ret

    def set_utrc_int8n_que(self, line, id, reg, len, value):
        """Write the 8-bit register of the device through the utrc protocol
        Queue communication, waiting for the completion of the execution of the instructions in the previous queue
        Protocol details refer to [utrc_communication_protocol]

        Args:
            line (int): RS485 line
                2: RS485 at the end of the robotic arm
                3: RS485 for control box
            id (int): ID number of the device [1-125]
            reg (int): Device register address [0x01-0x7F]
            value (list): Data

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
        """
        txdata = bytes([line])
        txdata += bytes([id])
        txdata += bytes([reg])
        txdata += bytes([len])
        for i in range(len):
            txdata += bytes([value[i]])
        self.reg.UTRC_INT8N_QUE[3] = len + 4

        self.__send(UTRC_RW.W, self.reg.UTRC_INT8N_QUE, txdata)
        ret, utrc_rmsg = self.__pend(UTRC_RW.W, self.reg.UTRC_INT8N_QUE)
        if ret == UTRC_RX_ERROR.STATE:
            return 0
        else:
            return ret

    def set_pass_rs485_now(self, line, timeout_ms, tx_len, rx_len, tx_data):
        """Send data to rs485 bus and receive data
        Communicate immediately, do not wait for the execution of other instructions in the queue

        Args:
            line (int): RS485 line
                2: RS485 at the end of the robotic arm
                3: RS485 for control box
            timeout_ms (int): Receive data timeout [ms]
            tx_len (int): The length of the data sent
            rx_len (int): The length of the received data
            tx_data (list): Data sent

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
            data (list): Data received
        """
        if tx_len > 125 or rx_len > 125:
            return -99, 0, 0, 0

        txdata = bytes([line])
        txdata += bytes([timeout_ms])
        txdata += bytes([tx_len])
        txdata += bytes([rx_len])
        for i in range(tx_len):
            txdata += bytes([tx_data[i]])
        self.reg.PASS_RS485_NOW[3] = tx_len + 4
        self.reg.PASS_RS485_NOW[4] = rx_len + 2

        self.__send(UTRC_RW.W, self.reg.PASS_RS485_NOW, txdata)
        ret, utrc_rmsg = self.__pend(UTRC_RW.W, self.reg.PASS_RS485_NOW)
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
            line (int): RS485 line
                2: RS485 at the end of the robotic arm
                3: RS485 for control box
            tx_len (int): The length of the data sent
            tx_data (list): Data sent

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
        """
        if tx_len > 125:
            return -99

        txdata = bytes([line])
        txdata += bytes([tx_len])
        for i in range(tx_len):
            txdata += bytes([tx_data[i]])
        self.reg.PASS_RS485_QUE[3] = tx_len + 2

        self.__send(UTRC_RW.W, self.reg.PASS_RS485_QUE, txdata)
        ret, utrc_rmsg = self.__pend(UTRC_RW.W, self.reg.PASS_RS485_QUE)
        if ret == UTRC_RX_ERROR.STATE:
            return 0
        else:
            return ret
