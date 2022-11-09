import pandas as pd
from pathlib import Path
from .other import append_nested_columns


def expand_business_attributes(business_df: pd.DataFrame):
    business_df = append_nested_columns(business_df, 'attributes')
    business_df = business_df.drop('attributes', axis=1)
    return business_df


def prepare_business_df(business_df: pd.DataFrame):
    business_df = business_df.set_index('business_id')
    business_df = expand_business_attributes(business_df)
    return business_df


def save_business_df_json(business_df: pd.DataFrame):
    path = Path.cwd().joinpath('..', 'json-data', 'business.json').resolve()
    business_df.to_json(path_or_buf=path, orient="records", index=True)
