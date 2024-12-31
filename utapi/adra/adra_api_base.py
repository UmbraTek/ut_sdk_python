#!/usr/bin/env python3
#
# Copyright (C) 2020 UmbraTek Inc. All Rights Reserved.
#
# Software License Agreement (BSD License)
#
# Author: Jimy Zhang <jimy.zhang@umbratek.com> <jimy92@163.com>
# =============================================================================
from utapi.base.servo_api_base import _ServoApiBase


class AdraApiBase(_ServoApiBase):
    def __init__(self, socket_fp, bus_client, tx_data):
        _ServoApiBase.__init__(self, socket_fp, bus_client, tx_data)

    def close(self):
        u"""
        Close socket
        """
        self._close()

    def connect_to_id(self, id, virtual_id=0):
        u"""Sets the connection actuator ID.

        Args:
            id (int): ID of the actuator.
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

    def get_multi_version(self):
        u"""Get the Multi-turn version.

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning.
            version (int): Multi-turn version.
        """
        return self._get_multi_version()

    def get_mech_ratio(self):
        u"""Get the reduction ratio of the mechanical reducer.

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning.
            ratio (float): reduction ratio.
        """
        return self._get_mech_ratio()

    def set_mech_ratio(self, ratio):
        u"""Set the reduction ratio of the mechanical reducer.

        Args:
            ratio (float): reduction ratio.

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning.
        """
        return self._set_mech_ratio(ratio)

    def set_com_id(self, id):
        u"""Set the id number of the actuator.

        Args:
            id (int): id number [1-125].

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning.
        """
        return self._set_com_id(id)

    def set_com_baud(self, baud):
        u"""Set communication baud rate, which can only be set to the following baud rates:
        9600, 14400, 19200, 38400, 56000,
        115200,128000,230400,256000,460800,500,000,512000,600000,750000,
        921600,1000000,1500000,2000000,2500000,3000000,3500000,4000000,4500000,
        5000000,5500000,6000000,8000000,11250000.

        Args:
            baud (int): communication baud rate.

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning.
        """
        return self._set_com_baud(baud)

    def reset_err(self):
        u"""Reset fault.

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning.
        """
        return self._reset_err()

    def restart_driver(self):
        u"""Restart the actuator.

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning.
        """
        return self._restart_driver()

    def erase_parm(self):
        u"""Restore the parameters to factory settings.

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning.
        """
        return self._erase_parm()

    def saved_parm(self):
        u"""Save the current parameter settings.

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning.
        """
        return self._saved_parm()

    ############################################################
    #                       Extension Api
    ############################################################

    def get_elec_ratio(self):
        u"""Get electronic gear ratio.

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning.
            ratio (float): reduction ratio.
        """
        return self._get_elec_ratio()

    def set_elec_ratio(self, ratio):
        u"""Set electronic gear ratio.

        Args:
            ratio (float): reduction ratio.

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning.
        """
        return self._set_elec_ratio(ratio)

    def get_motion_dir(self):
        u"""Get the direction of motion, 0: forward direction, 1: negative direction.

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning.
            dir (bool): 1 or 0.
        """
        return self._get_motion_dir()

    def set_motion_dir(self, dir):
        u"""Set the direction of motion, 0: forward direction, 1: negative direction.

        Args:
            dir (bool): 1 or 0.

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning.
        """
        return self._set_motion_dir(dir)

    def get_iwdg_cyc(self):
        u"""see the set_iwdg_cyc.

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning.
            cyc (int): Cycle time.
        """
        return self._get_iwdg_cyc()

    def set_iwdg_cyc(self, cyc):
        u"""Set the maximum interval of broadcast read commands. The unit of time is torque cycle.
        When reading actuator data in broadcast mode,
        you must send a broadcast read command within the specified period.
        If the communication interruption period exceeds the specified period, the actuator reports an error.
        If this function is not required, set it to 0 to disable it.
        Unit of period: 1 / CurrentCycle(Normal is 20 KHZ).

        For example, because the control cycle of the torque loop is 20KHz,
        if the communication detection cycle is set to 10000 and the actuator data is obtained through broadcast,
        the instruction of actuator data acquisition through broadcast must be continuously used,
        and the interval must be less than 0.5 seconds (10000/20khz).
        If the communication detection period is set to 0, the broadcast instruction can be used discontinuously.

        Args:
            cyc (int): Cycle time.

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
        """
        return self._set_iwdg_cyc(cyc)

    def get_temp_limit(self):
        u"""Get the temperature limit threshold.

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning.
            min (int): Minimum temperature alarm threshold.
            max (int): Maximum temperature alarm threshold.
        """
        return self._get_temp_limit()

    def set_temp_limit(self, min, max):
        u"""Set the temperature limit threshold,
        the minimum alarm threshold range [-20, 90],
        the maximum alarm threshold range [-20, 90], in degrees Celsius.

        Args:
            min (int): Minimum temperature alarm threshold.
            max (int): Maximum temperature alarm threshold.

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning.
        """
        return self._set_temp_limit(min, max)

    def get_volt_limit(self):
        u"""Get the voltage limit threshold.

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning.
            min (int): Minimum voltage alarm threshold.
            max (int): Maximum voltage alarm threshold.
        """
        return self._get_volt_limit()

    def set_volt_limit(self, min, max):
        u"""Set the voltage limit threshold,
        the minimum alarm threshold range [18, 55],
        the maximum alarm threshold range [18, 55], unit volt.

        Args:
            min (int): Minimum voltage alarm threshold.
            max (int): Maximum voltage alarm threshold.

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning.
        """
        return self._set_volt_limit(min, max)

    def get_curr_limit(self):
        u"""Get current limit threshold.(Not released yet, waiting for update).

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning.
            value (float): Maximum current alarm threshold.
        """
        return self._get_curr_limit()

    def set_curr_limit(self, value):
        u"""Set current limit threshold.(Not released yet, waiting for update).

        Args:
            value (float): Maximum current alarm threshold.

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning.
        """
        return self._set_curr_limit(value)

    def get_brake_delay(self):
        u"""Get the delay time for closing and opening the brake when the actuator is enabled and disabled

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning.
            ontime (uint16_t): Time to open the brake after the actuator is enabled
            offtime (uint16_t): Time to close the brake after the actuator is disabled
        """
        return self._get_brake_delay()

    def set_brake_delay(self, ontime, offtime):
        u"""Set the delay time for closing and opening the brake when the actuator is enabled and disabled.
        The unit is 1/28,000 seconds. For example, if the value is set to 14000, the delay is 0.5 seconds.
        When the actuator is enabled, the internal execution process of the actuator is as follows:
            1. Enable the motion controller of the actuator
            2. Delay ontime
            3. Close the brake
        When the actuator is disabled, the internal execution process of the actuator is as follows:
            1. Open the brake
            2. Delay offtime
            3. Disabled the motion controller of the actuator
        During the delay, no other motor commands are executed

        Args:
            ontime (uint16_t): Time to open the brake after the actuator is enabled
            offtime (uint16_t): Time to close the brake after the actuator is disabled

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning.
        """
        return self._set_brake_delay(ontime, offtime)

    def get_debug_arg(self, i):
        return self._get_debug_arg(i)

    def set_debug_arg(self, i, param):
        return self._set_debug_arg(i, param)

    ############################################################
    #                       Control Api
    ############################################################

    def get_motion_mode(self):
        u"""Get the operating mode

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning.
            mode (int): operating mode of the actuator.
                1: Position mode
                2: Speed mode
                3: Torque mode
        """
        return self._get_motion_mode()

    def set_motion_mode(self, mode):
        u"""Set the operating mode.
        When the motion mode is set, the actuator is automatically disabled and need to re-enable the motion.
        It's normally best not to use this API directly, so use these apis instead:
            1. into_motion_mode_pos()
            2. into_motion_mode_vel()
            3. into_motion_mode_tau()

        Args:
            mode (int): operating mode of the actuator.
                1: Position mode
                2: Speed mode
                3: Torque mode

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning.
        """
        return self._set_motion_mode(mode)

    def into_motion_mode_pos(self):
        return self.set_motion_mode(1)

    def into_motion_mode_vel(self):
        return self.set_motion_mode(2)

    def into_motion_mode_tau(self):
        return self.set_motion_mode(3)

    def get_motion_enable(self):
        u"""Get motion enable status

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning.
            enable (bool): 0 Disable servo, 1 Enable servo.
        """
        return self._get_motion_enable()

    def set_motion_enable(self, enable):
        u"""Set motion enable status.
        It's normally best not to use this API directly, so use these apis instead:
            1. into_motion_enable()
            2. into_motion_disable()

        Args:
            enable (bool): 0 Disable servo, 1 Enable servo.

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning.
        """
        return self._set_motion_enable(enable)

    def into_motion_enable(self):
        return self.set_motion_enable(1)

    def into_motion_disable(self):
        u"""Stops the current motion, and close the enable and brake.

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning.
        """
        return self.set_motion_enable(0)

    def into_motion_stop(self):
        u"""Stops the current motion, but does not close the enable and brake.
        It is only valid for position mode and velocity mode.

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning.
        """
        return self.set_motion_mode(21)

    def get_brake_enable(self):
        u"""Get brake enable status.

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning.
            enable (bool): 0 Disable brake, 1 Enable brake.
        """
        return self._get_brake_enable()

    def set_brake_enable(self, enable):
        u"""Set the brake enable status, enable the brake separately,
        and operate this register only when the motion is disabled,
        because the brake is automatically opened in the motion enable status.
        It's normally best not to use this API directly, so use these apis instead:
            1. into_brake_enable()
            2. into_brake_disable()

        Args:
            enable (bool): 0 Disable brake, 1 Enable brake.

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning.
        """
        return self._set_brake_enable(enable)

    def into_brake_enable(self):
        return self.set_brake_enable(1)

    def into_brake_disable(self):
        return self.set_brake_enable(0)

    def get_temp_driver(self):
        u"""Get drive temperature.

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning.
            temp (float): temperature [degrees Celsius].
        """
        return self._get_temp_driver()

    def get_temp_motor(self):
        u"""Get drive motor.

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning.
            temp (float): temperature [degrees Celsius].
        """
        return self._get_temp_motor()

    def get_bus_volt(self):
        u"""Get bus voltage.

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning.
            volt (float): volt [V].
        """
        return self._get_bus_volt()

    def get_bus_curr(self):
        u"""Get bus current.

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning.
            current (float): current [A].
        """
        return self._get_bus_curr()

    def get_multi_volt(self):
        u"""Get battery voltage of multi-turn encoder.

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning.
            volt (float): volt [V].
        """
        return self._get_multi_volt()

    def get_error_code(self):
        u"""Get error code, the meaning of the fault code is referred to the appendix <fault code>.

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning.
            code (int): error code.
        """
        return self._get_error_code()

    ############################################################
    #                       Position Api
    ############################################################

    def get_pos_target(self):
        u"""Get target position.

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning.
            pos (float): target position [rad].
        """
        return self._get_pos_target()

    def set_pos_target(self, pos):
        u"""Set target position.

        Args:
            pos (float): target position [rad].

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning.
        """
        return self._set_pos_target(pos)

    def get_pos_current(self):
        u"""Get current position.

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning.
            pos (float): current position [rad].
        """
        return self._get_pos_current()

    def get_pos_limit_min(self):
        u"""Get the minimum limit threshold of the position in position mode.

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning.
            pos (float): position [rad].
        """
        return self._get_pos_limit_min()

    def set_pos_limit_min(self, pos):
        u"""Set the minimum limit threshold of the position in position mode,
        other modes such as speed mode and current mode do not work.

        Args:
            pos (float): position [rad].

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning.
        """
        return self._set_pos_limit_min(pos)

    def get_pos_limit_max(self):
        u"""Get the maximum limit threshold of the position in position mode.

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning.
            pos (float): position [rad].
        """
        return self._get_pos_limit_max()

    def set_pos_limit_max(self, pos):
        u"""Set the maximum limit threshold of the position in position mode,
        other modes such as speed mode and current mode do not work.

        Args:
            pos (float): position [rad].

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning.
        """
        return self._set_pos_limit_max(pos)

    def get_pos_limit_diff(self):
        u"""Gets the maximum tracking error threshold for position mode.

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning.
            pos (float): position error [rad].
        """
        return self._get_pos_limit_diff()

    def set_pos_limit_diff(self, pos):
        u"""Sets the maximum tracking error threshold for position mode.
        In the position mode, the tracking error alarm threshold of the current position and the target position,
        other modes such as speed mode and current mode do not work, the unit is radians.

        Args:
            pos (float): position error [rad].

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning.
        """
        return self._set_pos_limit_diff(pos)

    def get_pos_pidp(self):
        u"""Get position loop control parameter P.

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning.
            p (float): parameter P.
        """
        return self._get_pos_pidp()

    def set_pos_pidp(self, p):
        u"""Get position loop control parameter P.

        Args:
            p (float): parameter P.

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning.
        """
        return self._set_pos_pidp(p)

    def get_pos_smooth_cyc(self):
        u"""Get smoothing filter period of the position loop.

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning.
            cyc (int): smoothing period [1-125].
        """
        return self._get_pos_smooth_cyc()

    def set_pos_smooth_cyc(self, cyc):
        u"""Set smoothing filter period of the position loop. The smoothing filter period of the position loop.
        The larger the smoothing period, the smoother the movement and the slower the response. The range is 1 to 125.

        Args:
            cyc (int): smoothing period [1-125].

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning.
        """
        return self._set_pos_smooth_cyc(cyc)

    def get_pos_adrc_param(self, i):
        u"""Get speed loop ADRC parameters.

        Args:
            i ([int]): Adrc has many parameters, which parameter needs to be get.

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning.
            value (float): parameter Adrc.
        """
        return self._get_pos_adrc_param(i)

    def set_pos_adrc_param(self, i, param):
        u"""Set position loop ADRC parameters.

        Args:
            i ([int]): Adrc has many parameters, which parameter needs to be set.
            param ([type]): [description]

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning.
        """
        return self._set_pos_adrc_param(i, param)

    def pos_cal_zero(self):
        u"""Set current position as mechanical zero, after the operation, the user needs to restart the device.

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning.
        """
        return self._pos_cal_zero()

    ############################################################
    #                       Speed Api
    ############################################################

    def get_vel_target(self):
        u"""Get target speed.

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning.
            vel (float): speed [rad/s].
        """
        return self._get_vel_target()

    def set_vel_target(self, vel):
        u"""Set target speed.

        Args:
            vel (float): speed [rad/s].

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning.
        """
        return self._set_vel_target(vel)

    def get_vel_current(self):
        u"""Get current speed.

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning.
            vel (float): speed [rad/s].
        """
        return self._get_vel_current()

    def get_vel_limit_min(self):
        u"""Get the minimum limit of the speed in speed mode and position mode.

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning.
            vel (float): speed [rad/s].
        """
        return self._get_vel_limit_min()

    def set_vel_limit_min(self, vel):
        u"""Set the minimum limit of the speed in speed mode and position mode,
        other modes such as current mode do not work.

        Args:
            vel (float): speed [rad/s].

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning.
        """
        return self._set_vel_limit_min(vel)

    def get_vel_limit_max(self):
        u"""Get maximum limit of the speed in speed mode and position mode.

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning.
            vel (float): speed [rad/s].
        """
        return self._get_vel_limit_max()

    def set_vel_limit_max(self, vel):
        u"""Set maximum limit of the speed in speed mode and position mode,
        other modes such as current mode do not work.

        Args:
            vel (float): speed [rad/s].

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning.
        """
        return self._set_vel_limit_max(vel)

    def get_vel_limit_diff(self):
        u"""Get the maximum speed following error threshold in the speed mode.
        (Not released yet, waiting for update).

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning.
            vel (float): speed [rad/s].
        """
        return self._get_vel_limit_diff()

    def set_vel_limit_diff(self, vel):
        u"""Set the maximum speed following error threshold in the speed mode,
        the tracking error alarm threshold of the current spped and the target speed,
        other modes such as position mode and current mode do not work.
        (Not released yet, waiting for update)

        Args:
            vel (float): speed [rad/s].

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning.
        """
        return self._set_vel_limit_diff(vel)

    def get_vel_pidp(self):
        u"""Get speed loop control parameter P.

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning.
            p (float): parameter P.
        """
        return self._get_vel_pidp()

    def set_vel_pidp(self, p):
        u"""Set speed loop control parameter P.

        Args:
            p (float): parameter P.

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning.
        """
        return self._set_vel_pidp(p)

    def get_vel_pidi(self):
        u"""Get speed loop control parameter I.

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning.
            pid_i (float): parameter pid_i.
        """
        return self._get_vel_pidi()

    def set_vel_pidi(self, pid_i):
        u"""Set speed loop control parameter I.

        Args:
            pid_i (float): parameter pid_i.

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning.
        """
        return self._set_vel_pidi(pid_i)

    def get_vel_smooth_cyc(self):
        u"""Get smoothing filter period of the speed loop.

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning.
            cyc (int): smoothing period [1-125].
        """
        return self._get_vel_smooth_cyc()

    def set_vel_smooth_cyc(self, cyc):
        u"""Set smoothing filter period of the speed loop. The larger the smoothing period,
        the smoother the movement and the slower the response. The range is 1 to 125.

        Args:
            cyc (int): smoothing period [1-125].

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning.
        """
        return self._set_vel_smooth_cyc(cyc)

    def get_vel_adrc_param(self, i):
        u"""Get speed loop ADRC parameters.

        Args:
            i ([int]): Adrc has many parameters, which parameter needs to be get.

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning.
            value (float): parameter Adrc.
        """
        return self._get_vel_adrc_param(i)

    def set_vel_adrc_param(self, i, param):
        u"""Set speed loop ADRC parameters.

        Args:
            i ([int]): Adrc has many parameters, which parameter needs to be set.
            param ([type]): [description].

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning.
        """
        return self._set_vel_adrc_param(i, param)

    def set_vel_output_filter_param(self, param):
        u"""Set velocity output filter parameters.

        Args:
            param ([int]): The range is 1-999,
                the larger the value, the less frequently the speed is updated (the longer the period),
                the worse the real-time performance, and the smaller the speed fluctuation.

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning.
        """
        return self._set_vel_filter_param(1, param)

    def get_vel_output_filter_param(self):
        u"""Get velocity output filter parameters.

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning.
            value (float): parameter filter.
        """
        return self._get_vel_filter_param(1)

    ############################################################
    #                       Torque Api
    ############################################################

    def get_tau_target(self):
        u"""Get target torque.

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning.
            tau (float): target torque [N.m].
        """
        return self._get_tau_target()

    def set_tau_target(self, tau):
        u"""Set target torque.

        Args:
            tau (float): target torque [N.m].

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning.
        """
        return self._set_tau_target(tau)

    def get_tau_current(self):
        u"""Get torque torque.

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning.
            tau (float): current torque [N.m].
        """
        return self._get_tau_current()

    def get_tau_limit_min(self):
        u"""Get the minimum limit threshold of the torque.

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning.
            tau (float): torque [N.m].
        """
        return self._get_tau_limit_min()

    def set_tau_limit_min(self, tau):
        u"""Set the minimum limit threshold of the torque, all modes are effective.
        Trigger alarm condition (any one) :
            1. The actual torque exceeds the limit value for 3 seconds.
            2. The actual torque exceeds 2 times the limit value for 1.5 seconds.
            3. Exceed the actual limit by 3 times, about 10 milliseconds.

        Args:
            tau (float): torque [N.m].

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning.
        """
        return self._set_tau_limit_min(tau)

    def get_tau_limit_max(self):
        u"""Get the maximum limit threshold of the torque.

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning.
            tau (float): torque [N.m].
        """
        return self._get_tau_limit_max()

    def set_tau_limit_max(self, tau):
        u"""Set the maximum limit threshold of the torque, all modes are effective.
        Trigger alarm condition (any one) :
            1. The actual torque exceeds the limit value for 3 seconds.
            2. The actual torque exceeds 2 times the limit value for 1.5 seconds.
            3. Exceed the actual limit by 3 times, about 10 milliseconds.

        Args:
            tau (float): torque [N.m].

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning.
        """
        return self._set_tau_limit_max(tau)

    def get_tau_limit_diff(self):
        u"""Get the maximum torque following error threshold in the torque mode.
        (Not released yet, waiting for update)

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning.
            tau (float): torque [N.m].
        """
        return self._get_tau_limit_diff()

    def set_tau_limit_diff(self, value):
        u"""Set the maximum torque following error threshold in the torque mode,
        the tracking error alarm threshold of the current torque and the target torque,
        other modes such as position mode and speed mode do not work.
        (Not released yet, waiting for update)

        Args:
            tau (float): torque [N.m].

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning.
        """
        return self._set_tau_limit_diff(value)

    def get_tau_pidp(self):
        u"""Get torque loop control parameter P.

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning.
            pid_p (float): parameter P.
        """
        return self._get_tau_pidp()

    def set_tau_pidp(self, pid_p):
        u"""Set torque loop control parameter P.

        Args:
            pid_p (float): parameter P.

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning.
        """
        return self._set_tau_pidp(pid_p)

    def get_tau_pidi(self):
        u"""Get torque loop control parameter I.

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning.
            pid_i (float): parameter I.
        """
        return self._get_tau_pidi()

    def set_tau_pidi(self, pid_i):
        u"""Set torque loop control parameter I.

        Args:
            pid_i (float): parameter I.

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning.
        """
        return self._set_tau_pidi(pid_i)

    def get_tau_smooth_cyc(self):
        u"""Get smoothing filter period of the torque loop.

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning.
            cyc (int): smoothing period [1-125].
        """
        return self._get_tau_smooth_cyc()

    def set_tau_smooth_cyc(self, value):
        u"""Set smoothing filter period of the torque loop. The larger the smoothing period,
        the smoother the movement and the slower the response. The range is 1 to 125.

        Args:
            cyc (int): smoothing period [1-125].

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning.
        """
        return self._set_tau_smooth_cyc(value)

    def get_tau_adrc_param(self, i):
        u"""Get torque loop ADRC parameters.

        Args:
            i (int): Adrc has many parameters, which parameter needs to be get.

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning.
            value (float): parameter Adrc.
        """
        return self._get_tau_adrc_param(i)

    def set_tau_adrc_param(self, i, param):
        u"""Set torque loop ADRC parameters.

        Args:
            i (int): Adrc has many parameters, which parameter needs to be set.
            param (type): [description]

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning.
        """
        return self._set_tau_adrc_param(i, param)

    ############################################################
    #                       Advanced Api
    ############################################################
    def set_cpos_target(self, sid, eid, pos):
        u"""Broadcast mode (one packet) sets multiple actuator target positions.

        Args:
            sid (int): ID of the first actuator.
            eid (int): ID of the last actuator.
            pos (list): Target position of actuators, in ascending order of ID number.

        Returns:
            ret (int): meaningless.
        """
        return self._set_cpos_target(sid, eid, pos)

    def set_ctau_target(self, sid, eid, tau):
        u"""Broadcast mode (one packet) sets multiple actuator target torque.

        Args:
            sid (int): ID of the first actuator.
            eid (int): ID of the last actuator.
            tau (list): Target torque of actuators, in ascending order of ID number.

        Returns:
            ret (int): meaningless.
        """
        return self._set_ctau_target(sid, eid, tau)

    def set_cpostau_target(self, sid, eid, pos, tau):
        u"""Broadcast mode (one packet) sets multiple actuator target position and feedforward torques.

        Args:
            sid (int): ID of the first actuator.
            eid (int): ID of the last actuator.
            pos (list): Target position of actuators, in ascending order of ID number.
            tau (list): Feedforward torque of actuators, in ascending order of ID number.

        Returns:
            ret (int): meaningless.
        """
        return self._set_cpostau_target(sid, eid, pos, tau)

    def set_cposvel_target(self, sid, eid, pos, vel):
        u"""Broadcast mode (one packet) sets multiple actuator target position and target speed.

        Args:
            sid (int): ID of the first actuator.
            eid (int): ID of the last actuator.
            pos (list): Target position of actuators, in ascending order of ID number.
            vel (list): Target speed of actuators, in ascending order of ID number.

        Returns:
            ret (int): meaningless.
        """
        return self._set_cposvel_target(sid, eid, pos, vel)
    
    def set_cvel_target(self, sid, eid, vel):
        u"""Broadcast mode (one packet) sets multiple actuator target speed.
        Applies to firmware after January 2025.

        Args:
            sid (int): ID of the first actuator.
            eid (int): ID of the last actuator.
            vel (list): Target speed of actuators, in ascending order of ID number.

        Returns:
            ret (int): meaningless.
        """
        return self._set_cvel_target(sid, eid, vel)

    def get_spostau_current(self):
        u"""Gets the current position of the actuator, the current torque, and number of write broadcasts received.
        At the same time, the number of received broadcast write commands is cleared to zero.

        Args:

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning.
            pos (int): Current position of actuators.
            tau (int): Current torque of actuators.
            num (int): Cnumber of write broadcasts received.
        """
        return self._get_spostau_current()

    def get_cpostau_current(self, sid, eid):
        u"""Broadcast mode (one packet) gets multiple actuator current position,
        current torque, and number of write broadcasts received.
        At the same time, the number of received broadcast write commands is cleared to zero.

        Args:
            sid (int): ID of the first actuator.
            eid (int): ID of the last actuator.

        Returns:
            ret (list): Function execution result code, refer to appendix for code meaning,
                        in ascending order of ID number.
            pos (list): Current position of actuators, in ascending order of ID number.
            tau (list): Current torque of actuators, in ascending order of ID number.
            num (list): Cnumber of write broadcasts received, in ascending order of ID number.
        """
        return self._get_cpostau_current(sid, eid)

    def get_cpvt_current(self, sid, eid):
        u"""Broadcast mode (one packet) gets multiple actuator current position, velocity,
        torque, and number of write broadcasts received.
        At the same time, the number of received broadcast write commands is cleared to zero.

        Args:
            sid (int): ID of the first actuator.
            eid (int): ID of the last actuator.

        Returns:
            ret (list): Function execution result code, refer to appendix for code meaning,
                        in ascending order of ID number.
            pos (list): Current position of actuators, in ascending order of ID number.
            vel (list): Current velocity of actuators, in ascending order of ID number.
            tau (list): Current torque of actuators, in ascending order of ID number.
            num (list): Cnumber of write broadcasts received, in ascending order of ID number.
        """
        return self._get_cpvt_current(sid, eid)

    ############################################################
    #                      Production Api
    ############################################################
    def cal_multi(self):
        u"""Calibrate the multi-turn encoder.
        Generally, after the battery is disconnected and plugged, it will report the error of
        15(multi-turn encoder zero is not aligned), or 7(battery voltage is low), or 19(encoder error).
        At this time, it is necessary to calibrate the zero of the multi-turn encoder.
        Here are the steps:	
            1. Call this API.
            2. Wait 5 seconds.(At this point, you will hear the lock ring)
            3. If the calibration is successful and there are no other errors,
            the led light will enter the breathing state, at this time, it can be re-powered.
            If the led does not breathe, the calibration has failed, or there is some other type of error,
            and the error code should be read for analysis.

        Returns:
        ret (list): Function execution result code, refer to appendix for code meaning,
                    in ascending order of ID number.
        """
        return self._cal_multi()
