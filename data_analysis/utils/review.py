import pandas as pd

def prepare_review_df(review_df: pd.DataFrame):
    review_df['text_len'] = review_df['text'].apply(len)
    
    return review_df
