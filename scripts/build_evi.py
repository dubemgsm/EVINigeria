import os
import pandas as pd
import geopandas as gpd
import numpy as np
from shapely.ops import nearest_points

# File paths
SHP_PATH = "data/raw/nga_shp/nga_admin2.shp"
CONFLICT_PATH = "data/raw/acled_conflict.csv"
POPULATION_PATH = "data/raw/population.csv"
SCHOOLS_PATH = "data/raw/schools.csv"
OUTPUT_PATH = "data/processed/evi_scores.csv"

os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

print("1. Loading and cleaning spatial boundaries...")
gdf = gpd.read_file(SHP_PATH)
if gdf.crs != "EPSG:4326":
    gdf = gdf.to_crs("EPSG:4326")

bay_shp = gdf[gdf['adm1_name'].isin(['Borno', 'Adamawa', 'Yobe'])].copy()
bay_shp['adm2_name'] = bay_shp['adm2_name'].replace({'Tarmua': 'Tarmuwa'})
bay_shp.loc[bay_shp['adm2_name'] == 'Girei', 'adm2_pcode'] = 'NG002004'
bay_shp.loc[bay_shp['adm2_name'] == 'Gombi', 'adm2_pcode'] = 'NG002005'

# Project shapefile to UTM Zone 32N (EPSG:32632) for distances in meters
bay_shp_proj = bay_shp.to_crs(epsg=32632)
bay_shp_proj['centroid'] = bay_shp_proj.geometry.centroid

print("2. Loading conflict, school, and population data...")
conflict_df = pd.read_csv(CONFLICT_PATH).drop_duplicates().dropna(subset=['latitude', 'longitude'])
schools_df = pd.read_csv(SCHOOLS_PATH).drop_duplicates().dropna(subset=['latitude', 'longitude'])
pop_df = pd.read_csv(POPULATION_PATH).drop_duplicates()

# Correct population naming and pcodes
pop_df['lga'] = pop_df['lga'].replace({'Tarmua': 'Tarmuwa'})
pop_df.loc[pop_df['lga'] == 'Girei', 'pcode'] = 'NG002004'
pop_df.loc[pop_df['lga'] == 'Gombi', 'pcode'] = 'NG002005'

# Convert conflict and schools to GeoDataFrames and project them
conflict_gdf = gpd.GeoDataFrame(
    conflict_df,
    geometry=gpd.points_from_xy(conflict_df['longitude'], conflict_df['latitude']),
    crs="EPSG:4326"
)
conflict_gdf_proj = conflict_gdf.to_crs(epsg=32632)

schools_gdf = gpd.GeoDataFrame(
    schools_df,
    geometry=gpd.points_from_xy(schools_df['longitude'], schools_df['latitude']),
    crs="EPSG:4326"
)
schools_gdf_proj = schools_gdf.to_crs(epsg=32632)

print("3. Feature Engineering: Conflict Intensity (Recency & Fatalities Weighted)...")
# Filter conflict events to BAY states via spatial join
conflict_bay = gpd.sjoin(conflict_gdf, bay_shp, how="inner", predicate="intersects")

# Calculate recency weight (5-year half-life)
# Reference date is the max date in the dataset
conflict_bay['date_dt'] = pd.to_datetime(conflict_bay['date_start'])
date_max = conflict_bay['date_dt'].max()
conflict_bay['days_ago'] = (date_max - conflict_bay['date_dt']).dt.days
# Half-life of 5 years (1826.25 days) -> lambda = ln(2) / 5 = 0.1386
conflict_bay['recency_weight'] = np.exp(-0.1386 * (conflict_bay['days_ago'] / 365.25))

# Handle fatalities (best column) log-scaling to prevent outlier domination
conflict_bay['best'] = conflict_bay['best'].fillna(0)
conflict_bay['event_score'] = conflict_bay['recency_weight'] * (1 + np.log1p(conflict_bay['best']))

# Aggregate event score by LGA
conflict_intensity_agg = conflict_bay.groupby('adm2_pcode')['event_score'].sum().reset_index()
conflict_intensity_agg.columns = ['pcode', 'conflict_intensity']

print("4. Feature Engineering: Distance Proximities...")
# Distance from LGA centroid to nearest conflict event in BAY
conflict_points_union = conflict_gdf_proj.union_all()
schools_points_union = schools_gdf_proj.union_all()

proximity_conflict_list = []
dist_school_list = []

for idx, row in bay_shp_proj.iterrows():
    c = row['centroid']
    
    # Nearest conflict point
    near_conflict = nearest_points(c, conflict_points_union)[1]
    dist_c_km = c.distance(near_conflict) / 1000.0
    proximity_conflict_list.append((row['adm2_pcode'], dist_c_km))
    
    # Nearest school point
    near_school = nearest_points(c, schools_points_union)[1]
    dist_s_km = c.distance(near_school) / 1000.0
    dist_school_list.append((row['adm2_pcode'], dist_s_km))

proximity_conflict_df = pd.DataFrame(proximity_conflict_list, columns=['pcode', 'proximity_to_conflict'])
dist_school_df = pd.DataFrame(dist_school_list, columns=['pcode', 'distance_to_nearest_school'])

print("5. Feature Engineering: School Density and Population Pressure...")
# Spatial join for schools
schools_bay = gpd.sjoin(schools_gdf, bay_shp, how="inner", predicate="intersects")
schools_agg = schools_bay.groupby('adm2_pcode')['id'].count().reset_index()
schools_agg.columns = ['pcode', 'school_count']

# Assemble features at LGA level
base_lgas = bay_shp[['adm1_name', 'adm2_name', 'adm2_pcode', 'area_sqkm']].copy()
base_lgas.columns = ['state', 'lga', 'pcode', 'area_sqkm']

features = pd.merge(base_lgas, conflict_intensity_agg, on='pcode', how='left')
features['conflict_intensity'] = features['conflict_intensity'].fillna(0)

features = pd.merge(features, schools_agg, on='pcode', how='left')
features['school_count'] = features['school_count'].fillna(0).astype(int)

features = pd.merge(features, pop_df[['state', 'lga', 'pcode', 'school_age_total']], on=['state', 'lga', 'pcode'], how='left')
# Fill missing total population if any (using shapefile join check)
features['school_age_total'] = features['school_age_total'].fillna(0)

features = pd.merge(features, proximity_conflict_df, on='pcode', how='left')
features = pd.merge(features, dist_school_df, on='pcode', how='left')

# Calculate School Density: number of schools per 1,000 children
features['school_density'] = (features['school_count'] / features['school_age_total'].replace(0, 1)) * 1000.0
# Define Population Pressure: number of school-age children per LGA
features['population_pressure'] = features['school_age_total']

print("6. Constructing Education Vulnerability Index (EVI)...")
# Helper function for MinMax Normalization
def normalize(series):
    s_min = series.min()
    s_max = series.max()
    if s_max - s_min == 0:
        return series * 0.0
    return (series - s_min) / (s_max - s_min)

# Normalize components
features['conflict_intensity_norm'] = normalize(features['conflict_intensity'])
features['population_pressure_norm'] = normalize(features['population_pressure'])
features['school_density_norm'] = normalize(features['school_density'])

# Formula: EVI = (0.4 * Conflict Intensity) + (0.4 * Population Pressure) - (0.2 * School Density)
features['evi_raw'] = (0.4 * features['conflict_intensity_norm'] + 
                        0.4 * features['population_pressure_norm'] - 
                        0.2 * features['school_density_norm'])

# Normalize EVI to [0, 1] scale
features['evi_score'] = normalize(features['evi_raw'])

# Rank from highest to lowest vulnerability (1 is the most vulnerable)
features['rank'] = features['evi_score'].rank(ascending=False, method='min').astype(int)

# Sort by rank
features = features.sort_values(by='rank').reset_index(drop=True)

# Select final columns to save
final_cols = [
    'state', 'lga', 'pcode', 'area_sqkm', 'conflict_intensity', 'school_count', 
    'school_age_total', 'school_density', 'population_pressure', 
    'proximity_to_conflict', 'distance_to_nearest_school', 'evi_score', 'rank'
]
output_df = features[final_cols]

# Save output
output_df.to_csv(OUTPUT_PATH, index=False)
print(f"EVI construction finished! Saved {len(output_df)} rows to {OUTPUT_PATH}")
print(output_df.head(10))
