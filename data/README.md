# The Design and Control of a Motorized Prosthetic Arm

Author: Yael Ben Shalom<br>
Final project, MS in Robotics at Northwestern, 2021.


## Data Collection

In this part of the project, I focused on measuring prosthetics characteristics and collecting body-arm motion data.<br>
For further information about data collection please visit [my website](https://yaelbenshalom.github.io/motorized_prosthetic_arm/index.html).

This section contains all the data collected in this project and the scripts used to process it. It contains 2 main parts:
1. Prosthetic Measurements (length, mass, and center of mass location) to define the average prosthetic the device should support.
2. Walking data was collected from people with and without upper limb absence (including myself). The data was collected using sensors attached to the body in various locations (forearm, upper arm, lower back, etc.), that measured the body's angles, velocities, and accelerations. these were later used to explore the body-arm dynamics while walking, and to find the correlation between walking speed and arm swing

An example of the outputs of the sensors are presented in the following video:

<p align="center">
  <img align="center" src="https://github.com/YaelBenShalom/Motorized-Prosthetic-Arm/blob/master/videos/treadmill_test/accelerometer.gif">
</p>
