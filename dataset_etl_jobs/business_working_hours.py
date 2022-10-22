"""This module contains all jobs for getting working hours"""
from pyspark.sql import SparkSession, DataFrame, functions as f, types as t

from spark_setup.spark_setup import get_parquet_df, get_spark_session, write_dataframe_parquet

from data.paths.spark_parquet_paths import BUSINESS

DAYS_TUPLE = ('Sunday', 'Monday', 'Tuesday',
              'Wednesday', 'Thursday', 'Friday', 'Saturday')
DAYS_HRS_LIST = [day + '_hrs' for day in DAYS_TUPLE]

WHOLE_DAY_VALUE = 24.0
HALF_DAY_VALUE = 12.0
TIMESTAMP_HOUR_DENOMINATOR = 3600


def prepare_business_df(spark_session: SparkSession) -> DataFrame:
    """
    Reads business dataframe naming each day column respectively to DAYS_TUPLE,
        - Additionally, creates array column "hours" from similar structure
    :param SparkSession spark_session: SparkSession object
    :return: Read dataframe
    """
    return (get_parquet_df(BUSINESS,
                           spark_session)
            .select('business_id',
                    'name',
                    f.array(*[f'hours.{day}' for day in DAYS_TUPLE]).alias('hours')))


def split_schedule_weekday(prepared_business_df: DataFrame) -> DataFrame:
    """
    --------1-st withColumn------------------------------
    Adds column based on schedule string
    with format like 'hour:minute - hour1:minute1' converted to timestamps,
    transformed to difference between timestamps,
    then modifies it, because exceptions may be not caught:
    --------2-st withColumn---------------------------------
        - In regular case , f.e. '12:0 - 17:0' we receive 5.0, leave like it is
        - In case '12:0 - 2:0'  we receive -10.0 hours, although we want 14.0,
            that's because times are converted to single date.
            In this case, we modify value, adding 24.0 hours, receiving -10+24 = 14.0
        - In case '0:0 - 0:0' we receive 0.0 hrs, this situation can be caught only if
            start and end are the same timestamps ,
            so we are free to set this field`s hours FROM 0.0 TO 24.0

    :param DataFrame prepared_business_df: prepared business df
    :returns: Dataframe object with result column named work_hours
    """
    return (prepared_business_df
            .withColumn('work_hours', (f.to_timestamp(f.split
                                                      (f.col('schedule_weekday'), '-')
                                                      .getItem(1), 'H:m')
                                       .cast('long')
                                       - f.to_timestamp(f.split
                                                        (f.col('schedule_weekday'), '-')
                                                        .getItem(0), 'H:m')
                                       .cast('long')) / TIMESTAMP_HOUR_DENOMINATOR)
            .withColumn('work_hours',
                        f.when(f.col('work_hours') < 0,
                               WHOLE_DAY_VALUE + f.col('work_hours'))
                        .when(f.col('work_hours') == 0, WHOLE_DAY_VALUE)
                        .otherwise(f.col('work_hours'))))


def count_hours_mark_24(converted_hours: DataFrame) -> DataFrame:
    """Counts average hours value, marks businesses opened for 24 h
        - Groups by business_id and name, counting avg work_hours,
        - Collects list of working hours for each business
        - Filters records which don't have at least one day of 12-h working(or more)
        - Marks those records, that have at least one day of 24-h working
    :returns: Dataframe with counted average hours of work, marked is_open_for_24h column"""
    return (converted_hours
            .groupBy('business_id')
            .agg(f.avg('work_hours').alias('avg_hours_open'),
                 f.collect_list('work_hours').alias('list_work_hours'),
                 f.max('work_hours').alias('max_hours_day'),
                 f.first('name').alias('name'))
            .filter(f.col('max_hours_day') >= HALF_DAY_VALUE)
            .select('business_id',
                    'name',
                    f.round('avg_hours_open', 2)
                    .alias('avg_hours_open').cast(t.FloatType()),
                    f.array_contains('list_work_hours', WHOLE_DAY_VALUE)
                    .alias('is_open_for_24h')))


def process_business_df(prepared_business_df: DataFrame) -> DataFrame:
    """
    Encapsulates all data pipeline process.
        - Explodes array of work_schedules
        - Converts this schedule to difference between timestamps
        - Counts average hours value and marks with boolean value
            those business, which are opened 24-hrs at least one day in a week,
            collecting this value to single list
    :param DataFrame prepared_business_df: Read dataframe
    :returns: Result exercise 1 dataframe
    """
    exploded_hrs = (prepared_business_df.select('business_id',
                                                'name',
                                                f.explode('hours').alias('schedule_weekday')))
    hours_converted = split_schedule_weekday(exploded_hrs)
    counted_hours = count_hours_mark_24(hours_converted)
    return counted_hours


if __name__ == '__main__':
    prepared_business_df = prepare_business_df(get_spark_session())
    result = process_business_df(prepared_business_df)
    write_dataframe_parquet(result, 'counted_hours_business', 'overwrite')
