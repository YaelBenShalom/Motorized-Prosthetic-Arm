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


def main():
    # Find a connected ODrive
    print("Finding an odrive...")
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
        vel = math.sin((time.monotonic() - t0)*2)
        print("Moving at {} [turn/s]".format(str(int(vel))))
        odrv0.axis0.controller.input_vel = vel
        if odrv0.error != 0 or odrv0.axis0.error != 0:
            print("Error!!")
            break
        time.sleep(0.01)

        if time.monotonic() - t0 > 11:
            odrv0.axis0.controller.input_vel = 0
            break

if __name__ == '__main__':
    main()