import pandas as pd
import os

def read_watclaimcheck_dataset(root_path: str):

    '''
    Reads in the WatClaimCheck dataset from the filepath and returns a pandas dataframe of the train, valid, and test datasets

    Parameters:
    root_path (str): The absolute root_path directory of the dataset

    Returns:
    tuple: Train, Valid, Test Pandas Dataframes
    '''

    # Get the filepath for the jsons
    train_json = os.path.join(root_path, 'train.json')
    valid_json = os.path.join(root_path, 'valid.json')
    test_json = os.path.join(root_path, 'test.json')

    # Read json as pandas dataframe
    train_pd = pd.read_json(train_json)
    valid_pd = pd.read_json(valid_json)
    test_pd = pd.read_json(test_json)

    return train_pd, valid_pd, test_pd
