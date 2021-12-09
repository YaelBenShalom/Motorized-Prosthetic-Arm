# The Design and Control of a Motorized Prosthetic Arm

Author: Yael Ben Shalom<br>
Final project, MS in Robotics at Northwestern, 2021.


## Motor Control to Achieve the Desired Arm Motion

To control the motor, I used a 2 layer control system - feedback current and position control. The current was controlled by the ODrive's controller, and the position was controlled by a feedback PID controller (with an optional feedforward component).

The control system diagram:

<p align="center">
  <img align="center" src="https://github.com/YaelBenShalom/Motorized-Prosthetic-Arm/blob/master/images/motor_control/control_diagram.png">
</p>

The PID position control diagram:

<p align="center">
  <img align="center" src="https://github.com/YaelBenShalom/Motorized-Prosthetic-Arm/blob/master/images/motor_control/pid_diagram.png">
</p>

An example of motor position control using the PID controller. The blue plot is the input angles, the red plot is the controlled output angles, and the second graph is the error changing with time:

<p align="center">
  <img align="center" src="https://github.com/YaelBenShalom/Motorized-Prosthetic-Arm/blob/master/videos/motor_control/lab_device.gif">
</p>

<p align="center">
  <img align="center" src="https://github.com/YaelBenShalom/Motorized-Prosthetic-Arm/blob/master/videos/motor_control/graph.png">
</p>
