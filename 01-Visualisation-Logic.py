# -*- coding: utf-8 -*-
"""
Created on Sun Jun 26 20:20:30 2022

@author: alexc
"""

#%% imports

import pandas as pd
from datetime import datetime, timedelta, timezone
import logging

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)
from plot_function import plot_map

#%% load dataset

df = pd.read_parquet("cleaned_data/2020_dataset.parquet")

#%% vis logic

iter_time = datetime(2020, 1, 1, 0)
while iter_time <= datetime(2020, 2, 1, 8, 59):  # datetime(2020, 12, 31, 23, 59):
    logger.info(iter_time)
    lower_bound = iter_time - timedelta(hours=6)
    lower_bound = lower_bound.replace(tzinfo=timezone.utc)
    now_time = iter_time.replace(tzinfo=timezone.utc)
    temp_df = df.query("DateOfLaunch >= @lower_bound")
    temp_df = temp_df.query("DateOfLaunch <= @now_time")
    temp_df["time_diff_hrs"] = (
        now_time - temp_df["DateOfLaunch"]
    ).dt.total_seconds() / 3600
    plot_map(temp_df, now_time)
    logger.info(temp_df.shape)
    iter_time += timedelta(hours=1)
