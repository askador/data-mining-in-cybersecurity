"""This module contains utility files for pandas tasks"""
import pandas as pd


def get_parquet_pandas(file_path: str, **kwargs) -> pd.DataFrame:
    """
    This function reads parquet file into dataframe returned
    :param file_path: str path/to/file.csv (CONSTANT FROM data.paths)
    :param kwargs: optional, provides additional params like 'index_column'
    :return: Pandas dataframe read object
    ---EXAMPLE OF USAGE---
    from data.paths.parquet_paths import BUSINESS
    df = get_parquet_pandas(BUSINESS, some_kwargs = None)
    """
    return pd.read_parquet(file_path, **kwargs)
