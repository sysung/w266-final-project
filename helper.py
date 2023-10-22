import pandas as pd
import os
import sys
import json

from google.cloud import storage

def explode_dictionary(pd_df: pd.DataFrame, field: str) -> pd.DataFrame:
    '''
    Explodes a dictionary within a column as multiple columns

    Parameters:
    pd_df (pd.Dataframe): The pandas dataframe to extract column dictionary
    field (str): The column dictionary to explode

    Returns:
    pd.DataFrame: The new pandas dataframe with exploded column
    '''
    return pd.concat([pd_df.drop(field, axis=1), pd_df[field].apply(pd.Series)], axis=1)

def download_json_into_memory(bucket_name, blob_name):
    """Downloads a json into memory."""
    # The ID of your GCS bucket
    # bucket_name = "your-bucket-name"

    # The ID of your GCS object
    # blob_name = "storage-object-name"

    storage_client = storage.Client()

    bucket = storage_client.bucket(bucket_name)

    # Construct a client side representation of a blob.
    # Note `Bucket.blob` differs from `Bucket.get_blob` as it doesn't retrieve
    # any content from Google Cloud Storage. As we don't need additional data,
    # using `Bucket.blob` is preferred here.
    blob = bucket.blob(blob_name)
    contents = json.loads(blob.download_as_string())

    print(
        "Downloaded storage object {} from bucket {}.".format(
            blob_name, bucket_name
        )
    )

    return contents

def get_pd_from_json(json_file: str) -> pd.DataFrame:
    '''
    Converts JSON file into Pandas Dataframe

    Parameters:
    json_file (str): The json file in the directory

    Returns:
    pd.DataFrame: Pandas dataframe from json_file
    '''

    bucket_name = "watclaimcheck_dataset"

    # Downlaod JSON into memory
    json_in_memory = download_json_into_memory(bucket_name, json_file)

    # Transform JSON into Pandas dataframe
    pd_df = pd.DataFrame.from_dict(json_in_memory)

    # Expand dictionaries into individual columns
    # pd_df = explode_dictionary(pd_df, 'metadata')
    # pd_df = explode_dictionary(pd_df, 'premise_articles')
    # pd_df = explode_dictionary(pd_df, 'label')

    return pd_df

def download_dataset() -> tuple:
    '''
    Reads in the WatClaimCheck dataset from the filepath and returns a pandas dataframe of the train, valid, and test datasets

    Returns:
    tuple: Train, Valid, Test Pandas Dataframes
    '''

    train_pd = get_pd_from_json('train.json')
    valid_pd = get_pd_from_json('valid.json')
    test_pd = get_pd_from_json('test.json')

    return train_pd, valid_pd, test_pd

if __name__ == "__main__":
    train_pd, valid_pd, test_pd = download_dataset()
    