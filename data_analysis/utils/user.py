import pandas as pd

def prepare_user_df(user_df: pd.DataFrame):
    user_df['yelping_since'] = pd.to_datetime(user_df['yelping_since'])
    return user_df
    
    