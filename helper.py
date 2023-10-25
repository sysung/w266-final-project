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
    train_pd_df = get_pd_from_json(train_json_fp)
    valid_pd_df = get_pd_from_json(valid_json_fp)
    test_pd_df = get_pd_from_json(test_json_fp)

    return train_pd_df, valid_pd_df, test_pd_df

def download_prequential_dataset(dataset_fp: str, num_months: int = 6) -> list[pd.DataFrame]:
    '''
    Reads the WatClaimCheckdataset from the fileapth and returns a prequential pandas dataframe where each split is `num_months` months long by `review_date`

    Parameters:
    dataset_fp (str): Filepath of datset
    num_months (int): Number of months per partition

    Returns:
    List[pd.DataFrames]: List of prequetial dataframes
    '''
    # Concatenate all train, valid, and test dataframes
    full_pd_df = pd.concat(download_dataset(dataset_fp)).reset_index(drop=True)

    # Get all of the data corresponding to the metadata and labels
    clean_full_pd_df = clean_pd_df(full_pd_df)

    return [clean_full_pd_df]

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