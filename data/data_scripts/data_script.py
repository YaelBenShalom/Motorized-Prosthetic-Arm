import os
import csv
import pandas as pd
from math import pi


def calculate_Vel(Ang_list, time_list, index):
    return ((Ang_list[index+1] - Ang_list[index])
          / (time_list[index+1] - time_list[index]))


def calculate_Acc(Vel_list, time_list, index):
    return ((Vel_list[index+1] - Vel_list[index])
          / (time_list[index+1] - time_list[index]))


data_csv_dir = '../control_data/CSV Converted Files'
frame_frequency = 120
print("current directory: ", os.getcwd())

headers_list = []
time_list = []
R_Elbow_Ang_list = []
R_Shl_Flex_Ang_list = []
L_Elbow_Ang_list = []
L_Shl_Flex_Ang_list = []
R_Elbow_Vel_list = []
R_Shl_Flex_Vel_list = []
L_Elbow_Vel_list = []
L_Shl_Flex_Vel_list = []
R_Elbow_Acc_list = []
R_Shl_Flex_Acc_list = []
L_Elbow_Acc_list = []
L_Shl_Flex_Acc_list = []

for file in os.listdir(data_csv_dir):
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
        data_rows = open(data_path).read().strip().split("\n")[24:]
        
        data_headers = open(data_path).read().strip().split("\n")[23]
        splitted_headers = data_headers.strip().split("\t")
        headers_list.append([file, splitted_headers[9], splitted_headers[11], splitted_headers[21], splitted_headers[23]])
        
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

        time_list.append(file_time_list)
        R_Elbow_Ang_list.append(file_R_Elbow_Ang_list)
        R_Shl_Flex_Ang_list.append(file_R_Shl_Flex_Ang_list)        
        L_Elbow_Ang_list.append(file_L_Elbow_Ang_list)
        L_Shl_Flex_Ang_list.append(file_L_Shl_Flex_Ang_list)
        R_Elbow_Vel_list.append(file_R_Elbow_Vel_list)
        R_Shl_Flex_Vel_list.append(file_R_Shl_Flex_Vel_list)        
        L_Elbow_Vel_list.append(file_L_Elbow_Vel_list)
        L_Shl_Flex_Vel_list.append(file_L_Shl_Flex_Vel_list)
        R_Elbow_Acc_list.append(file_R_Elbow_Acc_list)
        R_Shl_Flex_Acc_list.append(file_R_Shl_Flex_Acc_list)        
        L_Elbow_Acc_list.append(file_L_Elbow_Acc_list)
        L_Shl_Flex_Acc_list.append(file_L_Shl_Flex_Acc_list)

print(headers_list[62])
