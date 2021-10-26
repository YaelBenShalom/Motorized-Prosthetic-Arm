# Set up for T-motor R60 KV115:

# Hardware Configuration:
odrv0.config.enable_brake_resistor = True
odrv0.config.brake_resistance = 0.5 # [Ohm]
odrv0.config.dc_max_negative_current = 10*10**(-6) # [Amps]

# Motor Configuration:
odrv0.axis0.motor.config.current_lim = 60.0 # [A]
odrv0.axis0.motor.config.requested_current_range = 90.0 # [A]
odrv0.axis0.motor.config.calibration_current = 10.0 # [A]
odrv0.axis0.motor.config.pole_pairs = 14
odrv0.axis0.motor.config.torque_constant = 8.27 / 115
odrv0.axis0.motor.config.motor_type = MOTOR_TYPE_HIGH_CURRENT

# Encoder Configuration:
odrv0.axis0.encoder.config.abs_spi_cs_gpio_pin = 4
odrv0.axis1.encoder.config.abs_spi_cs_gpio_pin = 3
odrv0.axis0.encoder.config.mode = ENCODER_MODE_SPI_ABS_AMS
odrv0.axis0.encoder.config.cpr = 2**14

# Controller Configuration:
odrv0.axis0.controller.config.vel_limit = 5.0 # [turn/s]

# Save configuration:
odrv0.save_configuration()

# Motor Calibration:
odrv0.axis0.requested_state = AXIS_STATE_FULL_CALIBRATION_SEQUENCE

# Encoder Calibration:
odrv0.axis0.requested_state = AXIS_STATE_ENCODER_OFFSET_CALIBRATION

# Enable closed loop control:
odrv0.axis0.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL  

# Error Handling:
dump_errors(odrv0)  
dump_errors(odrv0, True)
