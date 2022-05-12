#!/usr/bin/env python3
#
# Copyright (C) 2020 UmbraTek Inc. All Rights Reserved.
#
# Software License Agreement (BSD License)
#
# Author: Jimy Zhang <jimy.zhang@umbratek.com> <jimy92@163.com>
# =============================================================================
from base.arm_report_config import ArmReportConfig


class UtraReportConfig10Hz(ArmReportConfig):
    def __init__(self, ip):
        """This class will create a new thread to connect to ubot and receive the config of ubot at a frequency of 10HZ
        The status is as follows:
            trs_maxacc (float): maximum translational acceleration of the tool-space
            trs_jerk (float): translational jerk of the tool-space
            rot_maxacc (float): maximum rotate acceleration of the tool-space
            rot_jerk (float): rotate jerk of the tool-space
            p2p_maxacc (float): maximum acceleration of the joint-space
            p2p_jerk (float): jerk of the joint-space
            collis_sens (float): sensitivity of collision detection
            teach_sens (float): sensitivity of freedrive
            tcp_offset (list): coordinate offset of the end tcp tool
            tcp_load (list): payload mass and center of gravity
            gravity_dir (list): direction of the acceleration experienced by the robot

        Args:
            ip (string): IP address of UTRA robotic arm
        """

        ArmReportConfig.__init__(self, ip, 30003)
