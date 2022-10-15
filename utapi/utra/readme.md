# UTRA/OPTI SDK Programming Guide

[TOC]

## 1 Motion Mode

There are two modes of motion.

### 1.1 Mode 0: Position control mode

In this mode, the robotic arm can execute a series of motion Commands automatically planned by the control box, which is also the mode that the control box enters by default after startup.

### 1.2 Mode 2: Joint teaching mode

In this mode, the robotic arm will enter the zero gravity mode, and the user can freely drag the links of the robotic arm to complete the teaching function. If the drag teaching is completed, switch back to mode 0.

* Steps to enter teach mode

  ```
  1. Set the correct load, TCP offset, installation direction and teaching sensitivity of the robot.    // API:set_tcp_load(mass, dir); set_tcp_offset(offset)
                   // set_gravity_dir(dir); set_teach_sens(num)
  2. Enable the robot.                        // API: set_motion_enable(8, 1)
  3. Set the state of the robot to 0(ready).  // API: set_motion_status(0)
  4. Set the teach mode of the robot.         // API: set_motion_mode(5)
  ```

* Note

1. Set_teach_sens, sensitivity increases from 90 % to 110 %, and 110 is the highest sensitivity. Sensitivity is not the higher the better, the most important, under normal circumstances 100 is very appropriate, is also the default value.

## 2 Motion State

### 2.1 set_motion_status()

There are three states that can be set.

| Status | Describe                                                     |
| ------ | ------------------------------------------------------------ |
| 0      | Ready motion<br>Can be understood as ready for motion or stand-by. In this state, the robotic arm can normally respond to and execute motion commands. If the robotic arm recovers from an error, power outage, or stop state (state 4), remember to set the state to 0 before continuing to send motion commands. Otherwise the commands sent will be discarded. |
| 3      | Paused state<br>Pause the currently executing motion.After a pause, you can resume movement by setting the state to 0. |
| 4      | Stop state<br>Terminates the current motion and clears the cached subsequent commands. |

### 2.2 get_motion_status(state)

There are four states that can be get.

| Status | Describe                                                     |
| ------ | ------------------------------------------------------------ |
| 1      | In motion<br>The robotic arm is executing motion commands and is not stationary. |
| 2      | Standby<br>The control box is already in motion ready state, but no motion commands are cached for execution. |
| 3      | Pausing<br>The robotic arm is set to pause state.            |
| 4      | Stopping<br>The robot arm is in the stopped state, in this state, the robot arm does not execute motion commands. This state is the state entered by default upon power-on. You can set the state to 0 to get the arm back into the ready motion state. |

## 3 Motion Instruction

1. Motions of the robotic arm: P2P motion, linear motion, linear-blending motion, circular motion, servo motion.The movement method is explained in the Studio - Blocky - Toolbar - Motion chapter, please check this chapter, here is the description of the application.

2. NTRO has a cache queue of 1024 instructions, and multiple motion instructions will be cached in the queue when they are sent. When the cache is full, continuing to send instructions will be discarded. You can obtain the current NTRO instruction cache number through instruction get_cmd_num() or automatic reporting UtraReportStatus10Hz().

* Steps for using motion instruction

  ```
  1. set_motion_mode(0)         // Set the robot to position control mode
  2. set_motion_enable(8, 1)    // Enable all joints of the robot
  3. set_motion_status(0)       // Set the state of the robot to ready
  4. Moveto_xxx_xxx()           // Motion instruction
  ```

### 3.1 P2P Motion

* features
  1. Use the planning method that minimizes the total joint motion angle, to achieve the point-to-point motion of joint space (unit: degree/radian).
  2. The trajectory of TCP is an irregular arc in Cartesian space.
  3. The speed between each command is discontinuous.
  4. Velocity planning is an S-curve.
  5. The movement efficiency and stability are the highest.

* SDK-API

    | API                                                      | parameter                                                    |
    | -------------------------------------------------------- | ------------------------------------------------------------ |
    | moveto_cartesian_p2p<br>( mvpose, mvvelo, mvacc, mvtime) | mvpose: Moving target, Cartesian coordinates<br>mvvelo/mvacc: Speed and acceleration of motion<br>mvtime: Reserve |
    | moveto_joint_p2p<br>(mvjoint, mvvelo, mvacc, mvtime)     | mvjoint: Moving target, joint coordinates<br>mvvelo/mvacc: Speed and acceleration of motion<br>mvtime: Reserve |
    | moveto_home_p2p<br>(mvvelo, mvacc, mvtime)               | mvvelo/mvacc: Speed and acceleration of motion<br>mvtime: Reserve |

* Example

  There is a demo on github: 

  ```
  1. ut_sdk_python/example/utra/demo03_motion_p2p.py
  2. ut_sdk_python/example/opti/demo03_motion_p2p.py
  3. ut_sdk_cpp/example/utra/demo03_motion_p2p.cpp
  4. ut_sdk_cpp/example/opti/demo03_motion_p2p.cpp
  ```

* Steps to use these instructions

  ```
  1. set_motion_mode(0)         // Set the robot to position control mode
  2. set_motion_enable(8, 1)    // Enable all joints of the robot
  3. set_motion_status(0)       // Set the state of the robot to ready
  4. moveto_joint_p2p()         // Motion instruction
  ```

* Application Scenario
  1. No straight line required for TCP.
  2. Speed does not need to be continuous between multiple motion commands.

### 3.2 Linear Motion

* features
  1. To achieve linear motion of TCP between Cartesian coordinates.
  2. The trajectory of TCP is an linear in Cartesian space.
  3. The speed between each command is discontinuous.
  4. Velocity planning is an S-curve.

* SDK-API

    | API                                                      | parameter                                                    |
    | -------------------------------------------------------- | ------------------------------------------------------------ |
    | moveto_cartesian_line<br>(mvpose, mvvelo, mvacc, mvtime) | mvpose: Moving target, Cartesian coordinates<br>mvvelo/mvacc: Speed and acceleration of motion<br>mvtime: Reserve |
    | moveto_joint_line<br>(mvjoint, mvvelo, mvacc, mvtime)    | mvjoint: Moving target, joint coordinates<br>mvvelo/mvacc: Speed and acceleration of motion<br>mvtime: Reserve |

* Example

    There is a demo on github: 

    ```
    1. ut_sdk_python/example/utra/demo04_motion_linear_blend.py
    2. ut_sdk_python/example/opti/demo04_motion_linear_blend.py
    3. ut_sdk_cpp/example/utra/demo04_motion_linear_blend.cpp
    4. ut_sdk_cpp/example/opti/demo04_motion_linear_blend.cpp
    ```

* Steps to use these instructions

    ```
    1. set_motion_mode(0)         // Set the robot to position control mode
    2. set_motion_enable(8, 1)    // Enable all joints of the robot
    3. set_motion_status(0)       // Set the state of the robot to ready
    4. moveto_cartesian_line()    // Motion instruction
    ```

* Application Scenario

    1. Straight line required for TCP.
    2. Speed does not need to be continuous between multiple motion commands.

### 3.3 Linear-Blending Motion

* features
  1. To achieve linear motion of TCP between Cartesian coordinates, inserting an arc between two straight lines for a smooth transition.
  2. The trajectory of TCP is an linear in Cartesian space(the corner is an arc).
  3. The speed between each command is continuous.
  4. Velocity planning is an S-curve.

* SDK-API

    | API                                                          | parameter                                                    |
    | ------------------------------------------------------------ | ------------------------------------------------------------ |
    | moveto_cartesian_lineb<br>(mvpose, mvvelo, mvacc, mvtime, mvradii) | mvpose: Moving target, Cartesian coordinates<br>mvvelo/mvacc: Speed and acceleration of motion<br>mvtime: Reserve<br>mvradii: Blend radius |
    | moveto_joint_lineb<br>(mvjoint, mvvelo, mvacc, mvtime, mvradii) | mvjoint: Moving target, joint coordinates<br>mvvelo/mvacc: Speed and acceleration of motion<br>mvtime: Reserve<br>mvradii: Blend radius |

* Example

  There is a demo on github: 

  ```
  1. ut_sdk_python/example/utra/demo05_motion_linear_blending.py
  2. ut_sdk_cpp/example/utra/demo05_motion_linear_blending.cpp
  ```

* Steps to use these instructions

  ```
  1. set_motion_mode(0)         // Set the robot to position control mode
  2. set_motion_enable(8, 1)    // Enable all joints of the robot
  3. set_motion_status(0)       // Set the state of the robot to ready
  4. plan_sleep(1)              // Set the planning delay. Because more than two motion commands are required when planning the blending path of straight lines and arcs, it is necessary to set a planning delay to ensure that the second/third... motion commands have been received when planning the first motion command. This is to compensate for the delay of the application sending data to the NTRO controller. This delay time can be adjusted, generally between 0.1-3 seconds.
  5. moveto_cartesian_lineb()   // Motion instruction1
  6. moveto_cartesian_lineb()   // Motion instruction2
  7. moveto_cartesian_lineb()   // Motion instruction3......
  ```

* Application Scenario

  1. Straight line required for TCP.
  2. Speed need to be continuous between multiple motion commands.

### 3.4 Circular Motion

* features
  1. Circular motion of TCP calculates the trajectory of the spatial circle according to the three-point coordinates, the threepoint coordinates are starting point, parameter 1 and parameter 2.Trajectories can be consecutive complete N circles, or 1/ N circles.
  2. The trajectory of TCP is an arc in Cartesian space.
  3. The speed between each command is discontinuous.
  4. Velocity planning is an S-curve.

* SDK-API

    | API                                                          | parameter                                                    |
    | ------------------------------------------------------------ | ------------------------------------------------------------ |
    | moveto_cartesian_circle<br>(pose1, pose2, mvvelo, mvacc, mvtime, percent) | mvpose: Moving target, Cartesian coordinates<br>mvvelo/mvacc: Speed and acceleration of motion<br>mvtime: Reserve<br>percent: Percentage number of arc paths |
    | moveto_joint_circle<br>(mvjoint1, mvjoint2, mvvelo, mvacc, mvtime, percent) | mvjoint: Moving target, joint coordinates<br>mvvelo/mvacc: Speed and acceleration of motion<br>mvtime: Reserve<br>percent: Percentage number of arc paths |

* Example

  There is a demo on github: 

  ```
  1. ut_sdk_python/example/utra/demo06_motion_circle.py
  2. ut_sdk_cpp/example/utra/demo06_motion_circle.cpp
  ```

* Steps to use these instructions

  ```
  1. set_motion_mode(0)         // Set the robot to position control mode
  2. set_motion_enable(8, 1)    // Enable all joints of the robot
  3. set_motion_status(0)       // Set the state of the robot to ready
  4. moveto_cartesian_circle()  // Motion instruction
  ```

* Application Scenario

  1. TCP requires an arc or a circle.
  2. Speed does not need to be continuous between multiple motion commands.

### 3.5 Servo motion

* features
  1. Move to the target joint position at the specified time (The acceleration is infinite). 
  2. The controller frequency of the NTRO is 400Hz(If you need a higher frequency,you can send an email to umbratek to get 1KHz firmware). 
  3. The trajectory of TCP is an irregular arc in Cartesian space.
  4. No speed planning(The time parameter is only used to simply average the position of the split trajectory).
  5. It is equivalent to sending the target position directly to the server actuator.

* SDK-API

    | API                                                 | parameter                                                    |
    | --------------------------------------------------- | ------------------------------------------------------------ |
    | moveto_servo_joint<br>(frames_num, mvjoint, mvtime) | rames_num: Number of target coordinates, up to three<br>mvjoint: Joint positions[rad], That's equal to the number of joints times the number of frames<br>mvtime: Time to move to target [seconds] |

* Example

  There is a demo on github: 

  ```
  \1. ut_sdk_python/example/utra/demo08_motion_servo.py
  
  \2. ut_sdk_cpp/example/utra/demo08_motion_servo.cpp
  ```

* Steps to use these instructions

  For example, moving from the current position A to the target position B, the target velocity V, using T or S curve for velocity planning, the total running time is T. The optimal way for the robot arm to execute this trajectory is:

  ```
  1. The trajectory is discretized into N target points according to the calculation method of equal time (it is recommended that the discrete time interval is t=1/400=0.0025s according to the frequency of 400Hz).
  2. set_motion_mode(0)        // Set the robot to position control mode
  3. set_motion_enable(8, 1)   // Enable all joints of the robot
  4. set_motion_status(0)      // Set the state of the robot to ready
  
  5. plan_sleep(1)             // In order to make the control speed of the robot smoother and more continuous, it is necessary to set a planning delay to ensure that the second/third/more motion commands have been received when planning the first motion command. This is to compensate for the delay of the application sending data to the NTRO controller. This delay time can be adjusted, generally between 0.1-3 seconds.
  
  6. moveto_servo_joint()      // Send all the N target points to the NTRO controller, and set the running time of each execution instruction to 0. Then the robot will execute according to the planned speed of the trajectory.
  
  7. If the running time of each execution instruction is set to 0.005s, because the control cycle of the controller is 400Hz(0.025s), then each instruction controller needs to use two control cycles to execute, which is equivalent to reducing the speed/acceleration of the trajectory by 50%.
  ```

* Application Scenario

  1. An object needs to be tracked in real time. 
  2. The application software needs to plan its trajectory based on the actual scenario.

### 3.6 Queue of instructions 

When multiple motion commands are sent to the controller in a short period of time, the controller will queue these commands and execute them one by one. (Non-motion instructions are executed immediately and not queued).The maximum value of the queue store is 1024, and the API:get_cmd_num() can be used to check how many instructions are currently stored in the queue.

### 3.7  Sleep

There are two sleep commands: plan_sleep()¡¢move_sleep().Both are delays. 

* differences 

  1. move_sleep() is common instructions.
  2. plan_sleep() is motion instruction.

  First, the controller will have two threads that parse the user's instructions. 

  As mentioned above, the instructions sent by the user are first put into the queue and executed in turn. This execution is thread 1. When the motion instruction is executed, it will put the motion instruction into the second queue for cache and be executed by thread 2.
  Here, when thread 1 reaches the move_sleep() instruction, it delays execution for the user-specified amount of time and then continues execution of the next instruction. However, when executing plan_sleep(), there is no delay, because plan_sleep() is a motion instruction, thread 1 adds this instruction to the second queue, and when thread 2 reaches plan_sleep(), there is a user-specified delay.

* motion instruction

  The motion instruction are as follows: (the others are common instruction)

  ```
    int moveto_cartesian_line();
    int moveto_cartesian_lineb();
    int moveto_cartesian_p2p();
    int moveto_cartesian_p2pb();
    int moveto_cartesian_circle();
    int moveto_joint_line();
    int moveto_joint_lineb();
    int moveto_joint_p2p();
    int moveto_joint_circle();
    int moveto_home_p2p();
    int moveto_servo_joint();
    int moveto_joint_servo();
    int moveto_cartesian_servo();
    int plan_sleep();
  ```

* Application Scenario

  plan_sleep() mainly serves the moveto_cartesian_lineb()/moveto_cartesian_p2pb()/moveto_joint_lineb()/moveto_servo_joint()/moveto_joint_servo()/moveto_cartesian_servo() directive. Because these instructions need to be executed along with the instructions that follow them, using plan_sleep() eliminates communication, system, and other delays, so that the instructions will be queued when they are executed.

## 4 Real-Time Data Reporting

There are three automatic reporting methods:

1. The frequency of 10Hz reports the current state of the robot, including motion mode, motion state, enable state, brake state, error code, number of motion instruction buffers, current joint position, current TCP Cartesian position, current joint torque. A maximum of five clients can be connected at the same time; otherwise, the connection fails.
2. The frequency of 100Hz reports the current state of the robot, including motion mode, motion state, enable state, brake state, error code, number of motion instruction buffers, current joint position, current TCP Cartesian position, current joint torque. A maximum of one clients can be connected at the same time; otherwise, the connection fails.
3. The frequency of 10Hz reports robot configuration parameters, including linear motion speed and acceleration and acceleration, p2p motion speed and acceleration and acceleration, tcp offset load, installation direction, collision sensitivity, teaching sensitivity. A maximum of five clients can be connected at the same time; otherwise, the connection fails.

* SDK-API

    | API                       | parameter                              |
    | ------------------------- | -------------------------------------- |
    | UtraReportStatus10Hz(ip)  | ip (String): IP address of robotic arm |
    | UtraReportStatus100Hz(ip) | ip (String): IP address of robotic arm |
    | UtraReportConfig10Hz(ip)  | ip (String): IP address of robotic arm |

* Example

  There is a demo on github: 

  ```
  1. ut_sdk_python/example/utra/demo01_report.py
  2. ut_sdk_cpp/example/utra/demo01_report.cpp
  ```

* Steps to use these api

  ```
  1. ubot = UtraReportStatus10Hz()  // Instantiated class
  2. ubot.is_update()          // Determine whether the reported data has been updated.
  3. print(ubot.joint)         // Gets the reported joint position
  4. print(ubot.motion_status) // Gets the reported motion status
  5. Gets the other data reported
  ```

##  5 Set the parameters 

The controller takes effect immediately after setting the parameters, but the parameters are not saved when the controller is restarted. If you want the parameters to persist after a restart, you need to call the API:saved_parm().

### 5.1 Set collision sensitivity 

Call the API:set_collis_sens() to set collision sensitivity. Refer to the [Collision Sensitivity] section of the user manual for details.