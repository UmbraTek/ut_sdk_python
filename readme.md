
## Overview
Umbratek Python SDK, applicable products include: UTRA Arm Robot, OPTI Arm Robot, ADRA actuator, FIDO Quadruped Robot, FLXI E-Type Grippers, FLXI V-Type Grippers, DataLink Transceiver Module.

##  **Notes** 

*  Only support python3
*  The code test environment is ubuntu18.04, ubuntu20.04, ubuntu22.04.
*  Please follow the manual and pay attention to safety.

## Installation

 Installation is optional,  you can skip the installation if run examples. 

>  download

```
$ git clone https://github.com/UmbraTek/ut_sdk_python.git
```

>  install

```
$ python3 setup.py install
```

## Example

* UTRA
  
    [UTRA/OPTI SDK Programming Guide](https://github.com/UmbraTek/ut_sdk_python/tree/master/utapi/utra/readme.md)
    
    | Demo | Describe |
    | ---- | -------- |
    | [demo01_report](https://github.com/UmbraTek/ut_sdk_python/blob/master/example/utra/demo01_report.py) | This is a demo to print the data of three real-time automatically reported ports. |
    | [demo02_get_param.py](https://github.com/UmbraTek/ut_sdk_python/blob/master/example/utra/demo02_get_param.py) | This is a demo to get ubot parameters, status and other information run command. |
    | [demo03_motion_p2p.py](https://github.com/UmbraTek/ut_sdk_python/blob/master/example/utra/demo03_motion_p2p.py) | This is a demo of movement in joint space. |
    | [demo04_motion_linear.py](https://github.com/UmbraTek/ut_sdk_python/blob/master/example/utra/demo04_motion_linear.py) | This is a demo of movement in Tool space. |
    | [demo05_motion_linear_blending.py](https://github.com/UmbraTek/ut_sdk_python/blob/master/example/utra/demo05_motion_linear_blending.py) | This is a demo of movement in Tool space with an arc blending transition. |
    | [demo06_motion_circle.py](https://github.com/UmbraTek/ut_sdk_python/blob/master/example/utra/demo06_motion_circle.py) | This is a demo of circular motion in tool space. |
    | [demo08_motion_servo.py](https://github.com/UmbraTek/ut_sdk_python/blob/master/example/utra/demo08_motion_servo.py) | This is a demo of servo motion in joint space |
    | [demo21_flxie2_get_param.py](https://github.com/UmbraTek/ut_sdk_python/blob/master/example/utra/demo21_flxie2_get_param.py) | This is a demo to get the parameters, status and other information of FLXI E on the robot. |
    | [demo22_flxie2_motion_now.py](https://github.com/UmbraTek/ut_sdk_python/blob/master/example/utra/demo22_flxie2_motion_now.py) | This is a demo of controlling a FLXI E on robot. The command to control the FLXI E takes effect immediately whether the robot is moving or not. |
    | [demo23_flxie2_motion_que.py](https://github.com/UmbraTek/ut_sdk_python/blob/master/example/utra/demo23_flxie2_motion_que.py) | This is a demo of a robot controlling the FLXI E on robot.The command to control FLXI E will wait for the preceding robot motion command to be executed before taking effect. |
    | [demo24_flxiv_get_param.py](https://github.com/UmbraTek/ut_sdk_python/blob/master/example/utra/demo24_flxiv_get_param.py) | This is a demo to get the parameters, status and other information of FLXI V on the robot. |
    | [demo25_flxiv_motion_now.py](https://github.com/UmbraTek/ut_sdk_python/blob/master/example/utra/demo25_flxiv_motion_now.py) | This is a demo of controlling a FLXI V on robot. The command to control the FLXI V takes effect immediately whether the robot is moving or not. |
    | [demo31_rs485_pass_now.py](https://github.com/UmbraTek/ut_sdk_python/blob/master/example/utra/demo31_rs485_pass_now.py) | This is a demo of pass-through data to rs485 at the end of the manipulator.The command to pass-through data takes effect immediately whether the robot is moving or not. |
    | [demo32_rs485_pass_que.py](https://github.com/UmbraTek/ut_sdk_python/blob/master/example/utra/demo32_rs485_pass_que.py) | This is a demo of pass-through data to rs485 at the end of the manipulator.The command to pass-through data will wait for the preceding robot motion command to be executed before taking effect. |


* OPTI

   [UTRA/OPTI SDK Programming Guide](https://github.com/UmbraTek/ut_sdk_python/tree/master/utapi/utra/readme.md)

   The opti manipulator can refer to the utra demo and api. All the demos and instructions of the opti series and utra series are universal. It only needs to be noted that the target position of the movement needs to be modified according to different models, because the movement range of each model of the manipulator is not the same.

   | Demo                                                         | Describe                                   |
   | ------------------------------------------------------------ | ------------------------------------------ |
   | [demo03_motion_p2p.py](https://github.com/UmbraTek/ut_sdk_python/blob/master/example/utra/demo03_motion_p2p.py) | This is a demo of movement in joint space. |
   | [demo04_motion_linear.py](https://github.com/UmbraTek/ut_sdk_python/blob/master/example/utra/demo04_motion_linear.py) | This is a demo of movement in Tool space.  |

* ADRA

    | Demo  | Describe |
    | ------| ---------|
    | [demo1_motion_position.py](https://github.com/UmbraTek/ut_sdk_python/blob/master/example/adra/demo1_motion_position.py) | This demo is to control the device to move to the specified position. |
    | [demo2_motion_velocity.py](https://github.com/UmbraTek/ut_sdk_python/blob/master/example/adra/demo2_motion_velocity.py) | This demo controls the actuator running at a constant speed in speed mode. |
    | [demo3_motion_torque.py](https://github.com/UmbraTek/ut_sdk_python/blob/master/example/adra/demo3_motion_torque.py) | This demo controls the actuator running at a constant torque in torque mode. |
    | [demo4_get_param.py](https://github.com/UmbraTek/ut_sdk_python/blob/master/example/adra/demo4_get_param.py) | This is demo to get the state and parameters of the actuator. |
    | [demo5_motion_cpos.py](https://github.com/UmbraTek/ut_sdk_python/blob/master/example/adra/demo5_motion_cpos.py) | This is a demo of setting the target positions of 3 actuators simultaneously in broadcast mode (one packet). |
    | [demo6_motion_ctau.py](https://github.com/UmbraTek/ut_sdk_python/blob/master/example/adra/demo6_motion_ctau.py) | This is a demo of setting the target torque of 3 actuators simultaneously in broadcast mode (one packet). |
    | [demo7_motion_cpostau.py](https://github.com/UmbraTek/ut_sdk_python/blob/master/example/adra/demo7_motion_cpostau.py) | This is a demo of setting the maximum interval of broadcast read commands and setting the target positions and feedforward torques of 3 actuators simultaneously in broadcast mode (one packet). |
    | [demo8_motion_cposvel.py](https://github.com/UmbraTek/ut_sdk_python/blob/master/example/adra/demo8_motion_cposvel.py) | This is a demo of setting the maximum interval of broadcast read commands and setting the target positions and target speed of 3 actuators simultaneously in broadcast mode (one packet). |
  
* FLXI E-Type

    | Demo | Describe  |
    | -----| ----------|
    | [demo1_flxie2_motion_position.py](https://github.com/UmbraTek/ut_sdk_python/blob/master/example/flxie/demo1_flxie2_motion_position.py) | This demo is to control the gripper to move to the specified position. |
    | [demo2_flxie2_motion_torque.py](https://github.com/UmbraTek/ut_sdk_python/blob/master/example/flxie/demo2_flxie2_motion_torque.py) | This demo is to control the device to move to the specified torque. |
    | [demo3_flxie2_get_param.py](https://github.com/UmbraTek/ut_sdk_python/blob/master/example/flxie/demo3_flxie2_get_param.py) | This is demo to get the state and parameters of the gripper. |

* FLXI V-Type

    | Demo                                                         | Describe                                   |
   | ------------------------------------------------------------ | ------------------------------------------ |
   | [demo1_flxivl_motion_pump.py](https://github.com/UmbraTek/ut_sdk_python/blob/master/example/flxiv/demo1_flxivl_motion_pump.py) | This demo is to control the gripper enable/disable.          |
   | [demo2_flxivl_get_param.py](https://github.com/UmbraTek/ut_sdk_python/blob/master/example/flxiv/demo2_flxivl_get_param.py) | This is demo to get the state and parameters of the gripper. |

* DataLink

    | Demo | Describe |
    | -----| ---------|
    | [demo1_datalink_rs485.py](https://github.com/UmbraTek/ut_sdk_python/blob/master/example/datalink/demo1_datalink_rs485.py) | This example tests the EtherNet to RS485 module, sends the received RS485 data back. |
    | [demo2_datalink_can.py](https://github.com/UmbraTek/ut_sdk_python/blob/master/example/datalink/demo2_datalink_can.py) | This example tests the EtherNet to CAN module, sends the received CAN data back. |

##  manual 

 Please see the [wiki](https://umbratek.com/wiki/en/#!index.md)
