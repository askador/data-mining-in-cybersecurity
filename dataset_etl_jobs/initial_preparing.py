"""This module contains transformations from json to csv"""
from typing import Tuple

from pyspark.sql import DataFrame, SparkSession, functions as f, types as t

from spark_setup.spark_setup import get_spark_session, get_json_df, write_dataframe_parquet, clear_col_nested
from spark_setup.schemas import BUSINESS_SCHEMA, USER_SCHEMA, REVIEW_SCHEMA
from spark_setup.schemas import TIP_SCHEMA, CHECKIN_SCHEMA

from data.paths.parquet_paths import BUSINESS, USER, REVIEW, TIP, CHECKIN


def create_type_schema(parsed_fields: list[str], spark_type) -> t.StructType:
    return t.StructType([
        t.StructField(field, spark_type()) for field in parsed_fields
    ])


def prepare_business_df(spark_session: SparkSession) -> DataFrame:
    """Prepares business df:
        - Handles categories column, splitting it to array,
            and replacing nulls with an empty string
        - Takes attributes and creates json objects from them
        - Clears columns (can be extended)
    :returns: Dataframe object"""
    raw_business_df = (get_json_df(BUSINESS,
                                   spark_session,
                                   schema=BUSINESS_SCHEMA)
                       )
    business_parking_parsed_fields = ["garage", "street", "validated", "lot", "valet"]
    ambience_parsed_fields = ['touristy', 'hipster', 'romantic',
                              'intimate', 'trendy', 'upscale',
                              'classy', 'casual']
    good_for_meal = ['dessert', 'latenight', 'lunch', 'dinner', 'brunch', 'breakfast']

    ambience_json_schema = create_type_schema(ambience_parsed_fields, t.BooleanType)
    business_parking_json_schema = create_type_schema(business_parking_parsed_fields, t.BooleanType)
    good_for_meal_json_schema = create_type_schema(good_for_meal, t.BooleanType)

    raw_business_df = (raw_business_df
                       .withColumn('categories',
                                   f.when(
                                       f.col('categories').isNull(),
                                       '')
                                   .otherwise(f.col('categories')))
                       .withColumn('categories', f.split('categories', ', '))

                       .withColumn('BusinessParking',
                                   f.lower(f.col('attributes.BusinessParking')))
                       .withColumn('Ambience',
                                   f.lower(f.col('attributes.Ambience')))
                       .withColumn('GoodForMeal',
                                   f.lower(f.col('attributes.GoodForMeal')))

                       .withColumn('BusinessParking',
                                   f.to_json(f.from_json(
                                       f.col('BusinessParking'),
                                       business_parking_json_schema,
                                       {"mode": "PERMISSIVE"})))
                       .withColumn('Ambience',
                                   f.to_json(f.from_json(
                                       f.col('Ambience'),
                                       ambience_json_schema,
                                       {"mode": "PERMISSIVE"})))
                       .withColumn('GoodForMeal',
                                   f.to_json(f.from_json(
                                       f.col('GoodForMeal'),
                                       good_for_meal_json_schema,
                                       {"mode": "PERMISSIVE"})))
                       )
    result = clear_col_nested(raw_business_df, 'attributes', 'WiFi')
    return result


def prepare_user_df(spark_session: SparkSession) -> DataFrame:
    """Prepares user df:
        - Splits friends column
    :returns: Dataframe object"""
    raw_user_df = (get_json_df(USER,
                               spark_session,
                               schema=USER_SCHEMA)
                   )
    return raw_user_df.withColumn('friends', f.split('friends', ', '))


def prepare_checkin_df(spark_session: SparkSession) -> DataFrame:
    """Prepares checkin df:
        - Splits date column
    :returns: Dataframe object"""
    raw_user_df = (get_json_df(CHECKIN,
                               spark_session,
                               schema=CHECKIN_SCHEMA)
                   )
    return raw_user_df.withColumn('date', f.split('date', ', '))


def prepare_write_dataframes(spark_session: SparkSession) -> None:
    prepared_business_df = prepare_business_df(spark_session)
    prepared_user_df = prepare_user_df(spark_session)
    prepared_checkin_df = prepare_checkin_df(spark_session)

    read_review_df = get_json_df(REVIEW, spark_session, schema=REVIEW_SCHEMA)
    read_tip_df = get_json_df(TIP, spark_session, schema=TIP_SCHEMA)

    write_dataframe_parquet(prepared_business_df, 'yelp_academic_dataset_business_short', 'overwrite')
    write_dataframe_parquet(prepared_user_df, 'yelp_academic_dataset_user_short', 'overwrite')
    write_dataframe_parquet(prepared_checkin_df, 'yelp_academic_dataset_checkin_short', 'overwrite')
    write_dataframe_parquet(read_tip_df, 'yelp_academic_dataset_tip_short', 'overwrite')
    write_dataframe_parquet(read_review_df, 'yelp_academic_dataset_review_short', 'overwrite')


if __name__ == '__main__':
    prepare_write_dataframes(get_spark_session())
