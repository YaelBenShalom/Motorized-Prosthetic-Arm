# Designing, building and controlling a motorized prosthetic arm

Author: Yael Ben Shalom
Final project, MS in Robotics at Northwestern, 2021.


## Table of Contents

- [Project Description](#project_description)
- [Project Overview](#project_overview)
- [Getting Started](#getting-started)

## Project Description

In this project, I designed, built, and controlled a motorized prosthetic elbow that imitates healthy arm motion to help amputees prevent falling, avoid injuries, and maintain balance while walking. According to Kent and Major's research[1], asymmetries in body mass and motion affect the regulation of whole-body angular momentum in individuals with upper limb absence and may increase fall risk.

To better predict the arm-body motion, I analyzed arm movement data patterns, simulated full arm dynamics, and found the relation between walking speed to the angular velocity of the arm.<br><br>
Please visit [my website](https://yaelbenshalom.github.io/motorized_prosthetic_arm/index.html) for more information about this project.<br>

## Project Overview

This project contained 4 parts:

1. [Data collection](https://github.com/YaelBenShalom/Motorized-Prosthetic-Arm/tree/master/data)
2. [Arm motion analysis and modeling](https://github.com/YaelBenShalom/Motorized-Prosthetic-Arm/tree/master/motor_control/arm_pendulum_modeling)
3. [Motor control to achieve the desired arm motion](https://github.com/YaelBenShalom/Motorized-Prosthetic-Arm/tree/master/motor_control)
4. [Mechanical design of the prosthetic elbow](https://github.com/YaelBenShalom/Motorized-Prosthetic-Arm/tree/master/mech_design)


## Getting Started

1. Clone the repository:
    ```
    git clone git@github.com:YaelBenShalom/Motorized-Prosthetic-Arm.git
    ```

2. Install the `odrive-tool` package. For installation instructions, visit the [odrive getting-started page
](https://docs.odriverobotics.com/).

3. Assemble the system acording to [this scheme]().

4. To activate the system, connect the odrive to the computer and run:
    ```
    python3 motor_control/odrive_control.py --velocity=<walking velocity>
    ```