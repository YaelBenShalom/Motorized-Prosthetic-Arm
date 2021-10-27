import time


class PID:
    """ PID controller.
    """

    def __init__(self, Kp, Ki, Kd, init_time=None):
        """ Initialize the PID controller gains and corrections.
        Input:
          Kp                Proportional gain
          Kp                Proportional gain
          Kp                Proportional gain
          init_time         The initial time
        Output:
          None
        """
        if init_time is None:
            init_time = time.time()

        # Gains for each term
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd

        # Corrections (outputs)
        self.Cp = 0.0
        self.Ci = 0.0
        self.Cd = 0.0

        self.previous_time = init_time
        self.previous_error = 0.0

    def Update(self, error, current_time=None):
        """ Initialize the PID controller gains and corrections.
        Input:
          error             Current error
          current_time      The current time
        Output:
          new_terms         The new terms after update
        """
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

        new_terms = ((self.Kp * self.Cp) +   # Proportional term
                     (self.Ki * self.Ci) +  	# Integral term
                     (self.Kd * self.Cd))  	# Derivative term

        return new_terms


class UpdateControl(object):
    """ Base class for models that evolve based on a correction input, and
    have a target state.
    """

    def __init__(self, state=0.0, correction=0.0, target_state=0.0):
        """ Update the state.
        Input:
          state             Current state
          correction        Required correction
          target_state      Required target state
        Output:
          None
        """
        self.state = state
        self.target_state = target_state
        self.correction = correction
        self.history = []

    def SetCorrection(self, correction):
        """ Set the correction
        Input:
          correction        Required correction
        Output:
          None
        """
        self.correction = correction

    def SetTargetState(self, target_state):
        """ Set the target state
        Input:
          target_state      Required target state
        Output:
          None
        """
        self.target_state = target_state

    def GetState(self):
        """ Set the current state
        Input:
          None
        Output:
          state      Current state
        """
        return self.state

    def GetError(self):
        """ Set the current error
        Input:
          None
        Output:
          error      Current error
        """
        error = self.target_state - self.state
        return error

    def Update(self):
        """ Update the state and correction
        Input:
          None
        Output:
          None
        """
        correction = self.correction
        self.ApplyUpdate()
        self.history.append({'correction': correction,
                             'state': self.state})
