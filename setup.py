# Set up for T-motor R60 KV115:

import odrive

odrv0 = odrive.find_any()

# Hardware Configuration:
odrv0.config.enable_brake_resistor = True
odrv0.config.brake_resistance = 0.5  # [Ohm]
odrv0.config.dc_max_negative_current = -10*10**(-6)  # [Amps]

# Motor Configuration:
odrv0.axis0.motor.config.current_lim = 10.0  # [A]
odrv0.axis0.motor.config.requested_current_range = 60.0  # [A]
odrv0.axis0.motor.config.calibration_current = 10.0  # [A]
odrv0.axis0.motor.config.pole_pairs = 14
odrv0.axis0.motor.config.torque_constant = 8.27 / 115
odrv0.axis0.motor.config.motor_type = MOTOR_TYPE_HIGH_CURRENT

# Encoder Configuration:
odrv0.axis0.encoder.config.abs_spi_cs_gpio_pin = 4
odrv0.axis1.encoder.config.abs_spi_cs_gpio_pin = 3
odrv0.axis0.encoder.config.mode = ENCODER_MODE_SPI_ABS_AMS
odrv0.axis0.encoder.config.cpr = 2**14

# Controller Configuration:
odrv0.axis0.controller.config.vel_limit = 3.0  # [turn/s]

# Tuning Gains:
odrv0.axis0.controller.config.pos_gain = 150.0  # [(turn/s) / turn]
odrv0.axis0.controller.config.vel_gain = 0.3  # [Nm/(turn/s)]
odrv0.axis0.controller.config.vel_integrator_gain = 0.15  # [Nm/((turn/s) * s)]

# Save configuration:
odrv0.axis0.requested_state = AXIS_STATE_IDLE
odrv0.save_configuration()

# Motor Calibration:
odrv0.axis0.requested_state = AXIS_STATE_FULL_CALIBRATION_SEQUENCE

# Encoder Calibration:
odrv0.axis0.requested_state = AXIS_STATE_ENCODER_OFFSET_CALIBRATION

# Enable closed loop control:
odrv0.axis0.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL

# Save Motor and Encoder Offset Calibration:
odrv0.axis0.encoder.config.pre_calibrated = True
odrv0.axis0.motor.config.pre_calibrated = True
odrv0.axis0.encoder.config.pre_calibrated

# Error Handling:
odrv0.axis0.controller.input_posodrv0.clear_errors()
