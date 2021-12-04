# Designing, Building and Controlling a Motorized Prosthetic Arm

Author: Yael Ben Shalom<br>
Final project, MS in Robotics at Northwestern, 2021.


## Arm Motion Analysis and Modeling

To Better understand the motion of a human arm and find a suitable motor to imitate the elbow motion, I modeled the arm as a double pendulum system. I used the system Lagrangian and measured shoulder and elbow angles to find the motion equations and extract the required elbow torque. More explanations about the theoretical aspects of the method and calculations can be found [here](https://yaelbenshalom.github.io/motorized_prosthetic_arm/index.html).

The double pendulum can be described using the following system sketch, where the masses are located in the center of mass of every link:

<p align="center">
  <img align="center" src="https://github.com/YaelBenShalom/Motorized-Prosthetic-Arm/blob/master/images/double_pendulum/double-pendulum-diagram.png" width="50%">
</p>

The following video shows an animation of the arm motion, represented as a double pendulum:

<p align="center">
  <img align="center" src="https://github.com/YaelBenShalom/Motorized-Prosthetic-Arm/blob/master/videos/double_pendulum/arm_pendulum_animation.gif" width="130%">
</p>
