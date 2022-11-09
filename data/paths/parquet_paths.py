"""This module contains paths constants for parquet files"""
from pathlib import Path

CWD = Path.cwd()
BASE_DATA_PATH = 'data/yelp_academic_dataset_'
ENDING = '_short'

BUSINESS = CWD.joinpath(f'{BASE_DATA_PATH}business{ENDING}')

CHECKIN = CWD.joinpath(f'{BASE_DATA_PATH}checkin{ENDING}')

REVIEW = CWD.joinpath(f'{BASE_DATA_PATH}review{ENDING}')

TIP = CWD.joinpath(f'{BASE_DATA_PATH}tip{ENDING}')

USER = CWD.joinpath(f'{BASE_DATA_PATH}user{ENDING}')

FRIENDS_VISITORS = CWD.joinpath('data/friends_visitors')

WIFI_BUSINESSES = CWD.joinpath('data/wifi_businesses')

COUNTED_HOURS_BUSINESS = CWD.joinpath('data/counted_hours_business')

LOWEST_RATINGS = CWD.joinpath('data/lowest_ratings')

SUSPICIOUS_USERS = CWD.joinpath('data/suspicious_users_statistics')
