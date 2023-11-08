from datetime import datetime

import pandas as pd
import os
import json

def download_dataset(dataset_fp: str) -> tuple:
    '''
    Reads the WatClaimCheck dataset from the filepath and returns a pandas dataframe of the train, valid, and test datasets
    Reads the WatClaimCheck dataset from the filepath and returns a pandas dataframe of the train, valid, and test datasets

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
    train_pd_df = pd.read_json(train_json_fp)
    valid_pd_df = pd.read_json(valid_json_fp)
    test_pd_df = pd.read_json(test_json_fp)

    # Get all of the data corresponding to the metadata and labels
    clean_train_pd_df = clean_pd_df(train_pd_df)
    clean_valid_pd_df = clean_pd_df(valid_pd_df)
    clean_test_pd_df = clean_pd_df(test_pd_df)

    return clean_train_pd_df, clean_valid_pd_df, clean_test_pd_df

def filter_by_review_date(df: pd.DataFrame, start_date: datetime, end_date: datetime) -> pd.DataFrame:
    start_date_condition = df['review_date'] >= start_date
    end_date_condition = df['review_date'] < end_date
    return df[start_date_condition & end_date_condition].copy()

def download_prequential_dataset(dataset_fp: str, month_interval: int = 6, start_date: datetime = datetime(2010, 1, 1), end_date: datetime = datetime(2021, 7, 1)) -> tuple:
    '''
    Reads the WatClaimCheckdataset from the fileapth and returns a prequential pandas dataframe where each split is `month_interval` months long by `review_date`
    The dataset should be used similarly to time series cross validation.

    Parameters:
    dataset_fp     (str): Filepath of datset
    month_interval (int): Number of months per partition

    Returns:
    tuple: Tuple of lists of prequetial dataframes
    '''
    # TODO: Look into Window Generation https://www.tensorflow.org/tutorials/structured_data/time_series#data_windowing

    # Download dataset
    train_pd_df, valid_pd_df, test_pd_df = download_dataset(dataset_fp)

    print(f"Start date is {start_date.strftime('%Y-%m-%d')}. End date is {end_date.strftime('%Y-%m-%d')}")

    # Initialize partitions array
    train_partitions = []
    valid_partitions = []
    test_partitions = []

    # Iterate through 6-month intervals
    while start_date < end_date:
        offset_date = start_date + pd.DateOffset(months=month_interval)
        # print(f"Creating partition from {start_date.strftime('%Y-%m-%d')} to {offset_date.strftime('%Y-%m-%d')}")

        train_partition_df = filter_by_review_date(clean_train_pd_df, start_date, offset_date)
        valid_partition_df = filter_by_review_date(clean_valid_pd_df, start_date, offset_date)
        test_partition_df = filter_by_review_date(clean_test_pd_df, start_date, offset_date)

        train_partitions.append(train_partition_df)
        valid_partitions.append(valid_partition_df)
        test_partitions.append(test_partition_df)

        start_date = offset_date

    print(f"Created {len(train_partitions)} partitions")

    return train_partitions, valid_partitions, test_partitions

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

def explode_dictionary(pd_df: pd.DataFrame, field: str) -> pd.DataFrame:
    '''Explodes a dictionary within a column as multiple columns and then drops the parent field'''
    return pd.concat([pd_df.drop(field, axis=1), pd_df[field].apply(pd.Series)], axis=1)

def clean_pd_df(pd_df: pd.DataFrame) -> pd.DataFrame:
    '''Extracts field from dataframe, casts review_date to datetime and removes id'''

    print("Extracting fields from metadata")
    pd_df = explode_dictionary(pd_df, 'metadata')

    print("Extracting fields from label")
    pd_df = explode_dictionary(pd_df, 'label')
    
    # Set claim_date as review_date if review_date does not exist
    pd_df['review_date'].fillna(pd_df['claim_date'], inplace=True)

    # Convert review_date to date time
    pd_df['review_date'] = pd.to_datetime(pd_df['review_date'].str.split('T', expand=True)[0])

    # Drop ID
    pd_df = pd_df.drop(columns=['id'])

    return pd_df

if __name__ == "__main__":
    dataset_fp = "./WatClaimCheck_dataset"
    article_file = "1_3.json"

    full_pd_df = download_prequential_dataset(dataset_fp)