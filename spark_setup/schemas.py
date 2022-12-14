"""This module contains schemas for all necessary files in YELP dataset"""
from pyspark.sql import types as t

BUSINESS_SCHEMA = t.StructType([
    t.StructField('business_id', t.StringType()),
    t.StructField('name', t.StringType()),
    t.StructField('address', t.StringType()),
    t.StructField('attributes', t.StructType([
        t.StructField('AcceptsInsurance', t.StringType()),
        t.StructField('AgesAllowed', t.StringType()),
        t.StructField('Alcohol', t.StringType()),
        t.StructField('Ambience', t.StringType()),
        t.StructField('BYOB', t.StringType()),
        t.StructField('BYOBCorkage', t.StringType()),
        t.StructField('BestNights', t.StringType()),
        t.StructField('BikeParking', t.StringType()),
        t.StructField('BusinessAcceptsBitcoin', t.StringType()),
        t.StructField('BusinessAcceptsCreditCards', t.StringType()),
        t.StructField('BusinessParking', t.StringType()),
        t.StructField('ByAppointmentOnly', t.StringType()),
        t.StructField('Caters', t.StringType()),
        t.StructField('CoatCheck', t.StringType()),
        t.StructField('Corkage', t.StringType()),
        t.StructField('DietaryRestrictions', t.StringType()),
        t.StructField('DogsAllowed', t.StringType()),
        t.StructField('DriveThru', t.StringType()),
        t.StructField('GoodForDancing', t.StringType()),
        t.StructField('GoodForKids', t.StringType()),
        t.StructField('GoodForMeal', t.StringType()),
        t.StructField('HairSpecializesIn', t.StringType()),
        t.StructField('HappyHour', t.StringType()),
        t.StructField('HasTV', t.StringType()),
        t.StructField('Music', t.StringType()),
        t.StructField('NoiseLevel', t.StringType()),
        t.StructField('Open24Hours', t.StringType()),
        t.StructField('OutdoorSeating', t.StringType()),
        t.StructField('RestaurantsAttire', t.StringType()),
        t.StructField('RestaurantsCounterService', t.StringType()),
        t.StructField('RestaurantsDelivery', t.StringType()),
        t.StructField('RestaurantsGoodForGroups', t.StringType()),
        t.StructField('RestaurantsPriceRange2', t.StringType()),
        t.StructField('RestaurantsReservations', t.StringType()),
        t.StructField('RestaurantsTableService', t.StringType()),
        t.StructField('RestaurantsTakeOut', t.StringType()),
        t.StructField('Smoking', t.StringType()),
        t.StructField('WheelchairAccessible', t.StringType()),
        t.StructField('WiFi', t.StringType()),
    ])),
    t.StructField('city', t.StringType()),
    t.StructField('state', t.StringType()),
    t.StructField('postal_code', t.StringType()),
    t.StructField('latitude', t.FloatType()),
    t.StructField('longitude', t.FloatType()),
    t.StructField('stars', t.FloatType()),
    t.StructField('review_count', t.IntegerType()),
    t.StructField('is_open', t.IntegerType()),
    t.StructField('categories', t.StringType()),
    t.StructField('hours', t.StructType([
        t.StructField('Monday', t.StringType()),
        t.StructField('Tuesday', t.StringType()),
        t.StructField('Friday', t.StringType()),
        t.StructField('Wednesday', t.StringType()),
        t.StructField('Thursday', t.StringType()),
        t.StructField('Sunday', t.StringType()),
        t.StructField('Saturday', t.StringType()),
    ]))
])

CHECKIN_SCHEMA = t.StructType([
    t.StructField('business_id', t.StringType()),
    t.StructField('date', t.StringType())
])

REVIEW_SCHEMA = t.StructType([
    t.StructField('review_id', t.StringType()),
    t.StructField('user_id', t.StringType()),
    t.StructField('business_id', t.StringType()),
    t.StructField('stars', t.FloatType()),
    t.StructField('date', t.DateType()),
    t.StructField('text', t.StringType()),
    t.StructField('useful', t.IntegerType()),
    t.StructField('funny', t.IntegerType()),
    t.StructField('cool', t.IntegerType()),
])

TIP_SCHEMA = t.StructType([
    t.StructField('text', t.StringType()),
    t.StructField('date', t.StringType()),
    t.StructField('compliment_count', t.IntegerType()),
    t.StructField('business_id', t.StringType()),
    t.StructField('user_id', t.StringType()),
])

USER_SCHEMA = t.StructType([
    t.StructField('user_id', t.StringType()),
    t.StructField('name', t.StringType()),
    t.StructField('review_count', t.IntegerType()),
    t.StructField('yelping_since', t.StringType()),
    t.StructField('friends', t.StringType()),
    t.StructField('useful', t.IntegerType()),
    t.StructField('funny', t.IntegerType()),
    t.StructField('cool', t.IntegerType()),
    t.StructField('fans', t.IntegerType()),
    t.StructField('elite', t.ArrayType(t.IntegerType())),
    t.StructField('average_stars', t.FloatType()),
    t.StructField('compliment_hot', t.IntegerType()),
    t.StructField('compliment_more', t.IntegerType()),
    t.StructField('compliment_profile', t.IntegerType()),
    t.StructField('compliment_cute', t.IntegerType()),
    t.StructField('compliment_list', t.IntegerType()),
    t.StructField('compliment_note', t.IntegerType()),
    t.StructField('compliment_plain', t.IntegerType()),
    t.StructField('compliment_cool', t.IntegerType()),
    t.StructField('compliment_funny', t.IntegerType()),
    t.StructField('compliment_writer', t.IntegerType()),
    t.StructField('compliment_photos', t.IntegerType())
])
