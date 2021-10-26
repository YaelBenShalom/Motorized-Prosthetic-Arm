# this script converts all the .XLS files in the Control Data folder into .csv

import os
import csv
import pandas as pd


def main():
    """ Converts all the .XLS files in the Control Data folder into .csv
    """

    data_dir = '../'
    data_participant_dir = data_dir + 'control_data'

    for folder in os.listdir(data_participant_dir):
        data_trial_dir = data_participant_dir + '/' + folder + '/kinematics'
        for file in os.listdir(data_trial_dir):
            if file.endswith(".XLS"):
                file_name = file.split(".")[0]
                file_path = os.path.join(data_trial_dir, file)
                new_file_path = os.path.join(
                    data_participant_dir, '/CSV Converted Files/', file_name, '.csv')
                read_file = pd.read_table(
                    file_path, delimiter=",", encoding='utf-8')
                read_file.to_csv(new_file_path, index=None, header=True)
        print("Finish converting txt files in folder {}".format(folder))
    print("Finish converting all txt files")


if __name__ == '__main__':
    main()
