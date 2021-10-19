# this script converts all the .XLS files in the hand_back_motion_data folder into .csv

import os
import csv
import pandas as pd


def main():
    """ Converts all the .txt files in the hand_back_motion_data folder into .csv
    """

    data_dir = '../'
    data_participant_dir = os.path.join(data_dir, 'hand_back_motion_data')
    for folder in os.listdir(data_participant_dir):
        data_trial_dir = os.path.join(data_participant_dir, folder)
        for file in os.listdir(data_trial_dir):
            if file.endswith(".txt"):
                file_name = file.split(".")[0]
                file_path = os.path.join(data_trial_dir, file)
                new_file_path = os.path.join(data_participant_dir, '/CSV Converted Files/', file_name, '_', folder, '.csv')
                read_file = pd.read_table(file_path, delimiter=",", encoding='utf-8')
                read_file.to_csv(new_file_path, index = None, header=True)
        print("Finish converting txt files in folder {}".format(folder))
    print("Finish converting all txt files")


if __name__ == '__main__':
    main()
