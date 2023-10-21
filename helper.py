import pandas as pd
import os
import sys

def get_pd_from_json(root_path:str, json_file: str):
    '''
    Converts JSON file into Pandas Dataframe

    Parameters:
    root_path (str): The relative root_path directory of the dataset
    json_file (str): The json file in the directory

    Returns:
    pandas: Pandas dataframe from json_file
    '''

    # Get the filepath for the jsons
    json_fp = os.path.join(root_path, json_file)

    # Read json as pandas dataframe
    pd_df = pd.read_json(json_fp)

    return pd_df

def read_watclaimcheck_dataset(root_path: str):
    '''
    Reads in the WatClaimCheck dataset from the filepath and returns a pandas dataframe of the train, valid, and test datasets

    Parameters:
    root_path (str): The relative root_path directory of the dataset

    Returns:
    tuple: Train, Valid, Test Pandas Dataframes
    '''

    train_pd = get_pd_from_json(root_path, 'train.json')
    valid_pd = get_pd_from_json(root_path, 'valid.json')
    test_pd = get_pd_from_json (root_path, 'test.json')

    return train_pd, valid_pd, test_pd

if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise Exception('Requires 2 arguments!\nUsage: python helper.py <absolute_dataset_fp>')

    dataset_fp = sys.argv[1]
    if not os.path.isdir(dataset_fp):
        raise Exception('Relative directory not found!\nUsage: python helper.py <absolute_dataset_fp>')

    train_pd, valid_pd, test_pd = read_watclaimcheck_dataset(dataset_fp)
    print(train_pd.info(verbose=True))
