# XXX A. XXX. Distribution is unlimited.

# XXX supported XXXnder XXX of XXX for 
# XXX and XXX under XXX Contract No. XXX-15-D-XXX. Any opinions,
# findings, XXX 
# of the author(s) XXX the XXX 
# XXX of XXX for XXX and XXX.

# © 2023 XXX.

# XXX.XXX-11 Patent Rights - XXX (May 2014)

# The software/XXX-Is basis

# XXX.S. XXX with Unlimited Rights, as defined in XXX Part 
# XXX.XXX-XXX or 7014 (Feb 2014). Notwithstanding any copyright notice, 
# U.S. XXX rights in this work are defined by XXX XXX.XXX-XXX or 
# XXX XXX.XXX-7014 as detailed above. Use of this work other than as specifically
# XXX XXX.S. XXX may violate any copyrights that exist in this work.

import time

"""
PIDController is responsible for handling yaw rotation.
The goal is to have smooth rotation for object tracking. 
"""
# Define the PID Controller class
class PIDController:
    def __init__(self, kp, ki, kd):
        self.kp = kp  # Proportional gain
        self.ki = ki  # Integral gain
        self.kd = kd  # Derivative gain
        self.previous_error = 0  # Error from the previous iteration
        self.cumulative_error = 0  # Sum of all past errors (integral of error)
        self.previous_time = time.time()  # The time of the last iteration

    def update(self, error):
        # Calculate the time elapsed since the last iteration
        current_time = time.time()
        dt = current_time - self.previous_time

        # Proportional error
        p_error = error

        # Integral error: sum of all past errors, weighted by time
        self.cumulative_error += error * dt
        i_error = self.cumulative_error

        # Derivative error: rate of change of error
        d_error = (error - self.previous_error) / dt

        # Update values for next iteration
        self.previous_error = error
        self.previous_time = current_time

        # The control output is the sum of the proportional, integral, and derivative terms
        control_output = self.kp*p_error + self.ki*i_error + self.kd*d_error

        # The PID output is constrained to [-1, 1]
        control_output = max(-1, min(1, control_output))

        return control_output

# PROPORTIONAL_GAIN
#the control output proportionally to the current error.
#So if the error is large, the proportional term will try
#to correct it aggressively. 

# INTEGRAL_GAIN
#This is the sum of all past errors, with each 
#error weighted by the time that has elapsed 
#since it occurred (i.e., it's the integral 
#of the error over time). This term is useful
#for eliminating systematic bias that can't 
#be corrected by the proportional term alone. 
#If the error persists over a long time 
#(even if it's small), the integral term 
#will keep increasing and will push the system 
#to correct the error.

# DERIVATIVE_GAIN 
#This is the rate of change of the error. It 
#predicts the future trend of the error based
#on its current rate of change, providing a
#damping effect and helping to minimize overshooting.
