# Copyright 2021 The UmbraTek Inc. All Rights Reserved.
#
# Software License Agreement (BSD License)
#
# Author: Jimy Zhang <jimy.zhang@umbratek.com> <jimy92@163.com>
# =============================================================================
from base.servo_api_base import _ServoApiBase
from common.utrc import UTRC_RW
from common import hex_data


class FLXIV_REG:
    null = 0
    SENSER1 = [0x60, 0, 16, null, null]


class FlxiVlApiBase(_ServoApiBase):
    def __init__(self, socket_fp, bus_client, tx_data):
        _ServoApiBase.__init__(self, socket_fp, bus_client, tx_data)

    def close(self):
        """Close socket
        """
        self._close()

    def connect_to_id(self, id, virtual_id=0):
        """Connect device ID

        Args:
            id (int): The ID number of the device
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


############################################################
#                       Control Api
############################################################

    def get_motion_mode(self):
        """Get the operating mode

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
            mode (int): operating mode of the arm
                0: none
                1: pump
        """
        return self._get_motion_mode()

    def set_motion_mode(self, mode):
        """Set the operating mode
        When the pump mode is set, the device will deactivate the pump enable and need to re-enable the pump

        Args:
            mode (int): operating mode of the arm
                0: none
                1: pump

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
        """
        return self._set_motion_mode(mode)

    def get_motion_enable(self):
        """Get pump enable status

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
            enable (bool): 0 Disable pump, 1 Enable pump
        """
        return self._get_motion_enable()

    def set_motion_enable(self, enable):
        """Set pump enable status

        Args:
            enable (bool): 0 Disable pump, 1 Enable pump

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
        """
        return self._set_motion_enable(enable)

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

    def get_error_code(self):
        """Get error code, the meaning of the fault code is referred to the appendix <fault code>

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
            code (int): error code
        """
        return self._get_error_code()

    def get_senser(self):
        """Get the values of sensors, including pressure sensors and six-axis IMU sensors

        Returns:
            ret (int): Function execution result code, refer to appendix for code meaning
            data (list): [pump pressure, ROLL, PITCH, YAW]
        """
        self._send(UTRC_RW.R, FLXIV_REG.SENSER1, None)
        ret, bus_rmsg = self._pend(UTRC_RW.R, FLXIV_REG.SENSER1)
        senser = hex_data.bytes_to_fp32_big(bus_rmsg.data[0:16], 4)
        return ret, senser
