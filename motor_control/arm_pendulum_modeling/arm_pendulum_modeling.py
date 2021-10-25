# Imports required for data processing
import os
import csv
import pandas as pd
import argparse

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


# Extracting angles data and computing angular velocities and angular accelerations from the angles:
def calculate_vel(Ang_list, time_list, index):
    return ((Ang_list[index + 1] - Ang_list[index])
        / (time_list[index + 1] - time_list[index]))


def calculate_acc(Vel_list, time_list, index):
    return ((Vel_list[index + 1] - Vel_list[index])
        / (time_list[index + 1] - time_list[index]))


def main(args):
    # Defining parameters
    use_my_data = args["my_data"]
    use_double_pendulum = args["double_pendulum"]

    #########################################################################################################
    ####################################  Define the system's constants  ####################################
    #########################################################################################################

    if use_my_data:
        # Masses, length and center-of-mass positions (calculated using the lab measurements)
        # Mass calculations (mass unit is kg) 
        m_body = 53
        m_u = 0.028 * m_body                    # Average upper arm weights relative to body weight, from “Biomechanics
                                                # and Motor Control of Human Movement” by David Winter (2009), 4th edition
        m_l = 0.7395                            # Average lower prosthetics weights, calculated using lab measurements  
        # m_lower = 0.022 * m_body              # Average lower arm weights relative to body weight, from “Biomechanics
                                                # and Motor Control of Human Movement” by David Winter (2009), 4th edition
        # Arm length calculations (length unit is m) 
        H_body = 1.62
        L_u = 0.186 * H_body                    # Average upper arm length relative to body height
                                                # from “Biomechanics and Motor Control of Human Movement” by David
                                                # Winter (2009), 4th edition
        # L_l = (0.146 + 0.108) * H_body        # Average lower arm length relative to body height
                                                # from “Biomechanics and Motor Control of Human Movement” by David
                                                # Winter (2009), 4th edition
        L_l = 0.42                              # Average lower prosthetics length, calculated using lab measurements 

        # Arm center of mass length calculations (length unit is m) 
        L_u_c = 0.436 * L_u                     # Average upper arm length from shoulder to center of mass relative
                                                # to upper arm length, from “Biomechanics and Motor Control of Human
                                                # Movement” by David Winter (2009), 4th edition
        L_l_c = 0.2388                          # Average lower prosthetics length from elbow to center of mass,
                                                # calculated using lab measurements 
        # L_l_c = 0.682 * L_l                   # Average lower arm length from shoulder to center of mass relative
                                                # to upper arm length, from “Biomechanics and Motor Control of Human
                                                # Movement” by David Winter (2009), 4th edition
    else:
        # Masses, length and center-of-mass positions (calculated using the lab measurements)
        # Mass calculations (mass unit is kg) 
        m_body = 90.6                           # Average weights for American adult male
                                                # from "Anthropometric Reference Data for Children and Adults:
                                                # United States, 2015–2018"
        m_body_dict = {'ID': 51.0, 'JD': 79.5, 'JR': 76.0, 'KS': 59.3, 'KW': 63.8, 'LC': 61.2,
                       'LD': 97.3, 'LS': 82.2, 'MK': 93.5, 'MV': 98.5, 'SM': 68.5, 'TD': 70.0,
                       'TM': 66.2}

        m_u = 0.028 * m_body                    # Average upper arm weights relative to body weight, from “Biomechanics
                                                # and Motor Control of Human Movement” by David Winter (2009), 4th edition
        m_u_dict = {'ID': 0.028 * m_body_dict['ID'], 'JD': 0.028 * m_body_dict['JD'],
                    'JR': 0.028 * m_body_dict['JR'], 'KS': 0.028 * m_body_dict['KS'],
                    'KW': 0.028 * m_body_dict['KW'], 'LC': 0.028 * m_body_dict['LC'],
                    'LD': 0.028 * m_body_dict['LD'], 'LS': 0.028 * m_body_dict['LS'],
                    'MK': 0.028 * m_body_dict['MK'], 'MV': 0.028 * m_body_dict['MV'],
                    'SM': 0.028 * m_body_dict['SM'], 'TD': 0.028 * m_body_dict['TD'],
                    'TM': 0.028 * m_body_dict['TM']}

        m_l = 0.7395                            # Average lower prosthetics weights, calculated using lab measurements  

        # Arm length calculations (length unit is m) 
        H_body = 1.769                          # Average height for American adult male, from “Height and body-mass 
                                                # index trajectories of school-aged children and adolescents from 
                                                # 1985 to 2019 in 200 countries and territories: a pooled analysis 
                                                # of 2181 population-based studies with 65 million participants”
        H_body_dict = {'ID': 1.620, 'JD': 1.760, 'JR': 1.770, 'KS': 1.640, 'KW': 1.620, 'LC': 1.580,
                       'LD': 1.875, 'LS': 1.635, 'MK': 1.780, 'MV': 1.805, 'SM': 1.790, 'TD': 1.690,
                       'TM': 1.735}

        L_u = 0.186 * H_body                    # Average upper arm length relative to body height
                                                # from “Biomechanics and Motor Control of Human Movement” by David
                                                # Winter (2009), 4th edition
        L_u_dict = {'ID': 0.186 * H_body_dict['ID'], 'JD': 0.186 * H_body_dict['JD'],
                    'JR': 0.186 * H_body_dict['JR'], 'KS': 0.186 * H_body_dict['KS'],
                    'KW': 0.186 * H_body_dict['KW'], 'LC': 0.186 * H_body_dict['LC'],
                    'LD': 0.186 * H_body_dict['LD'], 'LS': 0.186 * H_body_dict['LS'],
                    'MK': 0.186 * H_body_dict['MK'], 'MV': 0.186 * H_body_dict['MV'],
                    'SM': 0.186 * H_body_dict['SM'], 'TD': 0.186 * H_body_dict['TD'],
                    'TM': 0.186 * H_body_dict['TM']}

        L_l = 0.42                              # Average lower prosthetics length, calculated using lab measurements

        # Arm center of mass length calculations (length unit is m) 
        L_u_c = 0.436 * L_u                     # Average upper arm length from shoulder to center of mass relative
                                                # to upper arm length, from “Biomechanics and Motor Control of Human
                                                # Movement” by David Winter (2009), 4th edition
        L_u_c_dict = {'ID': 0.436 * L_u_dict['ID'], 'JD': 0.436 * L_u_dict['JD'],
                      'JR': 0.436 * L_u_dict['JR'], 'KS': 0.436 * L_u_dict['KS'],
                      'KW': 0.436 * L_u_dict['KW'], 'LC': 0.436 * L_u_dict['LC'],
                      'LD': 0.436 * L_u_dict['LD'], 'LS': 0.436 * L_u_dict['LS'],
                      'MK': 0.436 * L_u_dict['MK'], 'MV': 0.436 * L_u_dict['MV'],
                      'SM': 0.436 * L_u_dict['SM'], 'TD': 0.436 * L_u_dict['TD'],
                      'TM': 0.436 * L_u_dict['TM']}
        L_l_c = 0.2388                          # Average lower prosthetics length from elbow to center of mass,
                                                # calculated using lab measurements 


    #########################################################################################################
    ###########################################  Extracting Data  ###########################################
    #########################################################################################################

    data_csv_dir = '../../data/control_data/CSV Converted Files'
    print("current directory: ", os.getcwd())

    if use_my_data:
        frame_frequency = 100

        walking_vel_list = []
        time_list = []
        elbow_ang_list, shoulder_ang_list, tot_ang_list = [], [], []
        elbow_vel_list, shoulder_vel_list = [], []
        elbow_acc_list, shoulder_acc_list = [], []
        elbow_acc_data_list, shoulder_acc_data_list = [], []
        back_ang_list, back_pos_list, back_vel_list = [], [], []

        folder_list = os.listdir(data_csv_dir)
        folder_list.sort()

        for folder in folder_list:

            data_trial_dir = os.path.join(data_csv_dir, folder)
            if os.path.isdir(data_trial_dir):
                file_list = os.listdir(data_trial_dir)

                for file in file_list:
                    if "00B429F8" in file:
                        if file.endswith(".csv"):
                            file_name = file[:-4]
                            walking_vel = file.split("_")[4][:5]

                            frame = 0
                            file_time_list = []
                            file_shoulder_ang_list, file_shoulder_vel_list, file_shoulder_acc_list, file_shoulder_acc_data_list = [], [], [], []

                            # Cutting out weird data behavior on data edges
                            data_path = os.path.join(data_csv_dir, folder, file)
                            data_rows = open(data_path).read().strip().split("\n")[6000:7500]

                            # Extract time [sec], elbow angles [rad], and shoulder angles [rad] from data
                            for row in data_rows:
                                splitted_row = row.strip().split("\t")

                                # Check if loop finished all data
                                if not len(splitted_row):
                                    break

                                file_time_list.append(frame / frame_frequency)
                                file_shoulder_ang_list.append(float(splitted_row[31]) * 2*pi/360)
                                file_shoulder_acc_data_list.append(float(splitted_row[14]))
                                frame += 1

                            # Extract elbow and shoulder velocities [rad/sec] from angles
                            for i in range(len(file_time_list) - 1):
                                shoulder_vel = calculate_vel(file_shoulder_ang_list, file_time_list, i)
                                file_shoulder_vel_list.append(shoulder_vel)

                            # Extract elbow and shoulder Accelerations [rad/sec^2] from velocities
                            for i in range(len(file_time_list) - 2):
                                shoulder_acc = calculate_acc(file_shoulder_vel_list, file_time_list, i)
                                file_shoulder_acc_list.append(shoulder_acc)

                            # Adjust lists length
                            adjusted_file_time_list = file_time_list[:-2]
                            adjusted_file_shoulder_ang_list = file_shoulder_ang_list[:-2]
                            adjusted_file_shoulder_vel_list = file_shoulder_vel_list[:-1]
                            adjusted_file_shoulder_acc_data_list = file_shoulder_acc_data_list[:-2]

                            time_list.append(adjusted_file_time_list)
                            walking_vel_list.append(walking_vel)

                            shoulder_ang_list.append(adjusted_file_shoulder_ang_list)
                            shoulder_vel_list.append(adjusted_file_shoulder_vel_list)
                            shoulder_acc_list.append(file_shoulder_acc_list)
                            shoulder_acc_data_list.append(adjusted_file_shoulder_acc_data_list)
                            break

                for file in file_list:
                    if "00B429E2" in file:
                        if file.endswith(".csv"):
                            file_name = file[:-4]
                            walking_vel = file.split("_")[4][:5]

                            frame = 0
                            file_time_list = []
                            file_elbow_ang_list, file_tot_ang_list, file_elbow_vel_list, file_elbow_acc_list, file_elbow_acc_data_list = [], [], [], [], []

                            # Cutting out weird data behavior on data edges
                            data_path = os.path.join(data_csv_dir, folder, file)
                            data_rows = open(data_path).read().strip().split("\n")[6000:7500]

                            # Extract time [sec], elbow angles [rad], and shoulder angles [rad] from data
                            for i in range(len(data_rows)):
                                splitted_row = data_rows[i].strip().split("\t")

                                # Check if loop finished all data
                                if not len(splitted_row):
                                    break

                                file_time_list.append(frame / frame_frequency)
                                file_tot_ang_list.append(float(splitted_row[31]) * 2*pi/360)
                                file_elbow_ang_list.append((float(splitted_row[31]) - file_shoulder_ang_list[i]) * 2*pi/360)
                                file_elbow_acc_data_list.append(float(splitted_row[14]))
                                frame += 1

                            # Extract elbow and shoulder velocities [rad/sec] from angles
                            for i in range(len(file_time_list) - 1):
                                elbow_vel = calculate_vel(file_elbow_ang_list, file_time_list, i)
                                file_elbow_vel_list.append(elbow_vel)

                            # Extract elbow and shoulder Accelerations [rad/sec^2] from velocities
                            for i in range(len(file_time_list) - 2):
                                elbow_acc = calculate_acc(file_elbow_vel_list, file_time_list, i)
                                file_elbow_acc_list.append(elbow_acc)

                            # Adjust lists length
                            adjusted_file_tot_ang_list = file_tot_ang_list[:-2]
                            adjusted_file_elbow_ang_list = file_elbow_ang_list[:-2]
                            adjusted_file_elbow_vel_list = file_elbow_vel_list[:-1]
                            adjusted_file_elbow_acc_data_list = file_elbow_acc_data_list[:-2]

                            tot_ang_list.append(adjusted_file_tot_ang_list)
                            elbow_ang_list.append(adjusted_file_elbow_ang_list)
                            elbow_vel_list.append(adjusted_file_elbow_vel_list)
                            elbow_acc_list.append(file_elbow_acc_list)
                            elbow_acc_data_list.append(file_elbow_acc_data_list)
                            break

                for file in file_list:
                    if "00B43D0C" in file:
                        if file.endswith(".csv"):
                            file_name = file[:-4]
                            walking_vel = file.split("_")[4][:5]
                            if walking_vel == "1.4ms":
                                continue

                            frame = 0
                            file_time_list = []
                            file_back_ang_list, file_back_pos_list, file_back_vel_list = [], [], []

                            # Cutting out weird data behavior on data edges
                            data_path = os.path.join(data_csv_dir, folder, file)
                            data_rows = open(data_path).read().strip().split("\n")[6000:7500]

                            # Extract time [sec], elbow angles [rad], and shoulder angles [rad] from data
                            for i in range(len(data_rows)):
                                splitted_row = data_rows[i].strip().split("\t")

                                # Check if loop finished all data
                                if not len(splitted_row):
                                    break

                                file_time_list.append(frame / frame_frequency)

                                file_back_ang_list.append(float(splitted_row[31]) * 2*pi/360)
                                file_back_pos_list.append(float(splitted_row[21]))
                                file_back_vel_list.append(float(splitted_row[24]))
                                frame += 1

                            # Adjust lists length
                            adjusted_file_back_ang_list = file_back_ang_list[:-2]
                            adjusted_file_back_pos_list = file_back_pos_list[:-2]
                            adjusted_file_back_vel_list = file_back_vel_list[:-2]

                            back_ang_list.append(adjusted_file_back_ang_list)
                            back_pos_list.append(adjusted_file_back_pos_list)
                            back_vel_list.append(adjusted_file_back_vel_list)
                            break

    else:
        frame_frequency = 120

        participants_list = []
        time_list = []
        elbow_ang_list, shoulder_ang_list = [], []
        elbow_vel_list, shoulder_vel_list = [], []
        elbow_acc_list, shoulder_acc_list = [], []

        for file in os.listdir(data_csv_dir):
            file_name = file.split(".")[0]
            participant_name = file.split("_")[0]

            if file.endswith(".csv"):
                frame = 0
                file_time_list = []
                file_R_elbow_ang_list, file_R_shoulder_ang_list = [], []
                file_L_elbow_ang_list, file_L_shoulder_ang_list = [], []
                file_R_elbow_vel_list, file_R_shoulder_vel_list = [], []
                file_L_elbow_vel_list, file_L_shoulder_vel_list = [], []
                file_R_elbow_acc_list, file_R_shoulder_acc_list = [], []
                file_L_elbow_acc_list, file_L_shoulder_acc_list = [], []

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

                    file_time_list.append(frame / frame_frequency)
                    file_R_shoulder_ang_list.append(float(splitted_row[11]) * 2*pi/360)
                    file_R_elbow_ang_list.append(float(splitted_row[9]) * 2*pi/360)
                    file_L_shoulder_ang_list.append(float(splitted_row[23]) * 2*pi/360)
                    file_L_elbow_ang_list.append(float(splitted_row[21]) * 2*pi/360)
                    frame += 1

                # Extract elbow and shoulder velocities [rad/sec] from angles
                for i in range(len(file_time_list) - 1):
                    R_elbow_vel = calculate_vel(file_R_elbow_Ang_list, file_time_list, i)
                    R_shoulder_vel = calculate_vel(file_R_shoulder_ang_list, file_time_list, i)
                    L_elbow_vel = calculate_vel(file_L_elbow_ang_list, file_time_list, i)
                    L_shoulder_vel = calculate_vel(file_L_shoulder_ang_list, file_time_list, i)

                    file_R_elbow_vel_list.append(R_elbow_vel)
                    file_R_shoulder_vel_list.append(R_shoulder_vel)
                    file_L_elbow_vel_list.append(L_elbow_vel)
                    file_L_shoulder_vel_list.append(L_shoulder_vel)

                # Extract elbow and shoulder Accelerations [rad/sec^2] from velocities
                for i in range(len(file_time_list) - 2):
                    R_elbow_acc = calculate_acc(file_R_elbow_vel_list, file_time_list, i)
                    R_shoulder_acc = calculate_acc(file_R_shoulder_vel_list, file_time_list, i)
                    L_elbow_acc = calculate_acc(file_L_elbow_vel_list, file_time_list, i)
                    L_shoulder_acc = calculate_acc(file_L_shoulder_vel_list, file_time_list, i)

                    file_R_elbow_acc_list.append(R_elbow_acc)
                    file_R_shoulder_acc_list.append(R_shoulder_acc)
                    file_L_elbow_acc_list.append(L_elbow_acc)
                    file_L_shoulder_acc_list.append(L_shoulder_acc)

                # Adjust lists length
                file_time_list = file_time_list[:-2]
                file_R_elbow_ang_list = file_R_elbow_ang_list[:-2]
                file_R_shoulder_ang_list = file_R_shoulder_ang_list[:-2]
                file_L_elbow_ang_list = file_L_elbow_ang_list[:-2]
                file_L_shoulder_ang_list = file_L_shoulder_ang_list[:-2]

                file_R_elbow_vel_list = file_R_elbow_vel_list[:-1]
                file_R_shoulder_vel_list = file_R_shoulder_vel_list[:-1]
                file_L_elbow_vel_list = file_L_elbow_vel_list[:-1]
                file_L_shoulder_vel_list = file_L_shoulder_vel_list[:-1]

                participants_list.append(participant_name)
                participants_list.append(participant_name)

                time_list.append(file_time_list)
                time_list.append(file_time_list)

                elbow_ang_list.append(file_R_elbow_ang_list)
                shoulder_ang_list.append(file_R_shoulder_ang_list)        
                elbow_ang_list.append(file_L_elbow_ang_list)
                shoulder_ang_list.append(file_L_shoulder_ang_list)
                elbow_vel_list.append(file_R_elbow_vel_list)
                shoulder_vel_list.append(file_R_shoulder_vel_list)        
                elbow_vel_list.append(file_L_elbow_vel_list)
                shoulder_vel_list.append(file_L_shoulder_vel_list)
                elbow_acc_list.append(file_R_elbow_acc_list)
                shoulder_acc_list.append(file_R_shoulder_acc_list)        
                elbow_acc_list.append(file_L_elbow_acc_list)
                shoulder_acc_list.append(file_L_shoulder_acc_list)


    #########################################################################################################
    ###########################################  System Modeling  ###########################################
    #########################################################################################################

    if not use_double_pendulum:
        # Computing the Lagrangian of the system
        m, g, R, R_c = symbols(r'm, g, R, R_c')

        # The system torque variables as function of t
        tau = Function(r'tau')(t)

        # The system configuration variables as function of t
        theta = Function(r'theta')(t)

        # The velocity as derivative of position wrt t
        theta_dot = theta.diff(t)

        # The acceleration as derivative of velocity wrt t
        theta_ddot = theta_dot.diff(t)

        # Converting the polar coordinates to cartesian coordinates
        x = R_c * sin(theta)
        y = -R_c * cos(theta)

        # Calculating the kinetic and potential energy of the system
        KE = 1/2 * m * ((x.diff(t))**2 + (y.diff(t))**2)
        PE = m * g * y

        # Computing the Lagrangian
        L = simplify(KE - PE)
        print('L: {} \n'.format(L))


        # Computing the Euler-Lagrange equations:
        # Define the derivative of L wrt the functions: x, xdot
        L_dtheta = L.diff(theta)
        L_dtheta_dot = L.diff(theta_dot)

        # Define the derivative of L_dxdot wrt to time t
        L_dtheta_dot_dt = L_dtheta_dot.diff(t)

        # Define the right hand side of the the Euler-Lagrange as a matrix
        rhs = simplify(L_dtheta_dot_dt - L_dtheta)

        # Define the left hand side of the the Euler-Lagrange as a Matrix
        lhs = tau

        # Compute the Euler-Lagrange equations as a matrix
        EL_eqns = Eq(lhs, rhs)

        print('Euler-Lagrange matrix for this systems: {} \n'.format(EL_eqns))

        # Simulating the system:
        # Substitute the derivative variables with a dummy variables and plug-in the constants
        solution_subs = rhs

        theta_dot_dummy = symbols('thetadot')
        theta_ddot_dummy = symbols('thetaddot')

        solution_subs = solution_subs.subs([(g, 9.81)])

        solution_subs = solution_subs.subs([((theta.diff(t)).diff(t), theta_ddot_dummy)])
        solution_subs = solution_subs.subs([(theta.diff(t), theta_dot_dummy)])

        # Lambdify the thetas and its derivatives
        func = lambdify([theta, theta_dot_dummy, theta_ddot_dummy,
                        m, R, R_c], solution_subs, modules = sympy)

        # Initialize the torque and power lists
        elbow_tau_list = []
        elbow_current_list = []
        elbow_power_list = []

        motor_kv = 115
        torque_const = 8.27 / motor_kv

        for i in range(len(time_list)):
            # Initialize the torque and power lists
            tau_list = []
            current_list = []
            power_list = []

            t_list = time_list[i]
            theta_list = elbow_ang_list[i]
            dtheta_list = elbow_vel_list[i]
            ddtheta_list = elbow_acc_list[i]

            # Plug-in the angles, angular velocities and angular accelerations for every time step to find the torques
            for j in range(len(t_list)):
                tau_list.append(func(theta_list[j], dtheta_list[j], ddtheta_list[j], m_l, L_l, L_l_c))

                # Calculate the current required to reach the required joints torques for every time step
                current_list.append(torque_const * tau_list[j])

                # Calculate the power required to reach the required angular velocities and joints torques for every time step
                power_list.append(dtheta_list[j] * tau_list[j])

            elbow_tau_list.append(tau_list)
            elbow_current_list.append(current_list)
            elbow_power_list.append(power_list)

            print(f"{walking_vel_list[i]}:\t max angle: {format(max(theta_list), '.3f')}[rad]\t max velocity: {format(max(dtheta_list), '.3f')}[rad/s]\t max torque: {format(max(tau_list), '.3f')}[Nm]\t max power: {format(max(power_list), '.3f')}[W]")

        # Calculation summary
        max_elbow_tau, max_elbow_power, max_elbow_vel, max_elbow_ang = -10, -10, -10, -10
        max_elbow_tau_index, max_elbow_power_index, max_elbow_vel_index, max_elbow_ang_index = 0, 0, 0, 0

        for i in range(len(elbow_tau_list)):
            if max_elbow_ang < max(elbow_ang_list[i]):
                max_elbow_ang = max(elbow_ang_list[i])
                max_elbow_ang_index = i
                
            if max_elbow_vel < max(elbow_vel_list[i]):
                max_elbow_vel = max(elbow_vel_list[i])
                max_elbow_vel_index = i

            if max_elbow_tau < max(elbow_tau_list[i]):
                max_elbow_tau = max(elbow_tau_list[i])
                max_elbow_tau_index = i

            if max_elbow_power < max(elbow_power_list[i]):
                max_elbow_power = max(elbow_power_list[i])
                max_elbow_power_index = i

        print(f"maximum elbow angle is {format(max_elbow_ang, '.3f')} [rad], in velocity {walking_vel_list[max_elbow_ang_index]} (trial {max_elbow_ang_index})")
        print(f"maximum elbow angular velocity is {format(max_elbow_vel, '.3f')} [rad/s] ({format(max_elbow_vel*60/(2*pi), '.3f')} [rpm]), in velocity {walking_vel_list[max_elbow_vel_index]} (trial {max_elbow_vel_index})")
        print(f"maximum elbow torque is {format(max_elbow_tau, '.3f')} [Nm], in velocity {walking_vel_list[max_elbow_tau_index]} (trial {max_elbow_tau_index})")
        print(f"maximum elbow power is {format(max_elbow_power, '.3f')} [W], in velocity {walking_vel_list[max_elbow_power_index]} (trial {max_elbow_power_index})")


        # The torque equations for the maximum power:
        solution_subs = solution_subs.subs([(m, m_l), (R, L_l), (R_c, L_l_c), (g, 9.81)])

        print("\nThe torque equations for the maximum torque:")
        print(Eq(tau, solution_subs))

        # print(Elbow_Ang_list[max_Elbow_tau_index])
        # print(Elbow_Vel_list[max_Elbow_tau_index])
        # print(Elbow_Acc_list[max_Elbow_tau_index])
        # print(Elbow_tau_list[max_Elbow_tau_index])
        # print(Elbow_Ang_list[2])
        # print(Elbow_tau_list[2])


    if use_double_pendulum:
        # Computing the Lagrangian of the system
        m1, m2, g, R1, R1_c, R2, R2_c = symbols(r'm1, m2, g, R1, R1_c, R2, R2_c')

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
        x1 = R1_c * sin(theta1)
        x2 = R1 * sin(theta1) + R2_c * sin(theta1 + theta2)

        y1 = -R1_c * cos(theta1)
        y2 = -R1 * cos(theta1) - R2_c * cos(theta1 + theta2)

        # Calculating the kinetic and potential energy of the system
        KE = 1/2 * m1 * ((x1.diff(t))**2 + (y1.diff(t))**2) + 1/2 * m2 * ((x2.diff(t))**2 + (y2.diff(t))**2)
        PE = m1 * g * y1 + m2 * g * y2

        # Computing the Lagrangian
        L = simplify(KE - PE)
        print('L: {} \n'.format(L))


        # Computing the Euler-Lagrange equations
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
                    simplify(L_dtheta2_dot_dt - L_dtheta2)])

        # Define the right hand side of the the Euler-Lagrange as a Matrix
        rhs = Matrix([tau1, tau2])

        # Compute the Euler-Lagrange equations as a matrix
        EL_eqns = Eq(lhs, rhs)

        print('Euler-Lagrange matrix for this systems:')
        print(EL_eqns)

        # Solve the equations for 𝜏1 and 𝜏2
        # Solve the Euler-Lagrange equations for the shoulder and elbow torques
        T = Matrix([tau1, tau2])
        soln = solve(EL_eqns, T, dict=True)

        # Initialize the solutions
        solution = [0, 0]
        i = 0

        for sol in soln:
            for v in T:
                solution[i] = simplify(sol[v])
                display(Eq(T[i], solution[i]))
                i =+ 1

        # Simulating the system
        # Substitute the derivative variables with a dummy variables and plug-in the constants
        solution_0_subs = solution[0]
        solution_1_subs = solution[1]

        theta1_dot_dummy = symbols('thetadot1')
        theta2_dot_dummy = symbols('thetadot2')
        theta1_ddot_dummy = symbols('thetaddot1')
        theta2_ddot_dummy = symbols('thetaddot2')

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

        # Lambdify the thetas and its derivatives
        func1 = lambdify([theta1, theta2, theta1_dot_dummy, theta2_dot_dummy, theta1_ddot_dummy,
                        theta2_ddot_dummy, m1, m2, R1, R2, R1_c, R2_c], solution_0_subs, modules = sympy)
        func2 = lambdify([theta1, theta2, theta1_dot_dummy, theta2_dot_dummy, theta1_ddot_dummy,
                        theta2_ddot_dummy, m1, m2, R1, R2, R1_c, R2_c], solution_1_subs, modules = sympy)

        # Initialize the torque and power lists
        shoulder_tau_list, elbow_tau_list = [], []
        shoulder_current_list, elbow_current_list = [], []
        shoulder_power_list, elbow_power_list = [], []
        freq_list = []
        
        motor_kv = 115
        torque_const = 8.27 / motor_kv

        for i in range(len(time_list)):
            # Initialize the torque and power lists
            tau1_list, tau2_list = [], []
            current1_list, current2_list = [], []
            power1_list, power2_list = [], []

            t_list = time_list[i]
            theta1_list = shoulder_ang_list[i]
            theta2_list = elbow_ang_list[i]
            dtheta1_list = shoulder_vel_list[i]
            dtheta2_list = elbow_vel_list[i]
            ddtheta1_list = shoulder_acc_list[i]
            ddtheta2_list = elbow_acc_list[i]

            count = 0
            vel_freq_list = []
            # Plug-in the angles, angular velocities and angular accelerations for every time step to find the torques
            for j in range(len(t_list)):
                if use_my_data:
                    if (count < 2) and (theta1_list[j] * theta1_list[j + 1] < 0) and (theta1_list[j] > 0):
                        vel_freq_list.append(j)
                        count += 1
                        
                    tau1_list.append(func1(theta1_list[j], theta2_list[j],
                                        dtheta1_list[j], dtheta2_list[j],
                                        ddtheta1_list[j], ddtheta2_list[j],
                                        m_u, m_l, L_u, L_l, L_u_c, L_l_c))

                    tau2_list.append(func2(theta1_list[j], theta2_list[j],
                                        dtheta1_list[j], dtheta2_list[j],
                                        ddtheta1_list[j], ddtheta2_list[j],
                                        m_u, m_l, L_u, L_l, L_u_c, L_l_c))
                
                else:
                    tau1_list.append(func1(theta1_list[j], theta2_list[j], dtheta1_list[j], dtheta2_list[j],
                                        ddtheta1_list[j], ddtheta2_list[j], m_u_dict[participants_list[i]],
                                        m_l, L_u_dict[participants_list[i]], L_l,
                                        L_u_c_dict[participants_list[i]], L_l_c))

                    tau2_list.append(func2(theta1_list[j], theta2_list[j], dtheta1_list[j], dtheta2_list[j],
                                        ddtheta1_list[j], ddtheta2_list[j], m_u_dict[participants_list[i]],
                                        m_l, L_u_dict[participants_list[i]], L_l,
                                        L_u_c_dict[participants_list[i]], L_l_c))

                # Calculate the current required to reach the required joints torques for every time step
                current1_list.append(torque_const * tau1_list[j])
                current2_list.append(torque_const * tau2_list[j])

                # Calculate the power required to reach the required angular velocities and joints torques for every time step
                power1_list.append(dtheta1_list[j] * tau1_list[j])
                power2_list.append(dtheta2_list[j] * tau2_list[j])

            shoulder_tau_list.append(tau1_list)
            elbow_tau_list.append(tau2_list)
            shoulder_current_list.append(current1_list)
            elbow_current_list.append(current2_list)
            shoulder_power_list.append(power1_list)
            elbow_power_list.append(power2_list)
            
            freq_list.append(1 / ((vel_freq_list[1] - vel_freq_list[0]) / frame_frequency))

            print(f"{walking_vel_list[i]}:\t max angle: {format(max(theta2_list), '.3f')}[rad]\t max velocity: {format(max(dtheta2_list), '.3f')}[rad/s]\t max torque: {format(max(tau2_list), '.3f')}[Nm]\t max power: {format(max(power2_list), '.3f')}[W]")

        # Calculation summary
        max_elbow_ang_list, max_tot_ang_list = [], []
        max_elbow_tau, max_elbow_power, max_elbow_vel, max_elbow_ang = -10, -10, -10, -10
        max_elbow_tau_index, max_elbow_power_index, max_elbow_vel_index, max_elbow_ang_index = 0, 0, 0, 0

        for i in range(len(elbow_tau_list)):
            max_elbow_ang_list.append(max(elbow_ang_list[i]))
            max_tot_ang_list.append(max(tot_ang_list[i]))

            if max_elbow_ang < max(elbow_ang_list[i]):
                max_elbow_ang = max(elbow_ang_list[i])
                max_elbow_ang_index = i
                
            if max_elbow_ang < max(elbow_ang_list[i]):
                max_elbow_ang = max(elbow_ang_list[i])
                max_elbow_ang_index = i
                
            if max_elbow_vel < max(elbow_vel_list[i]):
                max_elbow_vel = max(elbow_vel_list[i])
                max_elbow_vel_index = i

            if max_elbow_tau < max(elbow_tau_list[i]):
                max_elbow_tau = max(elbow_tau_list[i])
                max_elbow_tau_index = i

            if max_elbow_power < max(elbow_power_list[i]):
                max_elbow_power = max(elbow_power_list[i])
                max_elbow_power_index = i

        print(f"maximum elbow angle is {format(max_elbow_ang, '.3f')} [rad], in velocity {walking_vel_list[max_elbow_ang_index]} (trial {max_elbow_ang_index})")
        print(f"maximum elbow angular velocity is {format(max_elbow_vel, '.3f')} [rad/s] ({format(max_elbow_vel*60/(2*pi), '.3f')} [rpm]), in velocity {walking_vel_list[max_elbow_vel_index]} (trial {max_elbow_vel_index})")
        print(f"maximum elbow torque is {format(max_elbow_tau, '.3f')} [Nm], in velocity {walking_vel_list[max_elbow_tau_index]} (trial {max_elbow_tau_index})")
        print(f"maximum elbow power is {format(max_elbow_power, '.3f')} [W], in velocity {walking_vel_list[max_elbow_power_index]} (trial {max_elbow_power_index})")

        if use_my_data:
            # The torque equations for the maximum power:
            solution_0_subs = solution_0_subs.subs([(m1, m_u), (m2, m_l), (R1, L_u), (R2, L_l),
                                                    (R1_c, L_u_c), (R2_c, L_l_c), (g, 9.81)])
            solution_1_subs = solution_1_subs.subs([(m1, m_u), (m2, m_l), (R1, L_u), (R2, L_l),
                                                    (R1_c, L_u_c), (R2_c, L_l_c), (g, 9.81)])
        
        else:
            # The torque equations for the maximum power:
            solution_0_subs = solution_0_subs.subs([(m1, m_u_dict[participants_list[max_elbow_tau_index]]),
                                                    (m2, m_l), (R1, L_u_dict[participants_list[max_elbow_tau_index]]),
                                                    (R2, L_l), (R1_c, L_u_c_dict[participants_list[max_elbow_tau_index]]),
                                                    (R2_c, L_l_c), (g, 9.81)])
            solution_1_subs = solution_1_subs.subs([(m1, m_u_dict[participants_list[max_elbow_tau_index]]),
                                                    (m2, m_l), (R1, L_u_dict[participants_list[max_elbow_tau_index]]),
                                                    (R2, L_l), (R1_c, L_u_c_dict[participants_list[max_elbow_tau_index]]),
                                                    (R2_c, L_l_c), (g, 9.81)])

        print("\nThe torque equations for the maximum torque:")
        display(Eq(T[0], solution_0_subs))
        display(Eq(T[1], solution_1_subs))

        # display(Elbow_Ang_list[max_Elbow_tau_index])
        # display(Elbow_Vel_list[max_Elbow_tau_index])
        # display(Elbow_Acc_list[max_Elbow_tau_index])
        # display(Elbow_tau_list[max_Elbow_tau_index])
        # display(Elbow_Ang_list[2])
        # display(Elbow_tau_list[2])


if __name__ == '__main__':
    # construct the argument parse and parse the arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("--double_pendulum", default=False, help="use double pendulum")
    parser.add_argument("--my_data", default=True, help="use my data")
    args = vars(parser.parse_args())
    main(args)
