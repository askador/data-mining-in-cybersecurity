"""This module contains common functions for spark jobs"""
from pyspark import SparkConf
from pyspark.sql import SparkSession, DataFrame
from pyspark.sql import types as t, functions as f

DATA_DIRECTORY = '../data/'


def get_spark_session() -> SparkSession:
    """Returns spark session with all available slots ready to work
    :returns: SparkSession object"""
    session = (SparkSession.builder
               .master('local[*]')
               .appName('pyspark_tasks')
               .config(conf=SparkConf())
               .getOrCreate())
    session.conf.set('spark.sql.shuffle.partitions', '8')
    session.conf.set("mapreduce.fileoutputcommitter.marksuccessfuljobs", "false")
    session.conf.set("parquet.enable.summary-metadata", "false")
    return session


def get_csv_df(path: str, spark: SparkSession, header: str,
               schema=None, sep: str = ',', date_format: str = 'yyyy-MM-dd') -> DataFrame:
    """Returns read dataframe with or without provided schema
    :param date_format: format for date columns
    :param str path: The path to a csv file you want to read
    :param SparkSession spark: The SparkSession object
    :param str header: may be 'true' or 'false', passed to header option in Reader
    :param t.StructType schema: Schema, which can be passed to Reader
    :param str sep: Separator in csv file default - , (can be ; or \t)
    :returns: Read dataframe"""
    if not schema:
        return (spark.read.option('sep', sep)
                .option('header', header)
                .option('dateFormat', date_format)
                .csv(path))

    return (spark.read.option('sep', sep)
            .option('header', header)
            .schema(schema)
            .option('dateFormat', date_format)
            .csv(path)).repartition(8)


def write_dataframe_parquet(data_frame: DataFrame, name: str, mode: str) -> None:
    """Writes dataframe in parquet format in the output folder
    :param DataFrame data_frame: Dataframe to be written
    :param str name: Name of file
    :param str mode: mode for writing files"""
    save_parquet_dir = f'{DATA_DIRECTORY}{name}'
    data_frame.coalesce(1).write.parquet(save_parquet_dir, mode=mode)


def get_json_df(path: str, spark: SparkSession, schema=None) -> DataFrame:
    """Returns read dataframe with or without provided schema
    :param str path: The path to a json file you want to read
    :param SparkSession spark: The SparkSession object
    :param t.StructType schema: Schema, which can be passed to the Reader
    :returns: Read dataframe"""
    if not schema:
        dataframe = (spark.read
                     .json(path))
    else:
        dataframe = (spark.read
                     .schema(schema)
                     .json(path))
    return dataframe.repartition(8)


def clear_col(target_df: DataFrame,
                 col_name:str,
                 is_array: bool = False) -> DataFrame:
    """Clears column, should be extended for arrays if needed"""
    return target_df.withColumn('test', f.regexp_replace(col_name, ".*'(.*)'.*", r"$1"))
