from pathlib import Path
import pandas as pd


def append_nested_columns(dataframe: pd.DataFrame, col_name: str) -> pd.DataFrame:
    """
    Flattens nested json and appends result columns to target dataframe
    :param dataframe: target pandas dataframe
    :param col_name: name of column containing json
    :returns: targe df with appended nested columns
    """
    dataframe = pd.concat([dataframe, pd.json_normalize(
        dataframe[col_name].values.tolist())], axis=1)  # type: ignore
    return dataframe

def save_df_to_json(df: pd.DataFrame, path: Path | str):
    df.to_json(path_or_buf=path, orient="records", index=True)