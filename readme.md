
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
	[demo01_report](https://github.com/UmbraTek/ut_sdk_python/blob/master/example/utra/demo01_report.py)

	[demo02_get_param.py](https://github.com/UmbraTek/ut_sdk_python/blob/master/example/utra/demo02_get_param.py) 
	
	[demo03_motion_joint_space_p2p.py](https://github.com/UmbraTek/ut_sdk_python/blob/master/example/utra/demo03_motion_joint_space_p2p.py) 
	
	[demo04_motion_tool_space_line.py](https://github.com/UmbraTek/ut_sdk_python/blob/master/example/utra/demo04_motion_tool_space_line.py) 
	
	[demo05_motion_tool_space_lineb.py](https://github.com/UmbraTek/ut_sdk_python/blob/master/example/utra/demo05_motion_tool_space_lineb.py) 
	
	[demo06_motion_tool_space_arc.py](https://github.com/UmbraTek/ut_sdk_python/blob/master/example/utra/demo06_motion_tool_space_arc.py) 
	
	[demo08_motion_servo_joint.py](https://github.com/UmbraTek/ut_sdk_python/blob/master/example/utra/demo08_motion_servo_joint.py) 
	
	[demo21_flxie2_get_param.py](https://github.com/UmbraTek/ut_sdk_python/blob/master/example/utra/demo21_flxie2_get_param.py) 
	
	[demo22_flxie2_motion_now.py](https://github.com/UmbraTek/ut_sdk_python/blob/master/example/utra/demo22_flxie2_motion_now.py) 
	
	[demo23_flxie2_motion_que.py](https://github.com/UmbraTek/ut_sdk_python/blob/master/example/utra/demo23_flxie2_motion_que.py) 
	
	[demo24_flxiv_get_param.py](https://github.com/UmbraTek/ut_sdk_python/blob/master/example/utra/demo24_flxiv_get_param.py) 
	
	[demo25_flxiv_motion_now.py](https://github.com/UmbraTek/ut_sdk_python/blob/master/example/utra/demo25_flxiv_motion_now.py) 
	
	[demo31_rs485_pass_now.py](https://github.com/UmbraTek/ut_sdk_python/blob/master/example/utra/demo31_rs485_pass_now.py) 
	
	[demo32_rs485_pass_que.py](https://github.com/UmbraTek/ut_sdk_python/blob/master/example/utra/demo32_rs485_pass_que.py)
	
* OPTI

   [demo03_motion_joint_space_p2p.py](https://github.com/UmbraTek/ut_sdk_python/blob/master/example/opti/demo03_motion_joint_space_p2p.py) 

   [demo04_motion_tool_space_line.py](https://github.com/UmbraTek/ut_sdk_python/blob/master/example/opti/demo04_motion_tool_space_line.py) 

* ADRA

   [demo1_motion_position.py](https://github.com/UmbraTek/ut_sdk_python/blob/master/example/adra/demo1_motion_position.py) 

   [demo2_motion_velocity.py](https://github.com/UmbraTek/ut_sdk_python/blob/master/example/adra/demo2_motion_velocity.py) 

   [demo3_motion_torque.py](https://github.com/UmbraTek/ut_sdk_python/blob/master/example/adra/demo3_motion_torque.py) 

   [demo4_get_param.py](https://github.com/UmbraTek/ut_sdk_python/blob/master/example/adra/demo4_get_param.py) 

   [demo5_motion_cpos.py](https://github.com/UmbraTek/ut_sdk_python/blob/master/example/adra/demo5_motion_cpos.py) 

   [demo6_motion_ctau.py](https://github.com/UmbraTek/ut_sdk_python/blob/master/example/adra/demo6_motion_ctau.py) 

   [demo7_motion_cpostau.py](https://github.com/UmbraTek/ut_sdk_python/blob/master/example/adra/demo7_motion_cpostau.py) 

* FLXI E-Type

   [demo1_flxie2_motion_position.py](https://github.com/UmbraTek/ut_sdk_python/blob/master/example/flxie/demo1_flxie2_motion_position.py) 

   [demo2_flxie2_motion_current.py](https://github.com/UmbraTek/ut_sdk_python/blob/master/example/flxie/demo2_flxie2_motion_current.py) 

   [demo3_flxie2_get_param.py](https://github.com/UmbraTek/ut_sdk_python/blob/master/example/flxie/demo3_flxie2_get_param.py) 

* FLXI V-Type

   [demo1_flxivl_motion_pump.py](https://github.com/UmbraTek/ut_sdk_python/blob/master/example/flxiv/demo1_flxivl_motion_pump.py) 

   [demo2_flxivl_get_param.py](https://github.com/UmbraTek/ut_sdk_python/blob/master/example/flxiv/demo2_flxivl_get_param.py) 

* DataLink

   [demo1_datalink_rs485.py](https://github.com/UmbraTek/ut_sdk_python/blob/master/example/datalink/demo1_datalink_rs485.py) 

   [demo2_datalink_can.py](https://github.com/UmbraTek/ut_sdk_python/blob/master/example/datalink/demo2_datalink_can.py) 

##  manual 

 Please see the [wiki](https://umbratek.com/wiki/en/#!index.md)