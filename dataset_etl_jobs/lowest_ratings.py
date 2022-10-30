"""This module contains all jobs for investigating categories"""

from pyspark.sql import DataFrame, SparkSession, functions as f
from spark_setup.spark_setup import write_dataframe_parquet, get_parquet_df, get_spark_session

from data.paths.spark_parquet_paths import BUSINESS


def prepare_business_df(spark_session: SparkSession) -> DataFrame:
    """
    Reads business dataframe
    :param SparkSession spark_session: SparkSession object
    :return: Read dataframe
    """
    return (get_parquet_df(BUSINESS,
                           spark_session)
            .select('business_id',
                    'categories',
                    'stars',
                    'review_count'
                    ))


def process_business_df(business_df: DataFrame) -> DataFrame:
    """
    Encapsulates whole pipeline process
        - sorts categories column
        - groups by it and applies avg on stars and sum on review_count
        - orders by avg_stars ascending
    :param business_df:
    :return: result_df
    """
    return (business_df
            .withColumn('categories', f.sort_array(f.col('categories')))
            .groupBy('categories')
            .agg(f.round(f.avg('stars')).alias('avg_stars'), f.sum('review_count').alias('category_reviews'))
            .orderBy(f.col('avg_stars')))


if __name__ == "__main__":
    prepared_business_df = prepare_business_df(get_spark_session())
    result = process_business_df(prepared_business_df)
    write_dataframe_parquet(result,
                            'lowest_ratings',
                            'overwrite')
