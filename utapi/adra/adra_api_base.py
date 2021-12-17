# Copyright 2020 The UmbraTek Inc. All Rights Reserved.
#
# Software License Agreement (BSD License)
#
# Author: Jimy Zhang <jimy.zhang@umbratek.com> <jimy92@163.com>
# =============================================================================
from base.servo_api_base import _ServoApiBase


class AdraApiBase(_ServoApiBase):
    def __init__(self, socket_fp, bus_client, tx_data):
        _ServoApiBase.__init__(self, socket_fp, bus_client, tx_data)

    def close(self):
        """Close socket"""
        self._close()

    def connect_to_id(self, id, virtual_id=0):
        """Connect actuator ID

        Args:
            id (int): The ID number of the actuator
            virtual_id (int, optional): Only used for debugging. Defaults to 0.
        """
        return self._connect_to_id(id, virtual_id)

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
        return self._get_uuid()

    def get_sw_version(self):
        """Get the software version

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
            version (string): Software version, 12-bit string
        """
        return self._get_sw_version()

    def get_hw_version(self):
        """Get the hardware version

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
            version (string): Hardware version, 12-bit string
        """
        return self._get_hw_version()

    def get_multi_version(self):
        """Get the Multi-turn version

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
            version (int): Multi-turn version
        """
        return self._get_multi_version()

    def get_mech_ratio(self):
        """Get the reduction ratio of the mechanical reducer

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
            ratio (float): reduction ratio
        """
        return self._get_mech_ratio()

    def set_mech_ratio(self, ratio):
        """Set the reduction ratio of the mechanical reducer

        Args:
            ratio (float): reduction ratio

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
        """
        return self._set_mech_ratio(ratio)

    def set_com_id(self, id):
        """Set the id number of the device

        Args:
            id (int): id number [1-125]

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
        """
        return self._set_com_id(id)

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
        return self._set_com_baud(baud)

    def reset_err(self):
        """Reset fault

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
        """
        return self._reset_err()

    def restart_driver(self):
        """Restart the device

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
        """
        return self._restart_driver()

    def erase_parm(self):
        """Restore the parameters to factory settings

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
        """
        return self._erase_parm()

    def saved_parm(self):
        """Save the current parameter settings

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
        """
        return self._saved_parm()

    ############################################################
    #                       Ectension Api
    ############################################################

    def get_elec_ratio(self):
        """Get electronic gear ratio

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
            ratio (float): reduction ratio
        """
        return self._get_elec_ratio()

    def set_elec_ratio(self, ratio):
        """Set electronic gear ratio

        Args:
            ratio (float): reduction ratio

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
        """
        return self._set_elec_ratio(ratio)

    def get_motion_dir(self):
        """Get the direction of motion, 0: positive direction, 1: negative direction

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
            dir (bool): 1 or 0
        """
        return self._get_motion_dir()

    def set_motion_dir(self, dir):
        """Set the direction of motion, 0: positive direction, 1: negative direction

        Args:
            dir (bool): 1 or 0

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
        """
        return self._set_motion_dir(dir)

    def get_temp_limit(self):
        """Get the temperature limit threshold

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
            min (int): Minimum temperature alarm threshold
            max (int): Maximum temperature alarm threshold
        """
        return self._get_temp_limit()

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
        return self._set_temp_limit(min, max)

    def get_volt_limit(self):
        """Get the voltage limit threshold

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
            min (int): Minimum voltage alarm threshold
            max (int): Maximum voltage alarm threshold
        """
        return self._get_volt_limit()

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
        return self._set_volt_limit(min, max)

    def get_curr_limit(self):
        """Get current limit threshold

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
            value (float): Maximum current alarm threshold
        """
        return self._get_curr_limit()

    def set_curr_limit(self, value):
        """Set current limit threshold

        Args:
            value (float): Maximum current alarm threshold

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
        """
        return self._set_curr_limit(value)


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
        return self._get_motion_mode()

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
        return self._set_motion_mode(mode)

    def get_motion_enable(self):
        """Get motion enable status

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
            enable (bool): 0 Disable servo, 1 Enable servo
        """
        return self._get_motion_enable()

    def set_motion_enable(self, enable):
        """Set motion enable status

        Args:
            enable (bool): 0 Disable servo, 1 Enable servo

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
        """
        return self._set_motion_enable(enable)

    def get_brake_enable(self):
        """Get brake enable status

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
            enable (bool): 0 Disable brake, 1 Enable brake
        """
        return self._get_brake_enable()

    def set_brake_enable(self, enable):
        """Set the brake enable state, enable the brake separately, and operate this register only when the motion is disabled,
        because the brake is automatically opened in the motion enable state.

        Args:
            enable (bool): 0 Disable brake, 1 Enable brake

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
        """
        return self._set_brake_enable(enable)

    def get_temp_driver(self):
        """Get drive temperature

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
            temp (float): temperature [degrees Celsius]
        """
        return self._get_temp_driver()

    def get_temp_motor(self):
        """Get drive motor

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
            temp (float): temperature [degrees Celsius]
        """
        return self._get_temp_motor()

    def get_bus_volt(self):
        """Get bus voltage

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
            volt (float): volt [V]
        """
        return self._get_bus_volt()

    def get_bus_curr(self):
        """Get bus current

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
            current (float): current [A]
        """
        return self._get_bus_curr()

    def get_multi_volt(self):
        """Get battery voltage of multi-turn encoder

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
            volt (float): volt [V]
        """
        return self._get_multi_volt()

    def get_error_code(self):
        """Get error code, the meaning of the fault code is referred to the appendix <fault code>

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
            code (int): error code
        """
        return self._get_error_code()

    ############################################################
    #                       Position Api
    ############################################################

    def get_pos_target(self):
        """Get target position

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
            pos (float): target position [rad]
        """
        return self._get_pos_target()

    def set_pos_target(self, pos):
        """Set target position

        Args:
            pos (float): target position [rad]

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
        """
        return self._set_pos_target(pos)

    def get_pos_current(self):
        """Get current position

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
            pos (float): current position [rad]
        """
        return self._get_pos_current()

    def get_pos_limit_min(self):
        """Get the minimum limit threshold of the position in position mode

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
            pos (float): position [rad]
        """
        return self._get_pos_limit_min()

    def set_pos_limit_min(self, pos):
        """Set the minimum limit threshold of the position in position mode,
        other modes such as speed mode and current mode do not work

        Args:
            pos (float): position [rad]

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
        """
        return self._set_pos_limit_min(pos)

    def get_pos_limit_max(self):
        """Get the maximum limit threshold of the position in position mode

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
            pos (float): position [rad]
        """
        return self._get_pos_limit_max()

    def set_pos_limit_max(self, pos):
        """Set the maximum limit threshold of the position in position mode,
        other modes such as speed mode and current mode do not work

        Args:
            pos (float): position [rad]

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
        """
        return self._set_pos_limit_max(pos)

    def get_pos_limit_diff(self):
        """Get the maximum position following error threshold in position mode

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
            pos (float): position [rad]
        """
        return self._get_pos_limit_diff()

    def set_pos_limit_diff(self, pos):
        """Set the maximum position following error threshold in position mode,
        the tracking error alarm threshold of the current position and the target position,
        other modes such as speed mode and current mode do not work

        Args:
            pos (float): position [rad]

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
        """
        return self._set_pos_limit_diff(pos)

    def get_pos_pidp(self):
        """Get position loop control parameter P

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
            p (float): parameter P
        """
        return self._get_pos_pidp()

    def set_pos_pidp(self, p):
        """Get position loop control parameter P

        Args:
            p (float): parameter P

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
        """
        return self._set_pos_pidp(p)

    def get_pos_smooth_cyc(self):
        """Get smoothing filter period of the position loop

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
            cyc (int): smoothing period [1-125]
        """
        return self._get_pos_smooth_cyc()

    def set_pos_smooth_cyc(self, cyc):
        """Set smoothing filter period of the position loop. The larger the smoothing period,
        the smoother the movement and the slower the response. The range is 1 to 125

        Args:
            cyc (int): smoothing period [1-125]

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
        """
        return self._set_pos_smooth_cyc(cyc)

    def get_pos_adrc_param(self, i):
        """Get speed loop ADRC parameters

        Args:
            i ([int]): Adrc has many parameters, which parameter needs to be get

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
            value (float): parameter Adrc
        """
        return self._get_pos_adrc_param(i)

    def set_pos_adrc_param(self, i, param):
        """Set position loop ADRC parameters

        Args:
            i ([int]): Adrc has many parameters, which parameter needs to be set
            param ([type]): [description]

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
        """
        return self._set_pos_adrc_param(i, param)

    def pos_cal_zero(self):
        """Set current position as mechanical zero, after the operation, the user needs to restart the device

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
        """
        return self._pos_cal_zero()

    ############################################################
    #                       Speed Api
    ############################################################

    def get_vel_target(self):
        """Get target speed

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
            vel (float): speed [rad/s]
        """
        return self._get_vel_target()

    def set_vel_target(self, vel):
        """Set target speed

        Args:
            vel (float): speed [rad/s]

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
        """
        return self._set_vel_target(vel)

    def get_vel_current(self):
        """Get current speed

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
            vel (float): speed [rad/s]
        """
        return self._get_vel_current()

    def get_vel_limit_min(self):
        """Get the minimum limit of the speed in speed mode and position mode

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
            vel (float): speed [rad/s]
        """
        return self._get_vel_limit_min()

    def set_vel_limit_min(self, vel):
        """Set the minimum limit of the speed in speed mode and position mode,
        other modes such as current mode do not work

        Args:
            vel (float): speed [rad/s]

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
        """
        return self._set_vel_limit_min(vel)

    def get_vel_limit_max(self):
        """Get maximum limit of the speed in speed mode and position mode

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
            vel (float): speed [rad/s]
        """
        return self._get_vel_limit_max()

    def set_vel_limit_max(self, vel):
        """Set maximum limit of the speed in speed mode and position mode,
        other modes such as current mode do not work

        Args:
            vel (float): speed [rad/s]

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
        """
        return self._set_vel_limit_max(vel)

    def get_vel_limit_diff(self):
        """Get the maximum speed following error threshold in the speed mode

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
            vel (float): speed [rad/s]
        """
        return self._get_vel_limit_diff()

    def set_vel_limit_diff(self, vel):
        """Set the maximum speed following error threshold in the speed mode,
        the tracking error alarm threshold of the current spped and the target speed,
        other modes such as position mode and current mode do not work

        Args:
            vel (float): speed [rad/s]

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
        """
        return self._set_vel_limit_diff(vel)

    def get_vel_pidp(self):
        """Get speed loop control parameter P

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
            p (float): parameter P
        """
        return self._get_vel_pidp()

    def set_vel_pidp(self, p):
        """Set speed loop control parameter P

        Args:
            p (float): parameter P

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
        """
        return self._set_vel_pidp(p)

    def get_vel_pidi(self):
        """Get speed loop control parameter I

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
            pid_i (float): parameter pid_i
        """
        return self._get_vel_pidi()

    def set_vel_pidi(self, pid_i):
        """Set speed loop control parameter I

        Args:
            pid_i (float): parameter pid_i

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
        """
        return self._set_vel_pidi(pid_i)

    def get_vel_smooth_cyc(self):
        """Get smoothing filter period of the speed loop

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
            cyc (int): smoothing period [1-125]
        """
        return self._get_vel_smooth_cyc()

    def set_vel_smooth_cyc(self, cyc):
        """Set smoothing filter period of the speed loop. The larger the smoothing period,
        the smoother the movement and the slower the response. The range is 1 to 125

        Args:
            cyc (int): smoothing period [1-125]

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
        """
        return self._set_vel_smooth_cyc(cyc)

    def get_vel_adrc_param(self, i):
        """Get speed loop ADRC parameters

        Args:
            i ([int]): Adrc has many parameters, which parameter needs to be get

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
            value (float): parameter Adrc
        """
        return self._get_vel_adrc_param(i)

    def set_vel_adrc_param(self, i, param):
        """Set speed loop ADRC parameters

        Args:
            i ([int]): Adrc has many parameters, which parameter needs to be set
            param ([type]): [description]

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
        """
        return self._set_vel_adrc_param(i, param)

    ############################################################
    #                       Current Api
    ############################################################

    def get_tau_target(self):
        """Get target current

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
            tau (float): target current [A]
        """
        return self._get_tau_target()

    def set_tau_target(self, tau):
        """Set target current

        Args:
            tau (float): target current [A]

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
        """
        return self._set_tau_target(tau)

    def get_tau_current(self):
        """Get current current

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
            tau (float): current current [A]
        """
        return self._get_tau_current()

    def get_tau_limit_min(self):
        """Get the minimum limit threshold of the current

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
            tau (float): current [A]
        """
        return self._get_tau_limit_min()

    def set_tau_limit_min(self, tau):
        """Set the minimum limit threshold of the current, all modes are effective

        Args:
            tau (float): current [A]

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
        """
        return self._set_tau_limit_min(tau)

    def get_tau_limit_max(self):
        """Get the maximum limit threshold of the current

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
            tau (float): current [A]
        """
        return self._get_tau_limit_max()

    def set_tau_limit_max(self, tau):
        """Set the maximum limit threshold of the current, all modes are effective

        Args:
            tau (float): current [A]

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
        """
        return self._set_tau_limit_max(tau)

    def get_tau_limit_diff(self):
        """Get the maximum current following error threshold in the current mode

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
            tau (float): current [A]
        """
        return self._get_tau_limit_diff()

    def set_tau_limit_diff(self, value):
        """Set the maximum current following error threshold in the current mode,
        the tracking error alarm threshold of the current current and the target current,
        other modes such as position mode and speed mode do not work

        Args:
            tau (float): current [A]

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
        """
        return self._set_tau_limit_diff(value)

    def get_tau_pidp(self):
        """Get current loop control parameter P

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
            pid_p (float): parameter P
        """
        return self._get_tau_pidp()

    def set_tau_pidp(self, pid_p):
        """Set current loop control parameter P

        Args:
            pid_p (float): parameter P

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
        """
        return self._set_tau_pidp(pid_p)

    def get_tau_pidi(self):
        """Get current loop control parameter I

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
            pid_i (float): parameter I
        """
        return self._get_tau_pidi()

    def set_tau_pidi(self, pid_i):
        """Set current loop control parameter I

        Args:
            pid_i (float): parameter I

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
        """
        return self._set_tau_pidi(pid_i)

    def get_tau_smooth_cyc(self):
        """Get smoothing filter period of the current loop

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
            cyc (int): smoothing period [1-125]
        """
        return self._get_tau_smooth_cyc()

    def set_tau_smooth_cyc(self, value):
        """Set smoothing filter period of the current loop. The larger the smoothing period,
        the smoother the movement and the slower the response. The range is 1 to 125

        Args:
            cyc (int): smoothing period [1-125]

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
        """
        return self._set_tau_smooth_cyc(value)

    def get_tau_adrc_param(self, i):
        """Get current loop ADRC parameters

        Args:
            i ([int]): Adrc has many parameters, which parameter needs to be get

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
            value (float): parameter Adrc
        """
        return self._get_tau_adrc_param(i)

    def set_tau_adrc_param(self, i, param):
        """Set current loop ADRC parameters

        Args:
            i ([int]): Adrc has many parameters, which parameter needs to be set
            param ([type]): [description]

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
        """
        return self._set_tau_adrc_param(i, param)
