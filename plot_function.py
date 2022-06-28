# -*- coding: utf-8 -*-
"""
Created on Sun Jun 26 20:41:01 2022

@author: alexc
"""

# imports
from matplotlib import pyplot as plt
import cartopy
from cartopy import crs as ccrs
import pandas as pd

# station dataset

station_df = pd.read_csv("raw_data/RNLI_Lifeboat_Station_Locations.csv")

colour_list = ["b", "g", "r", "c", "m", "y", "k", "w"]

# plot


def plot_map(action_df=None, time=None):
    # xlim min -11
    # xlim max 3
    # ylim max 62
    # ylime min 48
    plt.figure(figsize=(10, 10))
    ax = plt.axes(projection=ccrs.PlateCarree())
    ax.gridlines(draw_labels=True, dms=True, x_inline=False, y_inline=False)

    # add features to prettify
    ax.add_feature(cartopy.feature.OCEAN)
    ax.add_feature(cartopy.feature.RIVERS)
    ax.add_feature(cartopy.feature.LAND)

    # plot lines from stations to points
    for index, row in action_df.iterrows():
        ax.plot([row["X_dest"], row["X_station"]], [row["Y_dest"], row["Y_station"]])
    # plot stations
    ax.scatter(x=station_df["X"], y=station_df["Y"], s=5)

    # plot active stations
    ax.scatter(x=action_df["X_station"], y=action_df["Y_station"], s=20, c="red")

    for i in range(0, 7):
        print(i)
        temp_df = action_df[action_df["time_diff_hrs"] == i]
        if temp_df.shape[0] != 0:
            print("plot")
            ax.scatter(temp_df["X_dest"], temp_df["Y_dest"], s=i, c=colour_list[i])
    plt.xlim(-1, 1)  # plt.xlim(-11, 3)
    plt.ylim(50, 52)  # plt.ylim(48, 62)
    plt.legend()
    plt.show()
