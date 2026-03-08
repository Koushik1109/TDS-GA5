import pandas as pd
import math

df = pd.read_csv("d:/IIT MADRAS/TDS/GA5/21/rideshare_trips.csv")
df["start_time"] = pd.to_datetime(df["start_time"], format='ISO8601')

# Step A: Filter peak hours
df["hour"] = df["start_time"].dt.hour
peak = df[(df["hour"] >= 17) & (df["hour"] < 21)]

# Step B: Haversine distance
def haversine(row):
    R = 6371
    lat1, lon1 = math.radians(row["pickup_lat"]), math.radians(row["pickup_lon"])
    lat2, lon2 = math.radians(row["dropoff_lat"]), math.radians(row["dropoff_lon"])
    dlat, dlon = lat2 - lat1, lon2 - lon1
    a = math.sin(dlat/2)**2 + math.cos(lat1)*math.cos(lat2)*math.sin(dlon/2)**2
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

peak = peak.copy()
peak["dist_km"] = peak.apply(haversine, axis=1)
long_trips = peak[peak["dist_km"] > 6]

# Step C: Top driver
result = long_trips.groupby("driver_id")["fare_amount"].sum()
top_driver = result.idxmax()
top_fare = round(result.max(), 2)
print(f"{top_driver}, {top_fare}")
