# Imports required for data processing
import os
import csv
import pandas as pd

# Imports required for dynamics calculations
import sympy
from sympy.abc import t
from sympy import symbols, Eq, Function, solve, sin, cos, Matrix, simplify, symbols, lambdify
from math import pi
import numpy as np
import matplotlib.pyplot as plt

# Imports required for animation
from plotly.offline import init_notebook_mode, iplot
from IPython.display import display, HTML
import plotly.graph_objects as go


def main():

    #########################################################################################################
    ####################################  Define the system's constants  ####################################
    #########################################################################################################

    # Masses, length and center-of-mass positions (calculated using the lab measurements)
    # Mass calculations (mass unit is kg) 
    # m_body = 90.6                         # Average weights for American adult male
                                            # from "Anthropometric Reference Data for Children and Adults:
                                            # United States, 2015–2018"

    m_body_dict = {'ID': 51.0, 'JD': 79.5, 'JR': 76.0, 'KS': 59.3, 'KW': 63.8, 'LC': 61.2,
                   'LD': 97.3, 'LS': 82.2, 'MK': 93.5, 'MV': 98.5, 'SM': 68.5, 'TD': 70.0,
                   'TM': 66.2}

    m_u_const = 0.028                       # Average upper arm weights relative to body weight, from “Biomechanics
                                            # and Motor Control of Human Movement” by David Winter (2009), 4th edition
                                            # m_upper_arm = 0.028 * m_body  

    m_upper_arm_dict = {'ID': m_u_const * m_body_dict['ID'], 'JD': m_u_const * m_body_dict['JD'],
                        'JR': m_u_const * m_body_dict['JR'], 'KS': m_u_const * m_body_dict['KS'],
                        'KW': m_u_const * m_body_dict['KW'], 'LC': m_u_const * m_body_dict['LC'],
                        'LD': m_u_const * m_body_dict['LD'], 'LS': m_u_const * m_body_dict['LS'],
                        'MK': m_u_const * m_body_dict['MK'], 'MV': m_u_const * m_body_dict['MV'],
                        'SM': m_u_const * m_body_dict['SM'], 'TD': m_u_const * m_body_dict['TD'],
                        'TM': m_u_const * m_body_dict['TM']}

    m_lower_arm = 0.7395                    # Average lower prosthetics weights, calculated using lab measurements  

    # Arm length calculations (length unit is m) 
    # H_body = 1.769                        # Average height for American adult male, from “Height and body-mass 
                                            # index trajectories of school-aged children and adolescents from 
                                            # 1985 to 2019 in 200 countries and territories: a pooled analysis 
                                            # of 2181 population-based studies with 65 million participants”

    H_body_dict = {'ID': 1.620, 'JD': 1.760, 'JR': 1.770, 'KS': 1.640, 'KW': 1.620, 'LC': 1.580,
                   'LD': 1.875, 'LS': 1.635, 'MK': 1.780, 'MV': 1.805, 'SM': 1.790, 'TD': 1.690,
                   'TM': 1.735}

    L_u_const = 0.186                       # Average upper arm length relative to body height
                                            # from “Biomechanics and Motor Control of Human Movement” by David
                                            # Winter (2009), 4th edition
                                            # L_upper_arm = 0.186 * H_body

    L_upper_arm_dict = {'ID': L_u_const * H_body_dict['ID'], 'JD': L_u_const * H_body_dict['JD'],
                        'JR': L_u_const * H_body_dict['JR'], 'KS': L_u_const * H_body_dict['KS'],
                        'KW': L_u_const * H_body_dict['KW'], 'LC': L_u_const * H_body_dict['LC'],
                        'LD': L_u_const * H_body_dict['LD'], 'LS': L_u_const * H_body_dict['LS'],
                        'MK': L_u_const * H_body_dict['MK'], 'MV': L_u_const * H_body_dict['MV'],
                        'SM': L_u_const * H_body_dict['SM'], 'TD': L_u_const * H_body_dict['TD'],
                        'TM': L_u_const * H_body_dict['TM']}

    L_lower_arm = 0.42                      # Average lower prosthetics length, calculated using lab measurements 

    # Arm center of mass length calculations (length unit is m) 
    L_u_COM_const = 0.436                   # Average upper arm length from shoulder to center of mass relative
                                            # to upper arm length, from “Biomechanics and Motor Control of Human
                                            # Movement” by David Winter (2009), 4th edition
                                            # L_upper_arm_COM = 0.436 * L_upper_arm

    L_upper_arm_COM_dict = {'ID': L_u_COM_const * L_upper_arm_dict['ID'], 'JD': L_u_COM_const * L_upper_arm_dict['JD'],
                            'JR': L_u_COM_const * L_upper_arm_dict['JR'], 'KS': L_u_COM_const * L_upper_arm_dict['KS'],
                            'KW': L_u_COM_const * L_upper_arm_dict['KW'], 'LC': L_u_COM_const * L_upper_arm_dict['LC'],
                            'LD': L_u_COM_const * L_upper_arm_dict['LD'], 'LS': L_u_COM_const * L_upper_arm_dict['LS'],
                            'MK': L_u_COM_const * L_upper_arm_dict['MK'], 'MV': L_u_COM_const * L_upper_arm_dict['MV'],
                            'SM': L_u_COM_const * L_upper_arm_dict['SM'], 'TD': L_u_COM_const * L_upper_arm_dict['TD'],
                            'TM': L_u_COM_const * L_upper_arm_dict['TM']}
        
    L_lower_arm_COM = 0.2388                # Average lower prosthetics length from elbow to center of mass,
                                            # calculated using lab measurements 


    #########################################################################################################
    ###########################################  Extracting Data  ###########################################
    #########################################################################################################

    # Extracting angles data and computing angular velocities and angular accelerations from the angles:
    def calculate_Vel(Ang_list, time_list, index):
        return ((Ang_list[index + 1] - Ang_list[index])
            / (time_list[index + 1] - time_list[index]))


    def calculate_Acc(Vel_list, time_list, index):
        return ((Vel_list[index + 1] - Vel_list[index])
            / (time_list[index + 1] - time_list[index]))


    data_csv_dir = '../../data/control_data/CSV Converted Files'
    frame_frequency = 120
    print("current directory: ", os.getcwd())

    participants_list = []
    time_list = []
    Elbow_Ang_list = []
    Shl_Flex_Ang_list = []
    Elbow_Vel_list = []
    Shl_Flex_Vel_list = []
    Elbow_Acc_list = []
    Shl_Flex_Acc_list = []

    for file in os.listdir(data_csv_dir):
        file_name = file.split(".")[0]
        participant_name = file.split("_")[0]
        
        if file.endswith(".csv"):
            frame = 0
            file_time_list = []
            file_R_Elbow_Ang_list = []
            file_R_Shl_Flex_Ang_list = []
            file_L_Elbow_Ang_list = []
            file_L_Shl_Flex_Ang_list = []
            file_R_Elbow_Vel_list = []
            file_R_Shl_Flex_Vel_list = []
            file_L_Elbow_Vel_list = []
            file_L_Shl_Flex_Vel_list = []
            file_R_Elbow_Acc_list = []
            file_R_Shl_Flex_Acc_list = []
            file_L_Elbow_Acc_list = []
            file_L_Shl_Flex_Acc_list = []

            data_path = os.path.join(data_csv_dir, file)
            
            # Cutting out weird data behavior on data edges
            if file == 'TD_WN7.csv':
                data_rows = open(data_path).read().strip().split("\n")[40:]
            elif file == 'TD_WN4.csv':
                data_rows = open(data_path).read().strip().split("\n")[24:-12]    
            elif file == 'TD_WN11.csv':
                data_rows = open(data_path).read().strip().split("\n")[24:-3]               
            else:
                data_rows = open(data_path).read().strip().split("\n")[24:]
            
            # Extract time [sec], elbow angles [rad], and shoulder angles [rad] from data
            for row in data_rows:
                splitted_row = row.strip().split("\t")

                # Check if loop finished all data
                if len(splitted_row) < 80:
                    break

                file_time_list.append(frame/frame_frequency)
                file_R_Elbow_Ang_list.append(float(splitted_row[9]) * 2*pi/360)
                file_R_Shl_Flex_Ang_list.append(float(splitted_row[11]) * 2*pi/360)
                file_L_Elbow_Ang_list.append(float(splitted_row[21]) * 2*pi/360)
                file_L_Shl_Flex_Ang_list.append(float(splitted_row[23]) * 2*pi/360)
                frame += 1

            # Extract elbow and shoulder velocities [rad/sec] from angles
            for i in range(len(file_time_list) - 1):
                R_Elbow_Vel = calculate_Vel(file_R_Elbow_Ang_list, file_time_list, i)
                R_Shl_Flex_Vel = calculate_Vel(file_R_Shl_Flex_Ang_list, file_time_list, i)
                L_Elbow_Vel = calculate_Vel(file_L_Elbow_Ang_list, file_time_list, i)
                L_Shl_Flex_Vel = calculate_Vel(file_L_Shl_Flex_Ang_list, file_time_list, i)
                
                file_R_Elbow_Vel_list.append(R_Elbow_Vel)
                file_R_Shl_Flex_Vel_list.append(R_Shl_Flex_Vel)
                file_L_Elbow_Vel_list.append(L_Elbow_Vel)
                file_L_Shl_Flex_Vel_list.append(L_Shl_Flex_Vel)

            # Extract elbow and shoulder Accelerations [rad/sec^2] from velocities
            for i in range(len(file_time_list) - 2):
                R_Elbow_Acc = calculate_Acc(file_R_Elbow_Vel_list, file_time_list, i)
                R_Shl_Flex_Acc = calculate_Acc(file_R_Shl_Flex_Vel_list, file_time_list, i)
                L_Elbow_Acc = calculate_Acc(file_L_Elbow_Vel_list, file_time_list, i)
                L_Shl_Flex_Acc = calculate_Acc(file_L_Shl_Flex_Vel_list, file_time_list, i)
                
                file_R_Elbow_Acc_list.append(R_Elbow_Acc)
                file_R_Shl_Flex_Acc_list.append(R_Shl_Flex_Acc)
                file_L_Elbow_Acc_list.append(L_Elbow_Acc)
                file_L_Shl_Flex_Acc_list.append(L_Shl_Flex_Acc)

            # Adjust lists length
            file_time_list = file_time_list[:-2]
            file_R_Elbow_Ang_list = file_R_Elbow_Ang_list[:-2]
            file_R_Shl_Flex_Ang_list = file_R_Shl_Flex_Ang_list[:-2]
            file_L_Elbow_Ang_list = file_L_Elbow_Ang_list[:-2]
            file_L_Shl_Flex_Ang_list = file_L_Shl_Flex_Ang_list[:-2]

            file_R_Elbow_Vel_list = file_R_Elbow_Vel_list[:-1]
            file_R_Shl_Flex_Vel_list = file_R_Shl_Flex_Vel_list[:-1]
            file_L_Elbow_Vel_list = file_L_Elbow_Vel_list[:-1]
            file_L_Shl_Flex_Vel_list = file_L_Shl_Flex_Vel_list[:-1]

            participants_list.append(participant_name)
            participants_list.append(participant_name)

            time_list.append(file_time_list)
            time_list.append(file_time_list)

            Elbow_Ang_list.append(file_R_Elbow_Ang_list)
            Shl_Flex_Ang_list.append(file_R_Shl_Flex_Ang_list)        
            Elbow_Ang_list.append(file_L_Elbow_Ang_list)
            Shl_Flex_Ang_list.append(file_L_Shl_Flex_Ang_list)
            Elbow_Vel_list.append(file_R_Elbow_Vel_list)
            Shl_Flex_Vel_list.append(file_R_Shl_Flex_Vel_list)        
            Elbow_Vel_list.append(file_L_Elbow_Vel_list)
            Shl_Flex_Vel_list.append(file_L_Shl_Flex_Vel_list)
            Elbow_Acc_list.append(file_R_Elbow_Acc_list)
            Shl_Flex_Acc_list.append(file_R_Shl_Flex_Acc_list)        
            Elbow_Acc_list.append(file_L_Elbow_Acc_list)
            Shl_Flex_Acc_list.append(file_L_Shl_Flex_Acc_list)


    #########################################################################################################
    ###########################################  System Modeling  ###########################################
    #########################################################################################################

    # Computing the Lagrangian of the system:
    m1, m2, g, R1, R1_COM, R2, R2_COM = symbols(r'm1, m2, g, R1, R1_COM, R2, R2_COM')

    # The system torque variables as function of t
    tau1 = Function(r'tau1')(t)
    tau2 = Function(r'tau2')(t)

    # The system configuration variables as function of t
    theta1 = Function(r'theta1')(t)
    theta2 = Function(r'theta2')(t)

    # The velocity as derivative of position wrt t
    theta1_dot = theta1.diff(t)
    theta2_dot = theta2.diff(t)

    # The acceleration as derivative of velocity wrt t
    theta1_ddot = theta1_dot.diff(t)
    theta2_ddot = theta2_dot.diff(t)

    # Converting the polar coordinates to cartesian coordinates
    x1 = R1_COM*sin(theta1)
    x2 = R1*sin(theta1) + R2_COM*sin(theta1 + theta2)

    y1 = -R1_COM*cos(theta1)
    y2 = -R1*cos(theta1) - R2_COM*cos(theta1 + theta2)

    # Calculating the kinetic and potential energy of the system
    KE = 1/2*m1*((x1.diff(t))**2 + (y1.diff(t))**2) + 1/2*m2*((x2.diff(t))**2 + (y2.diff(t))**2)
    PE = m1*g*y1 + m2*g*y2

    # Computing the Lagrangian
    L = simplify(KE - PE)
    print('L: {} \n'.format(L))

    # Computing the Euler-Lagrange equations:
    # Define the derivative of L wrt the functions: x, xdot
    L_dtheta1 = L.diff(theta1)
    L_dtheta2 = L.diff(theta2)

    L_dtheta1_dot = L.diff(theta1_dot)
    L_dtheta2_dot = L.diff(theta2_dot)

    # Define the derivative of L_dxdot wrt to time t
    L_dtheta1_dot_dt = L_dtheta1_dot.diff(t)
    L_dtheta2_dot_dt = L_dtheta2_dot.diff(t)

    # Define the left hand side of the the Euler-Lagrange as a matrix
    lhs = Matrix([simplify(L_dtheta1_dot_dt - L_dtheta1),
                  simplify(L_dtheta2_dot_dt - L_dtheta2)
                ])

    # Define the right hand side of the the Euler-Lagrange as a Matrix
    rhs = Matrix([tau1, tau2])

    # Compute the Euler-Lagrange equations as a matrix
    EL_eqns = Eq(lhs, rhs)

    print('Euler-Lagrange matrix for this systems: {} \n'.format(EL_eqns))


    # Solve the equations for 𝜏1 and 𝜏2 :
    # Solve the Euler-Lagrange equations for the shoulder and elbow torques
    T = Matrix([tau1, tau2])
    soln = solve(EL_eqns, T, dict=True)

    # Initialize the solutions
    solution = [0, 0]
    i = 0

    for sol in soln:
        for v in T:
            solution[i] = simplify(sol[v])
            print('{} \n'.format(Eq(T[i], solution[i])))
            i =+ 1

    # Simulating the system:
    # Substitute the derivative variables with a dummy variables and plug-in the constants
    solution_0_subs = solution[0]
    solution_1_subs = solution[1]

    theta1_dot_dummy = symbols('dtheta1')
    theta2_dot_dummy = symbols('dtheta2')
    theta1_ddot_dummy = symbols('ddtheta1')
    theta2_ddot_dummy = symbols('ddtheta2')

    solution_0_subs = solution_0_subs.subs([(g, 9.81)])
    solution_1_subs = solution_1_subs.subs([(g, 9.81)])

    solution_0_subs = solution_0_subs.subs([((theta1.diff(t)).diff(t), theta1_ddot_dummy),
                                            ((theta2.diff(t)).diff(t), theta2_ddot_dummy)])
    solution_1_subs = solution_1_subs.subs([((theta1.diff(t)).diff(t), theta1_ddot_dummy),
                                            ((theta2.diff(t)).diff(t), theta2_ddot_dummy)])

    solution_0_subs = solution_0_subs.subs([(theta1.diff(t), theta1_dot_dummy),
                                            (theta2.diff(t), theta2_dot_dummy)])
    solution_1_subs = solution_1_subs.subs([(theta1.diff(t), theta1_dot_dummy),
                                            (theta2.diff(t), theta2_dot_dummy)])

    print(solution_0_subs)
    print(solution_1_subs)

    # Lambdify the thetas and its derivatives
    func1 = lambdify([theta1, theta2, theta1_dot_dummy, theta2_dot_dummy, theta1_ddot_dummy,
                    theta2_ddot_dummy, m1, m2, R1, R2, R1_COM, R2_COM], solution_0_subs, modules = sympy)
    func2 = lambdify([theta1, theta2, theta1_dot_dummy, theta2_dot_dummy, theta1_ddot_dummy,
                    theta2_ddot_dummy, m1, m2, R1, R2, R1_COM, R2_COM], solution_1_subs, modules = sympy)

    # Initialize the torque and power lists
    Shl_Flex_tau_list, Elbow_tau_list = [], []
    Shl_Flex_power_list, Elbow_power_list = [], []

    for i in range(len(time_list)):
        # Initialize the torque and power lists
        tau1_list, tau2_list = [], []
        power1_list, power2_list = [], []

        t_list = time_list[i]
        theta1_list = Shl_Flex_Ang_list[i]
        theta2_list = Elbow_Ang_list[i]
        dtheta1_list = Shl_Flex_Vel_list[i]
        dtheta2_list = Elbow_Vel_list[i]
        ddtheta1_list = Shl_Flex_Acc_list[i]
        ddtheta2_list = Elbow_Acc_list[i]

        # Plug-in the angles, angular velocities and angular accelerations for every time step to find the torques
        for j in range(len(t_list)):
            tau1_list.append(func1(theta1_list[j], theta2_list[j], dtheta1_list[j], dtheta2_list[j],
                                   ddtheta1_list[j], ddtheta2_list[j], m_upper_arm_dict[participants_list[i]],
                                   m_lower_arm, L_upper_arm_dict[participants_list[i]], L_lower_arm,
                                   L_upper_arm_COM_dict[participants_list[i]], L_lower_arm_COM))
            
            tau2_list.append(func2(theta1_list[j], theta2_list[j], dtheta1_list[j], dtheta2_list[j],
                                   ddtheta1_list[j], ddtheta2_list[j], m_upper_arm_dict[participants_list[i]],
                                   m_lower_arm, L_upper_arm_dict[participants_list[i]], L_lower_arm,
                                   L_upper_arm_COM_dict[participants_list[i]], L_lower_arm_COM))

            # Calculate the power required to reach the required angular velocities and joints torques for every time step
            power1_list.append(dtheta1_list[j] * tau1_list[j])
            power2_list.append(dtheta2_list[j] * tau2_list[j])
        
        Shl_Flex_tau_list.append(tau1_list)
        Elbow_tau_list.append(tau2_list)
        
        Shl_Flex_power_list.append(power1_list)
        Elbow_power_list.append(power2_list)   


    # Calculation summary:
    max_Elbow_tau, max_Elbow_power, max_Elbow_Vel = 0, 0, 0
    max_Elbow_tau_index, max_Elbow_power_index, max_Elbow_Vel_index = 0, 0, 0

    for i in range(len(Elbow_tau_list)):
        if max_Elbow_Vel < max(Elbow_Vel_list[i]):
            max_Elbow_Vel = max(Elbow_Vel_list[i])
            max_Elbow_Vel_index = i
            
        if max_Elbow_tau < max(Elbow_tau_list[i]):
            max_Elbow_tau = max(Elbow_tau_list[i])
            max_Elbow_tau_index = i
            
        if max_Elbow_power < max(Elbow_power_list[i]):
            max_Elbow_power = max(Elbow_power_list[i])
            max_Elbow_power_index = i

    print(f"maximum elbow angular velocity is {format(max_Elbow_Vel, '.3f')} [rad/sec] ({format(max_Elbow_Vel*60/(2*pi), '.3f')} [rpm]), in trial {max_Elbow_Vel_index}")
    print(f"maximum elbow torque is {format(max_Elbow_tau, '.3f')} [Nm], in trial {max_Elbow_tau_index}")
    print(f"maximum elbow power is {format(max_Elbow_power, '.3f')} [W], in trial {max_Elbow_power_index}")

    # The torque equations for the maximum torque:
    solution_0_subs = solution_0_subs.subs([(m1, m_upper_arm_dict[participants_list[max_Elbow_tau_index]]), (m2, m_lower_arm), (R1, L_upper_arm_dict[participants_list[max_Elbow_tau_index]]), (R2, L_lower_arm), (R1_COM, L_upper_arm_COM_dict[participants_list[max_Elbow_tau_index]]), (R2_COM, L_lower_arm_COM), (g, 9.81)])
    solution_1_subs = solution_1_subs.subs([(m1, m_upper_arm_dict[participants_list[max_Elbow_tau_index]]), (m2, m_lower_arm), (R1, L_upper_arm_dict[participants_list[max_Elbow_tau_index]]), (R2, L_lower_arm), (R1_COM, L_upper_arm_COM_dict[participants_list[max_Elbow_tau_index]]), (R2_COM, L_lower_arm_COM), (g, 9.81)])

    print(Eq(T[0], solution_0_subs))
    print(Eq(T[1], solution_1_subs))


if __name__ == '__main__':
    main()
