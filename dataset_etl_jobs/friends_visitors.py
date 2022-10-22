"""This module contains all jobs
in order to get friends of user which have left a review/tip on this business"""

from pyspark.sql import DataFrame, SparkSession, functions as f
from spark_setup.spark_setup import get_parquet_df, write_dataframe_parquet, get_spark_session

from data.paths.spark_parquet_paths import BUSINESS, REVIEW, USER, TIP


def prepare_business_df(spark_session: SparkSession) -> DataFrame:
    """
    Reads business dataframe, selects columns business id and name
    :param SparkSession spark_session: SparkSession object
    :returns: Read dataframe
    """
    return (get_parquet_df(BUSINESS,
                           spark_session)
            .select('business_id',
                    'name'))


def prepare_review_df(spark_session: SparkSession) -> DataFrame:
    """
    Reads review df,selects needed columns
    :param spark_session: SparkSession object
    :return: Read dataframe
    """
    return (get_parquet_df(REVIEW,
                           spark_session)
            .select('business_id',
                    'review_id',
                    'user_id'))


def prepare_tip_df(spark_session: SparkSession) -> DataFrame:
    """
    Reads tip df,selects needed columns
    :param spark_session: SparkSession object
    :return: Read dataframe
    """
    return (get_parquet_df(TIP,
                           spark_session)
            .select('business_id',
                    'user_id'))


def prepare_user_df(spark_session: SparkSession) -> DataFrame:
    """
    Reads user df,selects needed columns
    :param spark_session: SparkSession object
    :return: Read dataframe
    """
    return (get_parquet_df(USER,
                           spark_session)
            .select('user_id',
                    'name',
                    'friends'))


def process_reviews(business_df: DataFrame,
                    reviews_df: DataFrame,
                    tip_df: DataFrame,
                    user_df: DataFrame) -> DataFrame:
    """
    Provides whole data pipeline process:
        - Creates basic reviews_tips dataframe,
            which in fact has all 'visits' of all users (all tips and reviews)
            which will be used to get friends of every user that visited a business
            (this is reachable by union)
        - Creates copy of reviews_tips df for joining with user_business_reviews
        - Processes users_business_reviews dataframe,
            which is created by joining business and user to review, so we have
            record with : business_id, user_id, friends
                which can be interpreted as 'visit' of user to business
        - Creates array of friends, explodes them
        - Finds corresponding record in reviews_tips_friends for each friend
            by inner joining users_business_reviews and reviews_tips_friends
    :param business_df: prepared business dataframe
    :param reviews_df: prepared reviews dataframe
    :param tip_df: prepared tip dataframe
    :param user_df: prepared user dataframe
    :returns: result df with user`s friends` which have visited a business
    """
    reviews_tips = (reviews_df.drop('review_id').union(tip_df)
                    .join(user_df, ['user_id'])
                    .select(f.col('business_id'),
                            f.col('user_id').alias('user_id_joined'),
                            f.col('name').alias('user_name_joined'),
                            f.col('friends')))

    reviews_tips_friends = (reviews_tips.select('business_id',
                                                f.col('user_id_joined')
                                                .alias('user_id_friend'),
                                                f.col('user_name_joined')
                                                .alias('user_name_friend')))
    users_business_reviews = (reviews_tips
                              .join(business_df, ['business_id'])
                              .select(f.col('business_id').alias('business_id_reviews'),
                                      f.col('name').alias('business_name'),
                                      f.col('user_id_joined').alias('user_id'),
                                      f.col('user_name_joined').alias('user_name'),
                                      f.explode(f.col('friends')).alias('friend_id')))

    users_friends_join_condition = (
        [(users_business_reviews.business_id_reviews == reviews_tips_friends.business_id)
         & (users_business_reviews.friend_id == reviews_tips_friends.user_id_friend)])

    users_with_friends = (users_business_reviews
                          .join(reviews_tips_friends, users_friends_join_condition)
                          .select('business_id',
                                  'business_name',
                                  'user_id',
                                  'user_name',
                                  f.struct(f.col('friend_id').alias('user_id'),
                                           f.col('user_name_friend').alias('user_name'))
                                  .alias('friends_attendees')))
    return (users_with_friends
            .groupBy(['business_id', 'user_id']).agg(f.first('business_name')
                                                     .alias('business_name'),
                                                     f.first('user_name')
                                                     .alias('user_name'),
                                                     f.collect_list('friends_attendees')
                                                     .alias('friends_attendees'))
            .select('business_id', 'business_name',
                    'user_id', 'user_name', 'friends_attendees'))


if __name__ == "__main__":
    prepared_business_df = prepare_business_df(get_spark_session())
    prepared_reviews_df = prepare_review_df(get_spark_session())
    prepared_tip_df = prepare_tip_df(get_spark_session())
    prepared_user_df = prepare_user_df(get_spark_session())
    result = process_reviews(prepared_business_df,
                             prepared_reviews_df,
                             prepared_tip_df,
                             prepared_user_df)
    write_dataframe_parquet(result,
                            'friends_visitors',
                            'overwrite')
