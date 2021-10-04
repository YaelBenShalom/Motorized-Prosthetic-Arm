import os
import csv
import pandas as pd


def load_dataset(data_file_name, data_dir):
    """
    This function loads the synthesized data provided in a csv file in the
    /data_dir directory.
    """

    data_path = os.path.join(data_dir, data_file_name)
    data_rows = open(data_path).read().strip().split("\n")[6:]

    return data_rows


data_dir = '../processed_data'
data_file_name = 'TD_Elbow_Ang_WN2.csv'

data_rows = load_dataset(data_file_name, data_dir)
df = pd.read_csv('../processed_data/TD_Elbow_Ang_WN2.csv')
print(df)

t_list = []
R_Elbow_Ang_list = []
R_Shl_Flex_Ang_list = []
L_Elbow_Ang_list = []
L_Shl_Flex_Ang_list = []
R_Elbow_Ang_Vel_list = []
R_Shl_Flex_Vel_list = []
L_Elbow_Ang_Vel_list = []
L_Shl_Flex_Vel_list = []
R_Elbow_Ang_Acc_list = []
R_Shl_Flex_Acc_list = []
L_Elbow_Ang_Acc_list = []
L_Shl_Flex_Acc_list = []

for row in data_rows[:-2]:
    frame, t, _, _, _, _, R_Elbow_Ang, R_Shl_Flex_Ang, L_Elbow_Ang, L_Shl_Flex_Ang, R_Elbow_Ang_Vel, R_Shl_Flex_Vel, L_Elbow_Ang_Vel, L_Shl_Flex_Vel, R_Elbow_Ang_Acc, R_Shl_Flex_Acc, L_Elbow_Ang_Acc, L_Shl_Flex_Acc = row.strip().split(",")
    # print(f"size: {len(data_rows)}, frame: {frame}")

    t_list.append(float(t))
    R_Elbow_Ang_list.append(float(R_Elbow_Ang))
    R_Shl_Flex_Ang_list.append(float(R_Shl_Flex_Ang))
    L_Elbow_Ang_list.append(float(L_Elbow_Ang))
    L_Shl_Flex_Ang_list.append(float(L_Shl_Flex_Ang))
    # if int(frame) > len(data_rows)-1:
    #     continue
    R_Elbow_Ang_Vel_list.append(float(R_Elbow_Ang_Vel))
    R_Shl_Flex_Vel_list.append(float(R_Shl_Flex_Vel))
    L_Elbow_Ang_Vel_list.append(float(L_Elbow_Ang_Vel))
    L_Shl_Flex_Vel_list.append(float(L_Shl_Flex_Vel))
    # if int(frame) > len(data_rows)-2:
    #     continue
    R_Elbow_Ang_Acc_list.append(float(R_Elbow_Ang_Acc))
    R_Shl_Flex_Acc_list.append(float(R_Shl_Flex_Acc))
    L_Elbow_Ang_Acc_list.append(float(L_Elbow_Ang_Acc))
    L_Shl_Flex_Acc_list.append(float(L_Shl_Flex_Acc))

# print("t_list: ", t_list)
# print("R_Shl_Flex_Ang_list: ", R_Shl_Flex_Ang_list)
# print("R_Elbow_Ang_list: ", R_Elbow_Ang_list)
# print("R_Shl_Flex_Vel_list: ", R_Shl_Flex_Vel_list)
# print("R_Elbow_Ang_Vel_list: ", R_Elbow_Ang_Vel_list)
# print("R_Shl_Flex_Acc_list: ", R_Shl_Flex_Acc_list)
# print("R_Elbow_Ang_Acc_list: ", R_Elbow_Ang_Acc_list)

print("t_list: ", t_list)
print("L_Shl_Flex_Ang_list: ", L_Shl_Flex_Ang_list)
print("L_Elbow_Ang_list: ", L_Elbow_Ang_list)
print("L_Shl_Flex_Vel_list: ", L_Shl_Flex_Vel_list)
print("L_Elbow_Ang_Vel_list: ", L_Elbow_Ang_Vel_list)
print("L_Shl_Flex_Acc_list: ", L_Shl_Flex_Acc_list)
print("L_Elbow_Ang_Acc_list: ", L_Elbow_Ang_Acc_list)

