#!/usr/bin/env python3
#
# Copyright (C) 2020 UmbraTek Inc. All Rights Reserved.
#
# Software License Agreement (BSD License)
#
# Author: Jimy Zhang <jimy.zhang@umbratek.com> <jimy92@163.com>
# =============================================================================
from base.arm_report_status import ArmReportStatus


class UtraReportStatus10Hz(ArmReportStatus):
    def __init__(self, ip):
        """This class will create a new thread to connect to ubot and receive the status of ubot at a frequency of 10HZ
        The status is as follows:
            axis (int): number of arm axes
            motion_status (int): running status of the arm
            motion_mode (int): operating mode of the arm
            mt_brake (int): enable state of the joint brake
            mt_able (int): enable state of the arm
            err_code (int): error code
            war_code (int): warning code
            cmd_num (int): current number of instruction cache
            joint (list): the actual angular positions of all joints
            pose (list):the current measured tool pose
            tau (list):the actual angular current of all joints

        Args:
            ip (String): IP address of UTRA robotic arm
        """
        ArmReportStatus.__init__(self, ip, 30001)


class UtraReportStatus100Hz(ArmReportStatus):
    def __init__(self, ip, irq_fun=0):
        """This class will create a new thread to connect to ubot and receive the status of ubot at a frequency of 100HZ
        The status is as follows:
            see the UtraReportStatus10HZ

        Args:
            ip (String): IP address of UTRA robotic arm
        """
        ArmReportStatus.__init__(self, ip, 30002, irq_fun)
