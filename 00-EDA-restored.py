#%% imports

import pandas as pd
from datetime import datetime
import numpy as np


#%% load datasets

fleet_df = pd.read_csv("raw_data/RNLI_Lifeboat_Fleet.csv")
stations_df = pd.read_csv("raw_data/RNLI_Lifeboat_Station_Locations.csv")
units_df = pd.read_csv("raw_data/RNLI_Lifeguard_Units.csv")
returns_df = pd.read_csv("raw_data/RNLI_Returns_of_Service.csv")

#%% filter returns data

returns_df['DateOfLaunch'] = pd.to_datetime(returns_df['DateOfLaunch'])
filtered_returns = returns_df[returns_df['DateOfLaunch'].dt.year >= 2020]
filtered_returns = filtered_returns.dropna(subset=['X', 'Y'], axis=0, how='any')
filtered_returns['LifeboatStationNameProper'] = filtered_returns['LifeboatStationNameProper'].astype('string').str.lower()
filtered_returns = filtered_returns[['X', 'Y', 'AIC', 'LifeboatStationNameProper', 'CasualtyCategory', 'CasualtyTypeFull', 'OutcomeOfService', 'Activity', 'DateOfLaunch']]


#%% filter station locations

stations_df = stations_df[['X', 'Y', 'Station']]
stations_df['Station'] = stations_df['Station'].astype('string').str.lower()
merged_df = filtered_returns.merge(stations_df, how='left', left_on='LifeboatStationNameProper', right_on='Station', suffixes=['_dest', '_station'])
merged_df = merged_df.drop(columns=['LifeboatStationNameProper'])

#%% validate co-ords


def haversine(
    lon1: np.array,
    lat1: np.array,
    lon2: np.array,
    lat2: np.array,
) -> np.array:
    """Calculate the haversine distance between two coordinates.
    :param lon1: Longitude point 1.
    :param lat1: Latitude point 1.
    :param lon2: Longitude point 2.
    :param lat2: Latitude point2.
    :param logger: Optional logger to output activity.
    :return distance: Array of calculated distances."""
    # convert decimal degrees to radians
    lon1 = lon1.map(np.radians)
    lat1 = lat1.map(np.radians)
    lon2 = lon2.map(np.radians)
    lat2 = lat2.map(np.radians)

    # haversine formula
    d_lon = lon2 - lon1
    d_lat = lat2 - lat1
    a = np.sin(d_lat / 2) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin(d_lon / 2) ** 2
    c = 2 * np.arcsin(np.sqrt(a))
    r = 6371000
    distance = c * r
    return distance

merged_df['distance'] = haversine(merged_df.X_dest, merged_df.Y_dest, merged_df.X_station, merged_df.Y_station)
merged_df.dropna(subset=['distance'], axis=0, how='any', inplace=True)

#%% IQR removal of outliers

def iqr_outliers(data: pd.Series) -> float:
    q3, q1 = np.percentile(data.to_numpy(), [75, 25])
    IQR = q3 - q1
    upper_bound = q3 + 1.5 * IQR
    lower_bound = q1 - 1.5 * IQR
    return lower_bound, upper_bound

lower, upper = iqr_outliers(merged_df['distance'])
merged_df = merged_df[merged_df['distance'].between(lower, upper)]
#%% save df

merged_df.to_parquet("./cleaned_data/2020_dataset.parquet")
