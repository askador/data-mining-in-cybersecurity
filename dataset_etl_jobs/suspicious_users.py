import uuid
import random
from pyspark.sql import DataFrame, SparkSession, types as t, functions as f
from spark_setup.spark_setup import get_spark_session, write_dataframe_parquet


def create_users(spark_session: SparkSession) -> (DataFrame, DataFrame):
    random_values = [0, 4, 7]
    suspicious_stars = [0, 5]
    unsuspicious_stars = list(range(6))
    count_reviews = [1, 3, 10, 23]
    suspicious_values = [0, 2, 10]
    unsuspicious_values = [10, 20, 30]
    users_id = [str(uuid.uuid4()) for _ in range(5000)]

    schema = t.StructType([
        t.StructField('user_id', t.StringType()),
        t.StructField('useful', t.IntegerType()),
        t.StructField('funny', t.IntegerType()),
        t.StructField('cool', t.IntegerType()),
        t.StructField('fans', t.IntegerType()),
        t.StructField('compliments', t.IntegerType())
    ])
    user_values = [*[[users_id[i], random.choice(random_values),
                      random.choice(random_values), random.choice(random_values),
                      random.choice([0, 100, 50, 31, 1]), random.choice([0, 4, 100])]
                     for i in range(5000)]]

    users = spark_session.createDataFrame(user_values, schema)

    review_values = []
    review_schema = t.StructType([
        t.StructField('review_id', t.StringType()),
        t.StructField('user_id', t.StringType()),
        t.StructField('stars', t.IntegerType()),
        t.StructField('funny', t.IntegerType()),
        t.StructField('cool', t.IntegerType()),
        t.StructField('useful', t.IntegerType())
    ])
    for i in range(5000):
        inner_loop_value = random.choice(count_reviews)
        should_be_suspicious = (inner_loop_value > 5)
        for _ in range(inner_loop_value):
            if should_be_suspicious:
                review_values.append([str(uuid.uuid4()), users_id[i],
                                      random.choice(suspicious_stars),
                                      random.choice(suspicious_values),
                                      random.choice(suspicious_values),
                                      random.choice(suspicious_values)
                                      ])
            else:
                review_values.append([str(uuid.uuid4()), users_id[i],
                                      random.choice(unsuspicious_stars),
                                      random.choice(unsuspicious_values),
                                      random.choice(unsuspicious_values),
                                      random.choice(unsuspicious_values)
                                      ])
    reviews = spark_session.createDataFrame(review_values, review_schema)
    return users, reviews


def find_suspicious(users_df: DataFrame,
                    reviews_df: DataFrame) -> DataFrame:
    reviews_counted = (reviews_df
                       .withColumn('review_suspicious',
                                   f.when(((f.col('useful') + f.col('funny')
                                            + f.col('cool')) < 10) &
                                          ((f.col('stars') == 5) | (f.col('stars') == 0)), 1)
                                   .otherwise(0))
                       .groupBy('user_id')
                       .agg(f.sum('review_suspicious').alias('sum_suspicious'))
                       .filter('sum_suspicious > 5'))
    users_marked = users_df.withColumn('is_suspicious',
                                       ((f.col('useful') + f.col('funny')
                                         + f.col('cool')
                                         + f.col('compliments')) < 10) & (f.col('fans') <= 5))
    result = (users_marked
              .join(reviews_counted, 'user_id')
              .select('user_id', 'useful', 'funny',
                      'cool', 'fans', 'compliments', 'is_suspicious'))
    return result


if __name__ == '__main__':
    users, reviews = create_users(get_spark_session())
    write_dataframe_parquet(users, 'users_sample', 'overwrite')
    write_dataframe_parquet(reviews, 'reviews_sample', 'overwrite')
    res = find_suspicious(users, reviews)

    write_dataframe_parquet(res, 'suspicious_users_statistics', 'overwrite')
