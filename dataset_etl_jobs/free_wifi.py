"""This module contains all jobs for investigating wifi attribute"""

from pyspark.sql import DataFrame, SparkSession, functions as f
from spark_setup.spark_setup import write_dataframe_parquet, get_parquet_df, get_spark_session

from data.paths.spark_parquet_paths import BUSINESS


def prepare_business_df(spark_session: SparkSession) -> DataFrame:
    """
    Reads business dataframe naming wifi column
    :param SparkSession spark_session: SparkSession object
    :return: Read dataframe
    """
    return (get_parquet_df(BUSINESS,
                           spark_session)
            .select('business_id',
                    'name',
                    'attributes.WiFi',
                    'city',
                    'state',
                    'latitude',
                    'longitude',
                    ))


def mark_free_wifi(cleaned_wifi_df: DataFrame) -> DataFrame:
    """
    Marks dataframe using boolean filter on true or false
    :param cleaned_wifi_df: wifi column with cleaned values from quotes
    :returns: dataframe with column free_wifi containing boolean values
    """
    filtered_available_wifi = cleaned_wifi_df.filter("WiFi == 'free' or WiFi =='paid'")
    return filtered_available_wifi.select(
        'business_id',
        'name',
        'city',
        'state',
        'latitude',
        'longitude',
        (f.col('WiFi') == 'free').alias('free_wifi')
    )


def process_business_df(business_df: DataFrame) -> DataFrame:
    """
    Encapsulates whole pipeline process
        - Cleans wifi column,
        - Marks free_wifi column based on condition
    :param business_df:
    :return: result_df
    """
    marked_wifi = mark_free_wifi(business_df)
    return marked_wifi


if __name__ == "__main__":
    prepared_business_df = prepare_business_df(get_spark_session())
    result = process_business_df(prepared_business_df)
    write_dataframe_parquet(result,
                            'wifi_businesses',
                            'overwrite')
