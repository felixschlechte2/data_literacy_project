import pandas as pd
import geopandas as gpd
from shapely.geometry import Point

# Load station data (your CSV with latitude and longitude columns)
stations = pd.read_csv('unique_air_quality_stations.csv')  # Replace with your actual file
stations['geometry'] = stations.apply(lambda row: Point(row['Longitude'], row['Latitude']), axis=1)
stations_gdf = gpd.GeoDataFrame(stations, geometry='geometry', crs="EPSG:4326")  # Ensure CRS is WGS84

# Function to perform spatial join with GADM shapefiles
def spatial_join_gadm(stations_gdf, gadm_file, level_name):
    print(f"Processing GADM file: {gadm_file} for {level_name}")
    gadm_gdf = gpd.read_file(gadm_file)  # Load GADM shapefile
    gadm_gdf = gadm_gdf.to_crs(stations_gdf.crs)  # Ensure CRS match
    # Use 'predicate' instead of 'op'
    joined = gpd.sjoin(stations_gdf, gadm_gdf, how='left', predicate='within')
    return joined[f'NAME_{level_name}'] if f'NAME_{level_name}' in joined.columns else None


# List of GADM files and corresponding level names
gadm_files = {
    0: './gadm41_DEU_shp/gadm41_DEU_0.shp',  # Country level
    1: './gadm41_DEU_shp/gadm41_DEU_1.shp',  # State level
    2: './gadm41_DEU_shp/gadm41_DEU_2.shp',  # District level
    3: './gadm41_DEU_shp/gadm41_DEU_3.shp',  # Town/Municipality level (if available)
}

# Add state, district, and city/town fields to stations
stations['state'] = spatial_join_gadm(stations_gdf, gadm_files[1], 1)  # State
stations['district'] = spatial_join_gadm(stations_gdf, gadm_files[2], 2)  # District
stations['town_city'] = spatial_join_gadm(stations_gdf, gadm_files[3], 3)  # Town/City

# Save results to a CSV
stations.to_csv('stations_with_location.csv', index=False)
print("CSV saved: stations_with_location.csv")
