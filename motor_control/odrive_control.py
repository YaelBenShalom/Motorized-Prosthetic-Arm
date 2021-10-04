from __future__ import print_function

import odrive
from odrive.utils import start_liveplotter
from odrive.enums import *
import time
import math


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


def get_motor_state(driver_name):
    motor_pos =  driver_name.axis0.encoder.pos_estimate
    motor_vel =  driver_name.axis0.encoder.vel_estimate
    motor_current = driver_name.axis0.motor.current_control.Iq_setpoint

    return motor_pos, motor_vel, motor_current


def main():
    # Find a connected ODrive
    print("Finding an ODrive...")
    odrv0 = odrive.find_any()

    # Calibrate motor and wait for it to finish
    print("Starting calibration...")
    odrv0.axis0.requested_state = AXIS_STATE_FULL_CALIBRATION_SEQUENCE
    while odrv0.axis0.current_state != AXIS_STATE_IDLE:
        time.sleep(0.1)

    odrv0.axis0.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL
    odrv0.axis0.controller.config.input_mode = INPUT_MODE_PASSTHROUGH
    # odrv0.axis0.controller.config.control_mode = CONTROL_MODE_POSITION_CONTROL

    # To read a value, simply read the property
    print("The boards main supply voltage is {}V".format(str(odrv0.vbus_voltage)))

    liveplot(odrv0)

    # A sine wave to test
    # t0 = time.monotonic()
    # while True:
    #     setpoint = 4.0 * math.sin((time.monotonic() - t0)*2)
    #     print("Going to {}".format(str(int(setpoint))))
    #     odrv0.axis0.controller.input_pos = setpoint
    #     if odrv0.error != 0 or odrv0.axis0.error != 0:
    #         print("Error!!")
    #         break
    #     time.sleep(0.01)

    odrv0.axis0.controller.config.control_mode = CONTROL_MODE_VELOCITY_CONTROL

    # A sine wave to test
    t0 = time.monotonic()
    while True:
        try:
            vel = math.sin((time.monotonic() - t0)*2)
            odrv0.axis0.controller.input_vel = vel
            clear_errors(odrv0)

            output_pos, output_vel, output_current = get_motor_state(odrv0)
            # print("Moving to {} [turn]".format(output_pos))
            # print("Moving at {} [turn/s]".format(output_vel))
            # print("Motor current is {} [A]".format(output_current))
            print("The velocity error is {} [turn/s]".format(vel - output_vel))

            time.sleep(0.01)

            if time.monotonic() - t0 > 11:
                odrv0.axis0.controller.input_vel = 0
                break

        except:
            print("Shutting down")
            odrv0.axis0.controller.input_vel = 0
            raise


if __name__ == '__main__':
    main()
