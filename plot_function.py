# -*- coding: utf-8 -*-
"""
Created on Sun Jun 26 20:41:01 2022

@author: alexc
"""

# imports
from matplotlib import pyplot as plt
import cartopy
from datetime import datetime
from cartopy import crs as ccrs
import pandas as pd

# station dataset

station_df = pd.read_csv("raw_data/RNLI_Lifeboat_Station_Locations.csv")


def plot_map(action_df=None, time: datetime = None):
    plt.figure(figsize=(10, 10))
    ax = plt.axes(projection=ccrs.PlateCarree())

    # add features to prettify
    ax.add_feature(cartopy.feature.OCEAN, color="0.05")
    ax.add_feature(cartopy.feature.COASTLINE, color="white", alpha=0.25)
    ax.add_feature(cartopy.feature.LAND, color="0.15")

    year = str(time.year)
    month = str(time.month)
    day = str(time.day)
    hour = str(time.hour)

    if len(month) == 1:
        month = "0" + month
    if len(day) == 1:
        day = "0" + day
    if len(hour) == 1:
        hour = "0" + hour
    filename = f"{year}{month}{day}T{hour}"

    #
    plt.text(-1, 58, f"{day}-{month}-{year}", fontsize=22, c="white")

    # plot stations
    ax.scatter(x=station_df["X"], y=station_df["Y"], s=10, c="g")

    # plot active stations
    if action_df.shape[0] > 0:
        val_list = action_df.time_diff_days.unique().tolist()
        for value in val_list:
            mask_df = action_df[action_df["time_diff_days"] == value]
            size = 80 - 12 * value
            ax.scatter(
                x=mask_df["X_station"], y=mask_df["Y_station"], s=size, c="red",
            )
    plt.xlim(-11, 3)
    plt.ylim(48, 62)
    plt.savefig(f"./images/{filename}.jpg", bbox_inches="tight", pad_inches=0)
