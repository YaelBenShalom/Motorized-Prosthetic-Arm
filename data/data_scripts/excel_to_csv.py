# this script converts all the .XLS files in the Control Data folder
# into .csv

import os
import csv
import pandas as pd


data_dir = '../'
data_participant_dir = data_dir + '/control_data'

for folder in os.listdir(data_participant_dir):
    data_trial_dir = data_participant_dir + '/' + folder + '/kinematics'
    for file in os.listdir(data_trial_dir):
        if file.endswith(".XLS"):
            file_name = file.split(".")[0]
            file_path = data_trial_dir + '/' + file
            read_file = pd.read_table(file_path, delimiter=",", encoding='utf-8')
            read_file.to_csv(data_participant_dir + '/CSV Converted Files/'
                             + file_name + ".csv", index = None, header=True)
