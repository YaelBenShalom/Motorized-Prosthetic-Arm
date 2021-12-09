from __future__ import print_function

import argparse
import os
import time
import math
import pandas as pd

import matplotlib.pyplot as plt

from pid import PID

import odrive
from odrive.utils import start_liveplotter
from odrive.enums import *


STRAIGHT_POSITION = 0.55


def load_dataset(data_file_name, data_dir):
    """
    This function loads the synthesized data provided in a csv file in the
    /data_dir directory.
    """

    data_path = os.path.join(data_dir, data_file_name)
    data_rows = open(data_path).read().strip().split("\n")

    return data_rows


def liveplot(driver_name):
    start_liveplotter(lambda: [
        driver_name.axis0.encoder.pos_estimate,
        driver_name.axis0.encoder.vel_estimate,
        driver_name.axis0.motor.current_control.Iq_measured
    ])


def clear_errors(driver_name):
    if driver_name.axis0.error:
        print("axis 0", driver_name.axis0.error)
        driver_name.axis0.error = 0

    if driver_name.axis0.motor.error:
        print("motor 0", driver_name.axis0.motor.error)
        driver_name.axis0.motor.error = 0

    if driver_name.axis0.encoder.error:
        print("encoder 0", driver_name.axis0.encoder.error)
        driver_name.axis0.encoder.error = 0


def Calibration(driver_name):
    # Calibrate motor and wait for it to finish
    print("Starting calibration...")
    driver_name.axis0.requested_state = AXIS_STATE_FULL_CALIBRATION_SEQUENCE
    while driver_name.axis0.current_state != AXIS_STATE_IDLE:
        time.sleep(0.1)


def shut_down(driver_name):
    # Stopping the motor spin
    driver_name.axis0.controller.config.control_mode = CONTROL_MODE_VELOCITY_CONTROL
    driver_name.axis0.controller.input_vel = 0

    # Moving to straight position
    driver_name.axis0.controller.config.control_mode = CONTROL_MODE_POSITION_CONTROL
    driver_name.axis0.controller.input_pos = STRAIGHT_POSITION
    print("Going back to home position")


def get_motor_state(driver_name):
    motor_pos = driver_name.axis0.encoder.pos_estimate
    motor_vel = driver_name.axis0.encoder.vel_estimate
    motor_current = driver_name.axis0.motor.current_control.Iq_setpoint

    return motor_pos, motor_vel, motor_current


def position_control(driver_name, elbow_pos, elbow_torque):
    driver_name.axis0.controller.config.control_mode = CONTROL_MODE_POSITION_CONTROL

    motor_kv = 115
    torque_const = 8.27 / motor_kv
    position_offset = 0.18

    plot_rate = 1 / 110
    
    plot_graphs = False
    
    if plot_graphs:
        input_pos_plot = []
        output_torque_plot = []
        output_pos_plot = []
        output_vel_plot = []
        pos_error = []
        pos_error_abs = []
        t_plot = []
        
        plt.figure(figsize=(100, 50))
        plt.suptitle('Odrive Output', fontsize=75)
        plt.subplot(311)

    init_time = time.time()

    for i in range(len(elbow_pos)):
        try:
            current_time = time.time()
            t = current_time - init_time
            input_pos = elbow_pos[i] - position_offset

            driver_name.axis0.controller.input_pos = input_pos
            clear_errors(driver_name)

            output_pos, output_vel, output_curr = get_motor_state(driver_name)

            print("Position: {} [turn]\t Velocity: {} [turn/s]\t Current: {} [A]\t Position Error: {} [deg]".format(
                output_pos, output_vel, output_curr, (input_pos - output_pos)*360))
                
            if plot_graphs:
                input_pos_plot.append(input_pos*360)
                output_pos_plot.append(output_pos*360)
                output_vel_plot.append(output_vel*360)
                output_torque_plot.append(-output_curr * torque_const)
                pos_error.append((input_pos - output_pos)*360)
                pos_error_abs.append(abs(input_pos - output_pos)*360)
                t_plot.append(t)

                plt.scatter(t, input_pos*360, c="blue")
                plt.scatter(t, output_pos*360, c="red")
                
            time.sleep(plot_rate/2.5)

        except:
            print("Couldn't complete motion. shutting down")
            shut_down(driver_name)
            raise

    if plot_graphs:
        max_pos_error = max(pos_error_abs)
        print("Maximum position error is: ", max_pos_error)
        print("Average position error is: ", sum(pos_error)/len(pos_error))
        print("Maximum position error as a precent of the max position: {}%".format(
            max_pos_error*100/(max(elbow_torque)*360)))
        print("Delta time: {}".format(time.time() - init_time))

        plt.plot(t_plot, input_pos_plot, c="blue", label="Input position")
        plt.plot(t_plot, output_pos_plot, c="red", label="Output position")
        plt.ylabel('Angle [deg]', fontsize=40)
        plt.xlabel('Time [sec]', fontsize=40)
        plt.grid()
        plt.title('Input & Output Position', fontsize=50)
        plt.legend(fontsize=40)

        plt.subplot(312)
        plt.plot(t_plot, pos_error, label="Position error")
        plt.ylabel('Error [deg]', fontsize=40)
        plt.xlabel('Time [sec]', fontsize=40)
        plt.grid()
        plt.title('Position Error', fontsize=50)
        plt.legend(fontsize=40)

        plt.subplot(313)
        plt.plot(t_plot, elbow_torque, c="blue", label="Theoretical torque")
        plt.plot(t_plot, output_torque_plot, c="red", label="Output torque")
        plt.ylabel('Torque [Nm]', fontsize=40)
        plt.xlabel('Time [sec]', fontsize=40)
        plt.grid()
        plt.title('Theoretical Vs. Output Torque', fontsize=50)
        plt.legend(fontsize=40)

        plt.savefig("output.png")


def velocity_control(driver_name, elbow_vel, elbow_torque):
    driver_name.axis0.controller.config.control_mode = CONTROL_MODE_VELOCITY_CONTROL

    motor_kv = 115
    torque_const = 8.27 / motor_kv

    initial_pos = driver_name.axis0.controller.input_pos
    plot_rate = 1/100
    
    plot_graphs = False
    
    if plot_graphs:
        input_vel_plot = []
        output_torque_plot = []
        output_pos_plot = []
        output_vel_plot = []
        vel_error = []
        t_plot = []
        
        plt.figure(figsize=(100, 25))
        plt.suptitle('Odrive Output', fontsize=75)
        plt.subplot(211)

    for i in range(len(elbow_torque)):
        try:
            t = i * plot_rate
            input_vel = elbow_vel[i]

            driver_name.axis0.controller.input_vel = input_vel_plot
            clear_errors(driver_name)

            output_pos, output_vel, output_curr = get_motor_state(driver_name)
            
            print("Position: {} [turn]\t Velocity: {} [turn/s]\t Current: {} [A]\t Velocity Error: {} [deg/s]".format(
                output_pos, output_vel, output_curr, (input_vel - output_vel)*360))

            if plot_graphs:
                input_vel_plot.append(input_vel)
                output_pos_plot.append(output_pos)
                output_vel_plot.append(output_vel)
                output_torque_plot.append(-output_curr * torque_const)
                vel_error.append((input_vel - output_vel)*360)
                t_plot.append(t)

                plt.scatter(t, input_vel, c="blue")
                plt.scatter(t, output_vel, c="red")
                
            time.sleep(plot_rate)

        except:
            print("Couldn't complete motion. shutting down")
            shut_down(driver_name)
            raise
    
    if plot_graphs:
        plt.plot(t_plot, input_vel_plot, c="blue", label="Input velocity")
        plt.plot(t_plot, output_vel_plot, c="red", label="Output velocity")
        plt.ylabel('Torque [Nm]', fontsize=40)
        plt.xlabel('Time [sec]', fontsize=40)
        plt.grid()
        plt.title('Input & Output torque', fontsize=20)
        plt.legend(fontsize=50)

        plt.subplot(212)
        plt.plot(t_plot, vel_error, label="Position error")
        plt.ylabel('Error [deg]', fontsize=40)
        plt.xlabel('Time [sec]', fontsize=40)
        plt.grid()
        plt.title('Velocity Error', fontsize=20)
        plt.legend(fontsize=50)

        plt.savefig("output.png")


def current_control(driver_name, elbow_pos, elbow_torque):
    driver_name.axis0.controller.config.control_mode = CONTROL_MODE_TORQUE_CONTROL

    motor_kv = 115
    torque_const = 8.27 / motor_kv

    initial_pos = driver_name.axis0.controller.input_pos
    plot_rate = 1/100
    
    plot_graphs = False
    
    if plot_graphs:
        input_torque_plot = []
        output_torque_plot = []
        output_pos_plot = []
        output_vel_plot = []
        t_plot = []
        
        plt.figure(figsize=(100, 25))
        plt.suptitle('Odrive Output', fontsize=75)
        plt.subplot(211)

    for i in range(len(elbow_torque)):
        try:
            t = i * plot_rate
            input_torque = elbow_torque[i]

            driver_name.axis0.controller.input_torque = input_torque
            clear_errors(driver_name)

            output_pos, output_vel, output_curr = get_motor_state(driver_name)
            output_torque = -output_curr * torque_const
            
            print("Position: {} [turn]\t Velocity: {} [turn/s]\t Current: {} [A]\t Current Error: {} [Nm]".format(
                output_pos, output_vel, output_curr, input_torque - output_torque))

            if plot_graphs:
                input_torque_plot.append(input_torque)
                output_pos_plot.append(output_pos - initial_pos)
                output_vel_plot.append(output_vel)
                output_torque_plot.append(output_torque)
                t_plot.append(t)

                plt.scatter(t, input_torque, c="blue")
                plt.scatter(t, output_torque, c="red")
                
            time.sleep(plot_rate)

        except:
            print("Couldn't complete motion. shutting down")
            shut_down(driver_name)
            raise
    
    if plot_graphs:
        plt.plot(t_plot, input_torque_plot, c="blue", label="Input torque")
        plt.plot(t_plot, output_torque_plot, c="red", label="Output torque")
        plt.ylabel('Torque [Nm]', fontsize=50)
        plt.xlabel('Time [sec]', fontsize=50)
        plt.grid()
        plt.title('Input & Output torque', fontsize=20)
        plt.legend(fontsize=50)

        plt.subplot(212)
        plt.plot(t_plot, output_pos_plot, c="blue", label="Output position")
        plt.plot(t_plot, output_vel_plot, c="red", label="Output velocity")
        plt.plot(t_plot, output_torque_plot, c="green", label="Output torque")
        plt.xlabel('Time [sec]', fontsize=50)
        plt.grid()
        plt.title('Output Angle, Velocity & Torque', fontsize=20)
        plt.legend(fontsize=50)

        plt.savefig("output.png")


def main(args):
    use_double_pendulum = False

    # Find a connected ODrive (this will block until you connect one)
    print("Finding an ODrive...")
    odrv0 = odrive.find_any()

    if args["calibration"]:
        # Calibrate motor
        Calibration(odrv0)

    # Switching ti closed loop control stateboards
    odrv0.axis0.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL
    odrv0.axis0.controller.config.input_mode = INPUT_MODE_PASSTHROUGH
    output_pos, output_vel, output_current = get_motor_state(odrv0)

    # To read a value, simply read the property
    print("The boards main supply voltage is {}V".format(str(odrv0.vbus_voltage)))
    print("The motor initial positionis {}".format(output_pos))

    data_file_dict = {"0.5ms": "05ms.csv", "0.6ms": "06ms.csv", "0.7ms": "07ms.csv", "0.8ms": "08ms.csv", "0.9ms": "09ms.csv",
                      "1.0ms": "10ms.csv", "1.1ms": "11ms.csv", "1.2ms": "12ms.csv", "1.3ms": "13ms.csv", "1.4ms": "14ms.csv"}

    data_dir = '../data/my_data'
    data_file_name = data_file_dict[args["velocity"]]

    data_rows = load_dataset(data_file_name, data_dir)

    single_pend_elbow_position = []
    single_pend_elbow_torque = []
    double_pend_elbow_position = []
    double_pend_elbow_torque = []

    for row in data_rows:
        position, torque = row.strip().split(",")

        single_pend_elbow_position.append(float(position[1:-1]))
        single_pend_elbow_torque.append(float(torque[1:-1]))

    if use_double_pendulum:
        elbow_pos = double_pend_elbow_position
        elbow_torque = double_pend_elbow_torque
    else:
        elbow_pos = single_pend_elbow_position[:2000]
        elbow_torque = single_pend_elbow_torque[:2000]

    if args["control"] == "position":
        position_control(odrv0, elbow_pos, elbow_torque)

    elif args["control"] == "velocity":
        velocity_control(odrv0, elbow_pos, elbow_torque)

    elif args["control"] == "current":
        current_control(odrv0, elbow_pos, elbow_torque)

    else:
        print("Control mode is invalid")

    print("Finished motion. shutting down")
    # shut_down(odrv0)


if __name__ == '__main__':
    # construct the argument parse and parse the arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("--calibration", default=False, help="calibrate motor")
    parser.add_argument(
        "--control", help="control mode: current, position, or velocity")
    parser.add_argument("--velocity", help="walking velocity")
    args = vars(parser.parse_args())

    time.sleep(3)
    main(args)
