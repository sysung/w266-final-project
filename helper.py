import pandas as pd
import os
import json

def get_pd_from_json(json_file: str) -> pd.DataFrame:
    '''
    Converts JSON file into Pandas Dataframe

    Parameters:
    json_file (str): The json file in the directory

    Returns:
    pd.DataFrame: Pandas dataframe from json_file
    '''

    pd_df = pd.read_json(json_file)

    return pd_df

def download_dataset(dataset_fp: str) -> tuple:
    '''
    Reads in the WatClaimCheck dataset from the filepath and returns a pandas dataframe of the train, valid, and test datasets

    Parameters:
    dataset_fp (str): Filepath of dataset

    Returns:
    tuple: Train, Valid, Test Pandas Dataframes
    '''

    # Get full path of json files
    train_json_fp = os.path.join(dataset_fp, 'train.json')
    valid_json_fp = os.path.join(dataset_fp, 'valid.json')
    test_json_fp = os.path.join(dataset_fp, 'test.json')

    # Get pandas dataframe from json
    train_pd = get_pd_from_json(train_json_fp)
    valid_pd = get_pd_from_json(valid_json_fp)
    test_pd = get_pd_from_json(test_json_fp)

    return train_pd, valid_pd, test_pd

def download_article(dataset_fp: str, article_file: str) -> dict:
    '''
    Downloads an article from the WatClaimCheck Dataset

    Parameters:
    dataset_fp   (str): Filepath of dataset
    article_file (str): Filepath of article

    Returns:
    dict: Article JSON
    '''

    # Read articles as json
    full_article_fp = open(os.path.join(dataset_fp, 'articles', article_file))
    json_data = json.load(full_article_fp)
    full_article_fp.close()

    return json_data

if __name__ == "__main__":
    dataset_fp = "./WatClaimCheck_dataset"
    article_file = "1_3.json"

    train_pd, valid_pd, test_pd = download_dataset(dataset_fp)
    article = download_article(dataset_fp, article_file)
    print(article)