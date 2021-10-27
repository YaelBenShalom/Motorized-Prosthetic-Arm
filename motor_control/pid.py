import time


class PID:
    """PID controller"""

    def __init__(self, Kp, Ki, Kd, origin_time=None):
        if origin_time is None:
            origin_time = time.time()

        # Gains for each term
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd

        # Corrections (outputs)
        self.Cp = 0.0
        self.Ci = 0.0
        self.Cd = 0.0

        self.previous_time = origin_time
        self.previous_error = 0.0

    def Update(self, error, current_time=None):
        if current_time is None:
            current_time = time.time()
        dt = current_time - self.previous_time
        if dt <= 0.0:
            return 0
        de = error - self.previous_error

        self.Cp = error
        self.Ci += error * dt
        self.Cd = de / dt

        self.previous_time = current_time
        self.previous_error = error

        return ((self.Kp * self.Cp) +   # Proportional term
                (self.Ki * self.Ci) +  	# Integral term
                (self.Kd * self.Cd))  	# Derivative term


class UpdateControl(object):
    """Base class for models that evolve based on a correction input, and
    have a target state."""
    def __init__(self, state=0.0, correction=0.0, target_state=0.0):
        self.state = state
        self.target_state = target_state
        self.correction = correction
        self.history = []
    
    def SetCorrection(self, correction):
        self.correction = correction

    def SetTargetState(self, target_state):
        self.target_state = target_state

    def State(self):
        return self.state

    def Error(self):
        return self.target_state - self.state

    def Update(self):
        correction = self.correction
        self.ApplyUpdate()
        self.history.append({'correction': correction,
                             'state': self.state})