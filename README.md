# The Design and Control of a Motorized Prosthetic Arm

Author: Yael Ben Shalom<br>
Final project, MS in Robotics at Northwestern, 2021.


## Table of Contents

- [Project Description](#project_description)
- [Project Overview](#project_overview)
- [Getting Started](#getting-started)

## Project Description

In this project, I designed, built, and controlled a motorized prosthetic elbow that imitates healthy arm motion to help amputees prevent falling, avoid injuries, and maintain balance while walking. According to [Kent and Major's research](https://www.sciencedirect.com/science/article/abs/pii/S0268003320301248?casa_token=pASJip1O0HgAAAAA:ckojZ8F55NSTF2rAq7aVUub568BDZgnYYnto9notnVSgfjbTsNp5ktE2Q-ZMWgL62Lgc80yd), asymmetries in body mass and motion affect the regulation of whole-body angular momentum in individuals with upper limb absence and may increase fall risk.

To better predict the arm-body motion, I analyzed arm movement data patterns, simulated full arm dynamics, and found the relation between walking speed to the angular velocity of the arm.

Please visit [my website](https://yaelbenshalom.github.io/motorized_prosthetic_arm/index.html) for more information about this project.

## Project Overview

This project contains 4 parts:

1. [Data collection](https://github.com/YaelBenShalom/Motorized-Prosthetic-Arm/tree/master/data)
2. [Arm motion analysis and modeling](https://github.com/YaelBenShalom/Motorized-Prosthetic-Arm/tree/master/motor_control/arm_pendulum_modeling)
3. [Motor control to achieve the desired arm motion](https://github.com/YaelBenShalom/Motorized-Prosthetic-Arm/tree/master/motor_control)
4. [Mechanical design of the prosthetic elbow](https://github.com/YaelBenShalom/Motorized-Prosthetic-Arm/tree/master/mech_design)

## Getting Started

1. Clone the repository:
    ```
    git clone https://github.com/YaelBenShalom/Motorized-Prosthetic-Arm.git
    ```

2. Install the `odrive-tool` package. For installation instructions, visit the [ODrive getting-started page](https://docs.odriverobotics.com/).

3. Assemble the system acording to [this scheme]().

4. Connect the module to the computer's USB port and upload the desired ODrive configuration by running:
    ```
    python3 setup.py
    ```

    The controller might need an additional tunning. follow the tunning instructions on the [ODrive control page](https://docs.odriverobotics.com/control).

5. Activate the system by running:
    ```
    python3 motor_control/odrive_control.py --velocity=<walking velocity>
    ```
