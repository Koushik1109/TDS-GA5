import pandas as pd
import sys
import subprocess

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

try:
    from geopy.distance import geodesic
except ImportError:
    print("Installing geopy...")
    install('geopy')
    from geopy.distance import geodesic

# Load datasets
warehouses = pd.read_csv('q-geospatial-python-closest-warehouses.csv')
orders = pd.read_csv('q-geospatial-python-closest-orders.csv')

def get_closest_warehouse(order_row, warehouses):
    order_coords = (order_row['latitude'], order_row['longitude'])
    
    distances = []
    for _, wh_row in warehouses.iterrows():
        wh_coords = (wh_row['latitude'], wh_row['longitude'])
        # using geodesic distance as prompted
        dist = geodesic(order_coords, wh_coords).kilometers
        distances.append((dist, wh_row['warehouse_id']))
        
    # extract minimum distance
    closest_warehouse = min(distances, key=lambda x: x[0])[1]
    return closest_warehouse

orders['closest_warehouse'] = orders.apply(lambda row: get_closest_warehouse(row, warehouses), axis=1)

counts = orders['closest_warehouse'].value_counts()
print("="*40)
print(counts)
print("="*40)
print(f"The warehouse that handles the most orders is {counts.index[0]}, with {counts.iloc[0]} orders.")
