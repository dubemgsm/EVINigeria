import os
import pandas as pd
import geopandas as gpd

# Define paths
SHP_PATH = "data/raw/nga_shp/nga_admin2.shp"
CONFLICT_PATH = "data/raw/acled_conflict.csv"
POPULATION_PATH = "data/raw/population.csv"
SCHOOLS_PATH = "data/raw/schools.csv"

PROCESSED_DIR = "data/processed"
os.makedirs(PROCESSED_DIR, exist_ok=True)

print("1. Loading and cleaning administrative boundaries shapefile...")
# Load the shapefile
gdf = gpd.read_file(SHP_PATH)

# Standardize coordinate system (WGS84 / EPSG:4326)
if gdf.crs != "EPSG:4326":
    gdf = gdf.to_crs("EPSG:4326")

# Clip to BAY states
bay_shp = gdf[gdf['adm1_name'].isin(['Borno', 'Adamawa', 'Yobe'])].copy()

# Name and Pcode corrections:
# Rename Tarmua to Tarmuwa
bay_shp['adm2_name'] = bay_shp['adm2_name'].replace({'Tarmua': 'Tarmuwa'})

# Correct Girei and Gombi pcodes (swapped in shapefile)
# Girei should be NG002004, Gombi should be NG002005 (alphabetical order)
bay_shp.loc[bay_shp['adm2_name'] == 'Girei', 'adm2_pcode'] = 'NG002004'
bay_shp.loc[bay_shp['adm2_name'] == 'Gombi', 'adm2_pcode'] = 'NG002005'

# Verify counts and list LGAs
print(f"Total LGAs in BAY shapefile after cleaning: {len(bay_shp)}")

# Create a base DataFrame containing all 65 LGAs to ensure completeness in all outputs
base_lgas = bay_shp[['adm1_name', 'adm2_name', 'adm2_pcode', 'area_sqkm']].copy()
base_lgas.columns = ['state', 'lga', 'pcode', 'area_sqkm']
base_lgas = base_lgas.sort_values(by=['state', 'lga']).reset_index(drop=True)


print("\n2. Processing conflict data...")
# Load conflict data
conflict_df = pd.read_csv(CONFLICT_PATH)

# Remove duplicates
conflict_df = conflict_df.drop_duplicates()

# Handle missing values in critical columns
conflict_df = conflict_df.dropna(subset=['latitude', 'longitude'])
if 'best' in conflict_df.columns:
    conflict_df['best'] = conflict_df['best'].fillna(0)

# Convert to GeoDataFrame
conflict_gdf = gpd.GeoDataFrame(
    conflict_df,
    geometry=gpd.points_from_xy(conflict_df['longitude'], conflict_df['latitude']),
    crs="EPSG:4326"
)

# Spatial join to clip to BAY states and assign correct LGA names and pcodes
conflict_joined = gpd.sjoin(conflict_gdf, bay_shp, how="inner", predicate="intersects")

# Aggregate to LGA level
conflict_agg = conflict_joined.groupby('adm2_pcode').agg(
    conflict_count=('id', 'count'),
    fatalities=('best', 'sum')
).reset_index()
conflict_agg.rename(columns={'adm2_pcode': 'pcode'}, inplace=True)

# Merge with base LGAs to include all 65 LGAs (with 0s for LGAs without conflict)
conflict_by_lga = pd.merge(base_lgas[['state', 'lga', 'pcode']], conflict_agg, on='pcode', how='left')
conflict_by_lga['conflict_count'] = conflict_by_lga['conflict_count'].fillna(0).astype(int)
conflict_by_lga['fatalities'] = conflict_by_lga['fatalities'].fillna(0).astype(int)

# Save output
conflict_by_lga.to_csv(os.path.join(PROCESSED_DIR, "conflict_by_lga.csv"), index=False)
conflict_by_lga.to_csv(os.path.join(PROCESSED_DIR, "conflict_by_LGA.csv"), index=False)
print("Saved conflict_by_lga.csv with shape:", conflict_by_lga.shape)


print("\n3. Processing population data...")
# Load population data
pop_df = pd.read_csv(POPULATION_PATH)

# Clean duplicates
pop_df = pop_df.drop_duplicates()

# Correct names in population data: Tarmua -> Tarmuwa
pop_df['lga'] = pop_df['lga'].replace({'Tarmua': 'Tarmuwa'})

# Correct pcodes in population data (if any discrepancies exist)
# Girei = NG002004, Gombi = NG002005. Let's make sure they match
pop_df.loc[pop_df['lga'] == 'Girei', 'pcode'] = 'NG002004'
pop_df.loc[pop_df['lga'] == 'Gombi', 'pcode'] = 'NG002005'

# Merge population with base LGAs (to get area_sqkm)
pop_by_lga = pd.merge(base_lgas, pop_df, on=['state', 'lga', 'pcode'], how='left')

# Calculate school age population density: school_age_total / area_sqkm
pop_by_lga['school_age_population_density'] = pop_by_lga['school_age_total'] / pop_by_lga['area_sqkm']

# Save output
pop_by_lga.to_csv(os.path.join(PROCESSED_DIR, "population_by_lga.csv"), index=False)
pop_by_lga.to_csv(os.path.join(PROCESSED_DIR, "population_by_LGA.csv"), index=False)
print("Saved population_by_lga.csv with shape:", pop_by_lga.shape)


print("\n4. Processing school data...")
# Load school data
schools_df = pd.read_csv(SCHOOLS_PATH)

# Remove duplicates
schools_df = schools_df.drop_duplicates()

# Handle missing coordinates
schools_df = schools_df.dropna(subset=['latitude', 'longitude'])

# Convert to GeoDataFrame
schools_gdf = gpd.GeoDataFrame(
    schools_df,
    geometry=gpd.points_from_xy(schools_df['longitude'], schools_df['latitude']),
    crs="EPSG:4326"
)

# Spatial join to clip to BAY states and assign correct LGA names and pcodes
schools_joined = gpd.sjoin(schools_gdf, bay_shp, how="inner", predicate="intersects")

# Aggregate school count to LGA level
schools_agg = schools_joined.groupby('adm2_pcode').agg(
    school_count=('id', 'count')
).reset_index()
schools_agg.rename(columns={'adm2_pcode': 'pcode'}, inplace=True)

# We can also aggregate counts by school category (layer)
schools_layer_agg = pd.crosstab(schools_joined['adm2_pcode'], schools_joined['layer']).reset_index()
schools_layer_agg.rename(columns={'adm2_pcode': 'pcode'}, inplace=True)

# Merge overall school count with base LGAs
schools_by_lga = pd.merge(base_lgas[['state', 'lga', 'pcode']], schools_agg, on='pcode', how='left')
schools_by_lga = pd.merge(schools_by_lga, schools_layer_agg, on='pcode', how='left')

# Fill NaNs with 0 and convert counts to int
schools_by_lga = schools_by_lga.fillna(0)
for col in schools_by_lga.columns[3:]:
    schools_by_lga[col] = schools_by_lga[col].astype(int)

# Save output
schools_by_lga.to_csv(os.path.join(PROCESSED_DIR, "schools_by_lga.csv"), index=False)
schools_by_lga.to_csv(os.path.join(PROCESSED_DIR, "schools_by_LGA.csv"), index=False)
print("Saved schools_by_lga.csv with shape:", schools_by_lga.shape)

print("\nData cleaning and preparation finished successfully!")
